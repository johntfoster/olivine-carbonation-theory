// SPDX-License-Identifier: Apache-2.0
#include "ADReferenceSpeciesBalance.h"

registerMooseObject("OlivineCarbonationApp", ADReferenceSpeciesBalance);
InputParameters
ADReferenceSpeciesBalance::validParams()
{
  auto p = ADKernel::validParams();
  p.addRequiredParam<MaterialPropertyName>("source", "Reference source J sum(nu r), eq:weak_fluid/weak_solid.");
  p.addParam<MaterialPropertyName>("flux", "", "Full reference component flux; omit for pure solids.");
  return p;
}
ADReferenceSpeciesBalance::ADReferenceSpeciesBalance(const InputParameters & parameters)
  : ADKernel(parameters),
    _source(getADMaterialProperty<Real>("source")),
    _flux(getParam<MaterialPropertyName>("flux").empty() ? nullptr : &getADMaterialProperty<RealVectorValue>("flux"))
{}
ADReal
ADReferenceSpeciesBalance::computeQpResidual()
{
  return -_test[_i][_qp]*_source[_qp]
         - (_flux ? _grad_test[_i][_qp]*(*_flux)[_qp] : ADReal(0.0));
}
