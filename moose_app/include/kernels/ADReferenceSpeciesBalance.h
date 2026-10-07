// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "ADKernel.h"
#include "RankTwoTensor.h"
class ADReferenceSpeciesBalance : public ADKernel
{
public:
  static InputParameters validParams();
  ADReferenceSpeciesBalance(const InputParameters & parameters);
protected:
  ADReal computeQpResidual() override;

  const ADMaterialProperty<Real> & _source;
  const ADMaterialProperty<RealVectorValue> * _flux;
};
