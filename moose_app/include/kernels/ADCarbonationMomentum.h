// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "ADKernel.h"
#include "RankTwoTensor.h"
class ADCarbonationMomentum : public ADKernel
{
public:
  static InputParameters validParams();
  ADCarbonationMomentum(const InputParameters & parameters);
protected:
  ADReal computeQpResidual() override;

  const unsigned int _component;
  const ADMaterialProperty<RankTwoTensor> & _P;
  const ADMaterialProperty<RankTwoTensor> & _F;
  const ADMaterialProperty<Real> & _J;
  const ADMaterialProperty<Real> & _rho;
  const ADMaterialProperty<Real> & _rho_f;
  const ADMaterialProperty<Real> & _conversion;
  const ADMaterialProperty<RealVectorValue> & _W;
  const RealVectorValue _gravity;
};
