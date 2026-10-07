// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "Material.h"
#include "RankTwoTensor.h"
/** Positive-mass elastic branch of eq:mineral_solve, solid_energy and total_stress. */
class ADLogarithmicMinerals : public Material
{
public:
 static InputParameters validParams();
 ADLogarithmicMinerals(const InputParameters &);
protected:
 void initQpStatefulProperties() override { computeQpProperties(); }
 void computeQpProperties() override;
 const ADMaterialProperty<RankTwoTensor> & _F;
 const ADMaterialProperty<Real> & _J;
 const ADMaterialProperty<Real> & _p;
 const ADMaterialProperty<RealVectorValue> * _E;
 const std::vector<Real> _phi0, _rho0, _K, _Ks, _G;
 const Real _epsilon;
 std::vector<const ADMaterialProperty<Real> *> _fractions;
 std::vector<ADMaterialProperty<Real> *> _densities, _roots;
 ADMaterialProperty<RankTwoTensor> & _P;
 ADMaterialProperty<Real> & _B;
};
