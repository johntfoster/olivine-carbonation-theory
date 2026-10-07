// SPDX-License-Identifier: Apache-2.0
#include "ADLogarithmicMinerals.h"
#include "MatchedLogMineralState.h"
#include "metaphysicl/raw_type.h"
#include <cmath>
#include <algorithm>
registerMooseObject("OlivineCarbonationApp", ADLogarithmicMinerals);
InputParameters ADLogarithmicMinerals::validParams()
{
 auto p=Material::validParams();
 p.addRequiredParam<MaterialPropertyName>("deformation_gradient", "F");
 p.addRequiredParam<MaterialPropertyName>("jacobian", "J");
 p.addRequiredParam<MaterialPropertyName>("pressure", "Common intrinsic pore pressure");
 p.addParam<MaterialPropertyName>("electric_field", "", "Current E; omit for field-free reduction");
 p.addRangeCheckedParam<Real>("permittivity", 1.0, "permittivity>0", "Common epsilon");
 for (auto name : {"reference_fractions", "reference_densities", "allocated_bulk_moduli", "mineral_bulk_moduli", "shear_moduli"})
   p.addRequiredParam<std::vector<Real>>(name, "Per-solid constants in identical phase order");
 p.addRequiredParam<std::vector<MaterialPropertyName>>("volume_fractions", "Current solid fractions");
 p.addRequiredParam<std::vector<MaterialPropertyName>>("densities", "Intrinsic density outputs");
 p.addRequiredParam<std::vector<MaterialPropertyName>>("mineral_jacobians", "True deformation determinant outputs");
 p.addRequiredParam<MaterialPropertyName>("stress", "Total first Piola output");
 p.addRequiredParam<MaterialPropertyName>("biot", "Aggregate instantaneous Biot coefficient output");
 return p;
}
ADLogarithmicMinerals::ADLogarithmicMinerals(const InputParameters & p)
 : Material(p), _F(getADMaterialProperty<RankTwoTensor>("deformation_gradient")),
 _J(getADMaterialProperty<Real>("jacobian")), _p(getADMaterialProperty<Real>("pressure")),
 _E(getParam<MaterialPropertyName>("electric_field").empty() ? nullptr : &getADMaterialProperty<RealVectorValue>("electric_field")),
 _phi0(getParam<std::vector<Real>>("reference_fractions")), _rho0(getParam<std::vector<Real>>("reference_densities")),
 _K(getParam<std::vector<Real>>("allocated_bulk_moduli")), _Ks(getParam<std::vector<Real>>("mineral_bulk_moduli")),
 _G(getParam<std::vector<Real>>("shear_moduli")), _epsilon(getParam<Real>("permittivity")),
 _P(declareADProperty<RankTwoTensor>("stress")), _B(declareADProperty<Real>("biot"))
{
 const auto & fractions=getParam<std::vector<MaterialPropertyName>>("volume_fractions");
 const auto & densities=getParam<std::vector<MaterialPropertyName>>("densities");
 const auto & roots=getParam<std::vector<MaterialPropertyName>>("mineral_jacobians");
 getMaterialPropertyOld<RankTwoTensor>("deformation_gradient");
 getMaterialPropertyOld<Real>("jacobian");
 getMaterialPropertyOld<Real>("pressure");
 const auto n=_phi0.size();
 if (n<1 || n>3 || _rho0.size()!=n || _K.size()!=n || _Ks.size()!=n || _G.size()!=n || fractions.size()!=n || densities.size()!=n || roots.size()!=n)
   paramError("reference_fractions", "Use equal-sized vectors of one to three solids (one/two only for reductions)");
 for (unsigned int s=0; s<n; ++s)
 {
   if (!(_phi0[s]>0 && _rho0[s]>0 && _G[s]>0 && _K[s]>0 && _K[s]<_phi0[s]*_Ks[s]))
     paramError("allocated_bulk_moduli", "Require positive constants and 0<K<phi_s0 K_s");
   _fractions.push_back(&getADMaterialProperty<Real>(fractions[s]));
   getMaterialPropertyOld<Real>(fractions[s]);
   _densities.push_back(&declareADProperty<Real>(densities[s]));
   _roots.push_back(&declareADProperty<Real>(roots[s]));
 }
}
void ADLogarithmicMinerals::computeQpProperties()
{
 const Real J=MetaPhysicL::raw_value(_J[_qp]);
 if (J<=0) mooseException("Positive skeleton J required");
 ADRankTwoTensor I; I.zero(); for (unsigned int i=0; i<3; ++i) I(i,i)=1;
 const ADRankTwoTensor C=_F[_qp]*_F[_qp].transpose();
 const ADRankTwoTensor deviator=C-C.trace()/3.0*I;
 ADRankTwoTensor sigma=-_p[_qp]*I;
 _B[_qp]=1.0;
 ADReal total_fraction=0;
 for (unsigned int s=0; s<_phi0.size(); ++s)
 {
   const ADReal phi=(*_fractions[s])[_qp];
   if (MetaPhysicL::raw_value(phi)<=0) mooseException("Positive solid masses required; phase disappearance is outside this branch");
   total_fraction+=phi;
   const Real k=_K[s]/_phi0[s], a=1-k/_Ks[s];
   // Author's companion solver: select the stable branch, then Newton in AD.
   const ADReal b_ad=matchedLogMineralVolume(_J[_qp], _p[_qp], _K[s], _Ks[s], _phi0[s]);
   (*_roots[s])[_qp]=b_ad;
   (*_densities[s])[_qp]=_rho0[s]/b_ad;
   sigma += phi/b_ad*(_G[s]*pow(_J[_qp],-2.0/3.0)*deviator
                      + k/a*log(_J[_qp]/b_ad)*I);
   _B[_qp]-=phi*k/(_Ks[s]+a*_p[_qp]*b_ad);
 }
 if (MetaPhysicL::raw_value(total_fraction)>=1.0) mooseException("Positive aqueous pore volume required");
 if (_E)
 {
   ADRankTwoTensor outer;
   for (unsigned int i=0; i<3; ++i) for (unsigned int j=0; j<3; ++j) outer(i,j)=(*_E)[_qp](i)*(*_E)[_qp](j);
   sigma+=_epsilon*(outer-0.5*((*_E)[_qp]*(*_E)[_qp])*I);
 }
 _P[_qp]=_J[_qp]*sigma*_F[_qp].inverse().transpose();
}
