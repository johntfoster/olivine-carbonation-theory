// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "ADIntegratedBC.h"
#include "RankTwoTensor.h"
class ADReferenceTraction : public ADIntegratedBC
{
public:
  static InputParameters validParams();
  ADReferenceTraction(const InputParameters & parameters);
protected:
  ADReal computeQpResidual() override;

  const unsigned int _component;
  const ADMaterialProperty<RealVectorValue> & _traction;
};
