// SPDX-License-Identifier: Apache-2.0
#include "ADTransferPotential.h"

registerMooseObject("OlivineCarbonationApp", ADTransferPotential);
InputParameters
ADTransferPotential::validParams()
{
  auto p = ADTimeKernel::validParams();
  p.addRequiredParam<MaterialPropertyName>("skeleton_velocity", "Skeleton velocity at fixed X; eq:weak_tau.");
  return p;
}
ADTransferPotential::ADTransferPotential(const InputParameters & parameters)
  : ADTimeKernel(parameters), _velocity(getADMaterialProperty<RealVectorValue>("skeleton_velocity"))
{}
ADReal
ADTransferPotential::computeQpResidual()
{
  return _test[_i][_qp]*(_u_dot[_qp] - 0.5*(_velocity[_qp]*_velocity[_qp]));
}
