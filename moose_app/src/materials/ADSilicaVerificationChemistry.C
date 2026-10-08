// SPDX-License-Identifier: Apache-2.0
#include "ADSilicaVerificationChemistry.h"
#include "metaphysicl/raw_type.h"
#include <cmath>

registerMooseObject("OlivineCarbonationApp", ADSilicaVerificationChemistry);
namespace { constexpr Real MS = 0.096113, MW = 0.018015, MC = 0.060083;
            constexpr Real RT = 8.31446261815324 * 298.15; }
InputParameters ADSilicaVerificationChemistry::validParams()
{
  auto p = Material::validParams();
  p.addRequiredCoupledVar("potential", "q = MS*(mu_Si-mu_water)/(R theta)");
  p.addCoupledVar("enrichment", "Optional P0 addition to q");
  p.addRequiredCoupledVar("solid_fraction", "Silica fraction; inert A and B remain positive");
  p.addRangeCheckedParam<Real>("density", 1000, "density>0", "Common test density");
  p.addRangeCheckedParam<Real>("inert_solid_fraction", 0.3, "inert_solid_fraction>0 & inert_solid_fraction<1", "A plus B");
  p.addRangeCheckedParam<Real>("rate_coefficient", 0.1, "rate_coefficient>0", "K_(3) R, mol/(m3 s)");
  p.addRangeCheckedParam<Real>("diffusion_mobility", 0, "diffusion_mobility>=0", "L, kg s/m3; zero for closed box");
  p.addRequiredRangeCheckedParam<Real>("equilibrium_quotient", "equilibrium_quotient>0", "x_Si/x_water^2 at equilibrium");
  return p;
}
ADSilicaVerificationChemistry::ADSilicaVerificationChemistry(const InputParameters & p)
  : Material(p), _q(adCoupledValue("potential")), _grad_q(adCoupledGradient("potential")),
    _enrichment(isCoupled("enrichment") ? &adCoupledValue("enrichment") : nullptr),
    _phi(adCoupledValue("solid_fraction")), _rho(getParam<Real>("density")),
    _inert(getParam<Real>("inert_solid_fraction")), _rate(getParam<Real>("rate_coefficient")),
    _mobility(getParam<Real>("diffusion_mobility")), _Qeq(getParam<Real>("equilibrium_quotient")),
    _fluid_phi(declareADProperty<Real>("fluid_phi")), _solid_phi(declareADProperty<Real>("silica_phi")),
    _eta(declareADProperty<Real>("silica_eta")), _source_f(declareADProperty<Real>("silica_fluid_source")),
    _source_s(declareADProperty<Real>("silica_solid_source")),
    _silicon(declareADProperty<Real>("aqueous_silicon")), _water(declareADProperty<Real>("water_moles")),
    _reaction(declareADProperty<Real>("silica_rate")),
    _dissipation(declareADProperty<Real>("reaction_power")),
    _flux(declareADProperty<RealVectorValue>("silica_flux")),
    _D(declareADProperty<RankTwoTensor>("silica_mobility"))
{}
void ADSilicaVerificationChemistry::computeQpProperties()
{
  const ADReal q = _q[_qp] + (_enrichment ? (*_enrichment)[_qp] : ADReal(0));
  // y=log(x/(1-x)); q=y+(MS/MW-1)*log(1+exp(y)).
  // Monotone inversion in AD retains derivatives of the mass fractions.
  ADReal y = q;
  for (unsigned int i=0; i<20; ++i)
  {
    const ADReal e=exp(y), x=e/(1+e);
    const ADReal step=(y+(MS/MW-1)*log(1+e)-q)/(1+(MS/MW-1)*x);
    y-=step;
    if (std::abs(MetaPhysicL::raw_value(step))<1e-14) break;
  }
  const ADReal x=1/(1+exp(-y));
  if (std::abs(MetaPhysicL::raw_value(log(x)-(MS/MW)*log(1-x)-q))>1e-10)
    mooseException("Silica potential inversion failed");
  _solid_phi[_qp]=_phi[_qp];
  _fluid_phi[_qp]=1-_inert-_phi[_qp];
  if (MetaPhysicL::raw_value(_phi[_qp])<=0 || MetaPhysicL::raw_value(_fluid_phi[_qp])<=0)
    mooseException("Positive mineral and fluid fractions required");
  _eta[_qp]=MS*x/(MS*x+MW*(1-x));
  _silicon[_qp]=_rho*_fluid_phi[_qp]*_eta[_qp]/MS;
  _water[_qp]=_rho*_fluid_phi[_qp]*(1-_eta[_qp])/MW;
  const ADReal force=log(x)-2*log(1-x)-std::log(_Qeq);
  _reaction[_qp]=_rate*force;
  _source_f[_qp]=-MS*_reaction[_qp];
  _source_s[_qp]=MC*_reaction[_qp];
  _dissipation[_qp]=RT*_reaction[_qp]*force;
  _D[_qp].zero();
  for (unsigned int i=0; i<3; ++i) _D[_qp](i,i)=_mobility*RT/MS;
  _flux[_qp]=-(_mobility*RT/MS)*_grad_q[_qp];
}
