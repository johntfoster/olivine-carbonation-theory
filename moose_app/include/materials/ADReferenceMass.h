#pragma once
#include "Material.h"
class ADReferenceMass : public Material
{
public:
 static InputParameters validParams();
 ADReferenceMass(const InputParameters &);
protected:
 void initQpStatefulProperties() override { computeQpProperties(); }
 void computeQpProperties() override;
 const ADMaterialProperty<Real> & _J;
 const ADMaterialProperty<Real> & _phi;
 const ADMaterialProperty<Real> & _density;
 const ADMaterialProperty<Real> * _eta;
 ADMaterialProperty<Real> & _storage;
};
