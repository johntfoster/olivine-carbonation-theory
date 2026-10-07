// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "ADKernel.h"
#include "RankTwoTensor.h"
class ADReferenceGauss : public ADKernel
{
public:
  static InputParameters validParams();
  ADReferenceGauss(const InputParameters & parameters);
protected:
  ADReal computeQpResidual() override;

  const ADMaterialProperty<RankTwoTensor> & _dielectric;
  const ADMaterialProperty<Real> & _charge;
};
