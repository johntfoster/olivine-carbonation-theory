// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "Material.h"

/** Exact isovolumetric binary-aqueous reduction of manuscript mechanism (3). */
class ADSilicaVerificationChemistry : public Material
{
public:
  static InputParameters validParams();
  ADSilicaVerificationChemistry(const InputParameters &);
protected:
  void initQpStatefulProperties() override { computeQpProperties(); }
  void computeQpProperties() override;
  const ADVariableValue & _q;
  const ADVariableGradient & _grad_q;
  const ADVariableValue * _enrichment;
  const ADVariableValue & _phi;
  const Real _rho, _inert, _rate, _mobility, _Qeq;
  ADMaterialProperty<Real> & _fluid_phi;
  ADMaterialProperty<Real> & _solid_phi;
  ADMaterialProperty<Real> & _eta;
  ADMaterialProperty<Real> & _source_f;
  ADMaterialProperty<Real> & _source_s;
  ADMaterialProperty<Real> & _silicon;
  ADMaterialProperty<Real> & _water;
  ADMaterialProperty<Real> & _reaction;
  ADMaterialProperty<Real> & _dissipation;
  ADMaterialProperty<RealVectorValue> & _flux;
  ADMaterialProperty<RankTwoTensor> & _D;
};
