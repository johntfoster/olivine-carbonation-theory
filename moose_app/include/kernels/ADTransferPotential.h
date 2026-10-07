// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "ADTimeKernel.h"
#include "RankTwoTensor.h"
class ADTransferPotential : public ADTimeKernel
{
public:
  static InputParameters validParams();
  ADTransferPotential(const InputParameters & parameters);
protected:
  ADReal computeQpResidual() override;

  const ADMaterialProperty<RealVectorValue> & _velocity;
};
