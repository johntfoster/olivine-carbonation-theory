// SPDX-License-Identifier: Apache-2.0
#include "ADReferenceTraction.h"

registerMooseObject("OlivineCarbonationApp", ADReferenceTraction);
InputParameters
ADReferenceTraction::validParams()
{
  auto p = ADIntegratedBC::validParams();
  p.addRequiredRangeCheckedParam<unsigned int>("component", "component<3", "Traction component");
  p.addRequiredParam<MaterialPropertyName>("traction", "Outward nominal traction; negative boundary sign.");
  return p;
}
ADReferenceTraction::ADReferenceTraction(const InputParameters & parameters)
  : ADIntegratedBC(parameters), _component(getParam<unsigned int>("component")),
    _traction(getADMaterialProperty<RealVectorValue>("traction"))
{}
ADReal
ADReferenceTraction::computeQpResidual()
{
  return -_test[_i][_qp]*_traction[_qp](_component);
}
