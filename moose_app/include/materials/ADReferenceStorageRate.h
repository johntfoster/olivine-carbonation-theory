// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "Material.h"
class ADReferenceStorageRate : public Material
{
public:
  static InputParameters validParams();
  ADReferenceStorageRate(const InputParameters &);
protected:
  void computeQpProperties() override;
  const ADMaterialProperty<Real> & _mass;
  const MaterialProperty<Real> & _old;
  const MaterialProperty<Real> & _older;
  MooseVariable * _variable;
  ADMaterialProperty<Real> & _rate;
};
