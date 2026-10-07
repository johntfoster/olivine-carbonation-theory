// SPDX-License-Identifier: Apache-2.0
#include "ADCarbonationMomentum.h"

registerMooseObject("OlivineCarbonationApp", ADCarbonationMomentum);
InputParameters
ADCarbonationMomentum::validParams()
{
  auto p = ADKernel::validParams();
  p.addRequiredRangeCheckedParam<unsigned int>("component", "component<3", "Momentum component; eq:weak_momentum.");
  p.addRequiredParam<MaterialPropertyName>("stress", "Total nominal stress including pressure and Maxwell stress.");
  p.addRequiredParam<MaterialPropertyName>("deformation_gradient", "F");
  p.addRequiredParam<MaterialPropertyName>("jacobian", "J");
  p.addRequiredParam<MaterialPropertyName>("density", "Current mixture density rho");
  p.addRequiredParam<MaterialPropertyName>("fluid_density", "Partial aqueous density phi_f rhobar_f");
  p.addRequiredParam<MaterialPropertyName>("fluid_production", "Current net aqueous mass production sum(cdot_f)");
  p.addRequiredParam<MaterialPropertyName>("relative_flux", "Reference bulk relative mass flux W_f");
  p.addParam<RealVectorValue>("gravity", RealVectorValue(), "Body acceleration");
  return p;
}
ADCarbonationMomentum::ADCarbonationMomentum(const InputParameters & parameters)
  : ADKernel(parameters), _component(getParam<unsigned int>("component")),
    _P(getADMaterialProperty<RankTwoTensor>("stress")),
    _F(getADMaterialProperty<RankTwoTensor>("deformation_gradient")),
    _J(getADMaterialProperty<Real>("jacobian")),
    _rho(getADMaterialProperty<Real>("density")),
    _rho_f(getADMaterialProperty<Real>("fluid_density")),
    _conversion(getADMaterialProperty<Real>("fluid_production")),
    _W(getADMaterialProperty<RealVectorValue>("relative_flux")),
    _gravity(getParam<RealVectorValue>("gravity"))
{}
ADReal
ADCarbonationMomentum::computeQpResidual()
{
  if (_component >= _mesh.dimension()) mooseError("Momentum component exceeds mesh dimension");
  if (_rho_f[_qp] <= 0.0) mooseException("Positive aqueous partial density required");
  ADReal result = 0.0;
  for (unsigned int j=0; j<3; ++j) result += _grad_test[_i][_qp](j)*_P[_qp](_component,j);
  return result + _test[_i][_qp]*(-_J[_qp]*_rho[_qp]*_gravity(_component)
      + _conversion[_qp]/_rho_f[_qp]*(_F[_qp]*_W[_qp])(_component));
}
