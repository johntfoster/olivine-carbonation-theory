// SPDX-License-Identifier: Apache-2.0
#include "ADReferencePullback.h"
registerMooseObject("OlivineCarbonationApp", ADReferencePullback);
InputParameters ADReferencePullback::validParams()
{
 auto p=Material::validParams();
 p.addRequiredParam<MaterialPropertyName>("jacobian", "J");
 p.addRequiredParam<MaterialPropertyName>("inverse_deformation_gradient", "F^-1");
 p.addRequiredParam<MaterialPropertyName>("mass_fraction", "Total eta");
 p.addRequiredParam<MaterialPropertyName>("current_source", "Current component mass production sum nu r");
 p.addRequiredParam<MaterialPropertyName>("current_charge", "Current mixture charge varrho");
 p.addRequiredParam<MaterialPropertyName>("bulk_reference_flux", "W_f");
 p.addRequiredParam<MaterialPropertyName>("relative_current_flux", "j_diff+j_disp");
 p.addRequiredRangeCheckedParam<Real>("permittivity", "permittivity>0", "Common positive permittivity");
 p.addRequiredParam<MaterialPropertyName>("reference_flux", "Full component flux output");
 p.addRequiredParam<MaterialPropertyName>("reference_source", "J-weighted source output");
 p.addRequiredParam<MaterialPropertyName>("reference_charge", "J-weighted charge output");
 p.addRequiredParam<MaterialPropertyName>("dielectric", "Pulled-back dielectric output");
 return p;
}
ADReferencePullback::ADReferencePullback(const InputParameters & p)
 : Material(p), _J(getADMaterialProperty<Real>("jacobian")),
 _inverse(getADMaterialProperty<RankTwoTensor>("inverse_deformation_gradient")),
 _eta(getADMaterialProperty<Real>("mass_fraction")),
 _source(getADMaterialProperty<Real>("current_source")),
 _charge(getADMaterialProperty<Real>("current_charge")),
 _W(getADMaterialProperty<RealVectorValue>("bulk_reference_flux")),
 _j(getADMaterialProperty<RealVectorValue>("relative_current_flux")),
 _epsilon(getParam<Real>("permittivity")),
 _flux(declareADProperty<RealVectorValue>("reference_flux")),
 _reference_source(declareADProperty<Real>("reference_source")),
 _reference_charge(declareADProperty<Real>("reference_charge")),
 _dielectric(declareADProperty<RankTwoTensor>("dielectric")) {}
void ADReferencePullback::computeQpProperties()
{
 _flux[_qp]=_eta[_qp]*_W[_qp]+_J[_qp]*(_inverse[_qp]*_j[_qp]);
 _reference_source[_qp]=_J[_qp]*_source[_qp];
 _reference_charge[_qp]=_J[_qp]*_charge[_qp];
 _dielectric[_qp]=_epsilon*_J[_qp]*(_inverse[_qp]*_inverse[_qp].transpose());
}
