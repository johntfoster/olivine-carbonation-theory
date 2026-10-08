// SPDX-License-Identifier: Apache-2.0
#include "ADReferenceStorageRate.h"
#include "MooseVariableFE.h"
#include "SystemBase.h"
#include "TimeIntegrator.h"
registerMooseObject("OlivineCarbonationApp", ADReferenceStorageRate);
InputParameters ADReferenceStorageRate::validParams()
{
  auto p=Material::validParams();
  p.addRequiredCoupledVar("variable", "Field whose TimeIntegrator controls storage history");
  p.addRequiredParam<MaterialPropertyName>("storage", "Complete reference mass");
  p.addRequiredParam<MaterialPropertyName>("rate", "AD mass rate for both EG rows");
  return p;
}
ADReferenceStorageRate::ADReferenceStorageRate(const InputParameters & p)
  : Material(p), _mass(getADMaterialProperty<Real>("storage")),
    _old(getMaterialPropertyOld<Real>("storage")), _older(getMaterialPropertyOlder<Real>("storage")),
    _variable(getVar("variable",0)), _rate(declareADProperty<Real>("rate"))
{}
void ADReferenceStorageRate::computeQpProperties()
{
  if (_dt<=0) { _rate[_qp]=0; return; }
  const auto & integrator=_variable->sys().getTimeIntegrator(_variable->number());
  if (integrator.type()=="ImplicitEuler" || (integrator.type()=="BDF2" && _t_step==1))
    _rate[_qp]=(_mass[_qp]-_old[_qp])/_dt;
  else if (integrator.type()=="BDF2")
  {
    const Real r=_dt/_dt_old;
    _rate[_qp]=((1+2*r)/(1+r)*_mass[_qp]-(1+r)*_old[_qp]+r*r/(1+r)*_older[_qp])/_dt;
  }
  else mooseError("ADReferenceStorageRate requires implicit-euler or bdf2");
}
