#include "ADOlivineReconstruction.h"
registerMooseObject("OlivineCarbonationApp", ADOlivineReconstruction);
InputParameters ADOlivineReconstruction::validParams()
{
 auto p=Material::validParams();
 p.addRequiredCoupledVar("backbone", "Continuous field");
 p.addCoupledVar("enrichment", 0.0, "Optional constant MONOMIAL enrichment");
 p.addRequiredParam<MaterialPropertyName>("value", "Total value output");
 p.addRequiredParam<MaterialPropertyName>("gradient", "Broken reference gradient output");
 return p;
}
ADOlivineReconstruction::ADOlivineReconstruction(const InputParameters & p)
 : Material(p), _backbone(adCoupledValue("backbone")), _enrichment(adCoupledValue("enrichment")),
   _gradient(adCoupledGradient("backbone")), _value(declareADProperty<Real>("value")),
   _grad(declareADProperty<RealVectorValue>("gradient")) {}
void ADOlivineReconstruction::computeQpProperties()
{
 _value[_qp]=_backbone[_qp]+_enrichment[_qp];
 _grad[_qp]=_gradient[_qp];
}
