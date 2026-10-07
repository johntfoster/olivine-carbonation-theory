// SPDX-License-Identifier: Apache-2.0
#include "ADReferenceMassStorage.h"
#include "SystemBase.h"
#include "TimeIntegrator.h"
#include "MooseVariableFE.h"
registerMooseObject("OlivineCarbonationApp", ADReferenceMassStorage);
InputParameters
ADReferenceMassStorage::validParams()
{
  auto p = ADTimeKernel::validParams();
  p.addRequiredParam<MaterialPropertyName>("storage", "Complete reference mass J phi rhobar eta; eq:weak_fluid/weak_solid.");
  p.addClassDescription("Conservative implicit Euler or variable-step BDF2 difference of complete reference mass, including all AD dependencies.");
  return p;
}
ADReferenceMassStorage::ADReferenceMassStorage(const InputParameters & parameters)
  : ADTimeKernel(parameters),
    _mass(getADMaterialProperty<Real>("storage")),
    _old(getMaterialPropertyOld<Real>("storage")),
    _older(getMaterialPropertyOlder<Real>("storage"))
{}
ADReal
ADReferenceMassStorage::computeQpResidual()
{
  if (_dt <= 0.0) return 0.0;
  const auto & integrator = _var.sys().getTimeIntegrator(_var.number());
  ADReal rate;
  if (integrator.type() == "ImplicitEuler" || (integrator.type() == "BDF2" && _t_step == 1))
    rate = (_mass[_qp] - _old[_qp]) / _dt;
  else if (integrator.type() == "BDF2")
  {
    const Real r = _dt / _dt_old;
    rate = ((1.0+2.0*r)/(1.0+r)*_mass[_qp] - (1.0+r)*_old[_qp]
            + r*r/(1.0+r)*_older[_qp])/_dt;
  }
  else
    mooseError("ADReferenceMassStorage requires implicit-euler or bdf2");
  return _test[_i][_qp] * rate;
}
