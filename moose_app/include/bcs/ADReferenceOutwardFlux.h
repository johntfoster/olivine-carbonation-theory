// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "ADIntegratedBC.h"
#include "RankTwoTensor.h"
class ADReferenceOutwardFlux : public ADIntegratedBC
{
public:
  static InputParameters validParams();
  ADReferenceOutwardFlux(const InputParameters & parameters);
protected:
  ADReal computeQpResidual() override;

  const ADMaterialProperty<Real> * _flux;
  const Function & _function;
};
