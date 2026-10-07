// SPDX-License-Identifier: Apache-2.0
#include "ADReferenceGauss.h"

registerMooseObject("OlivineCarbonationApp", ADReferenceGauss);
InputParameters
ADReferenceGauss::validParams()
{
  auto p = ADKernel::validParams();
  p.addRequiredParam<MaterialPropertyName>("dielectric", "J F^-1 epsilon F^-T, eq:weak_gauss.");
  p.addRequiredParam<MaterialPropertyName>("charge", "Reference charge J varrho.");
  return p;
}
ADReferenceGauss::ADReferenceGauss(const InputParameters & parameters)
  : ADKernel(parameters), _dielectric(getADMaterialProperty<RankTwoTensor>("dielectric")),
    _charge(getADMaterialProperty<Real>("charge"))
{}
ADReal
ADReferenceGauss::computeQpResidual()
{
  return _grad_test[_i][_qp]*(_dielectric[_qp]*_grad_u[_qp]) - _test[_i][_qp]*_charge[_qp];
}
