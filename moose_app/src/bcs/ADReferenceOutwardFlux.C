// SPDX-License-Identifier: Apache-2.0
#include "ADReferenceOutwardFlux.h"
#include "Function.h"
registerMooseObject("OlivineCarbonationApp", ADReferenceOutwardFlux);
InputParameters
ADReferenceOutwardFlux::validParams()
{
  auto p = ADIntegratedBC::validParams();
  p.addParam<MaterialPropertyName>("flux", "", "Outward reference mass/electric flux; positive boundary sign.");
  p.addParam<FunctionName>("function", "0", "Prescribed outward flux if property omitted.");
  return p;
}
ADReferenceOutwardFlux::ADReferenceOutwardFlux(const InputParameters & parameters)
  : ADIntegratedBC(parameters), _flux(getParam<MaterialPropertyName>("flux").empty() ? nullptr : &getADMaterialProperty<Real>("flux")),
    _function(getFunction("function"))
{}
ADReal
ADReferenceOutwardFlux::computeQpResidual()
{
  return _test[_i][_qp]*(_flux ? (*_flux)[_qp] : ADReal(_function.value(_t,_q_point[_qp])));
}
