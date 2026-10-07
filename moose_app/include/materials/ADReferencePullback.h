// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "Material.h"
#include "RankTwoTensor.h"
/** Constitutive-output pullbacks only; no chemistry/drag law is replaced. */
class ADReferencePullback : public Material
{
public:
 static InputParameters validParams();
 ADReferencePullback(const InputParameters &);
protected:
 void computeQpProperties() override;
 const ADMaterialProperty<Real> & _J;
 const ADMaterialProperty<RankTwoTensor> & _inverse;
 const ADMaterialProperty<Real> & _eta;
 const ADMaterialProperty<Real> & _source;
 const ADMaterialProperty<Real> & _charge;
 const ADMaterialProperty<RealVectorValue> & _W;
 const ADMaterialProperty<RealVectorValue> & _j;
 const Real _epsilon;
 ADMaterialProperty<RealVectorValue> & _flux;
 ADMaterialProperty<Real> & _reference_source;
 ADMaterialProperty<Real> & _reference_charge;
 ADMaterialProperty<RankTwoTensor> & _dielectric;
};
