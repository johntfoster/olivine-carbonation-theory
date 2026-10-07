#include "ADReferenceMass.h"
registerMooseObject("OlivineCarbonationApp", ADReferenceMass);
InputParameters ADReferenceMass::validParams()
{
 auto p=Material::validParams();
 p.addRequiredParam<MaterialPropertyName>("jacobian", "J");
 p.addRequiredParam<MaterialPropertyName>("volume_fraction", "phi; use total EG reconstruction");
 p.addRequiredParam<MaterialPropertyName>("density", "Intrinsic density rhobar");
 p.addParam<MaterialPropertyName>("mass_fraction", "", "eta; omit for a pure solid");
 p.addRequiredParam<MaterialPropertyName>("storage", "Complete reference storage output");
 return p;
}
ADReferenceMass::ADReferenceMass(const InputParameters & p)
 : Material(p), _J(getADMaterialProperty<Real>("jacobian")),
   _phi(getADMaterialProperty<Real>("volume_fraction")), _density(getADMaterialProperty<Real>("density")),
   _eta(getParam<MaterialPropertyName>("mass_fraction").empty() ? nullptr : &getADMaterialProperty<Real>("mass_fraction")),
   _storage(declareADProperty<Real>("storage"))
{
 // Make upstream outputs stateful so their initial values are evaluated before storage.
 getMaterialPropertyOld<Real>("jacobian");
 getMaterialPropertyOld<Real>("volume_fraction");
 getMaterialPropertyOld<Real>("density");
 if (_eta) getMaterialPropertyOld<Real>("mass_fraction");
}
void ADReferenceMass::computeQpProperties()
{ _storage[_qp]=_J[_qp]*_phi[_qp]*_density[_qp]*(_eta ? (*_eta)[_qp] : ADReal(1.0)); }
