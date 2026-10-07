// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "ADTimeKernel.h"
#include "RankTwoTensor.h"
class ADReferenceMassStorage : public ADTimeKernel
{
public:
  static InputParameters validParams();
  ADReferenceMassStorage(const InputParameters & parameters);
protected:
  ADReal computeQpResidual() override;

  const ADMaterialProperty<Real> & _mass;
  const MaterialProperty<Real> & _old;
  const MaterialProperty<Real> & _older;
};
