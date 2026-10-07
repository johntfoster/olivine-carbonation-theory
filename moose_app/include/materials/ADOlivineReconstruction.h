#pragma once
#include "Material.h"
class ADOlivineReconstruction : public Material
{
public:
 static InputParameters validParams();
 ADOlivineReconstruction(const InputParameters &);
protected:
 void initQpStatefulProperties() override { computeQpProperties(); }
 void computeQpProperties() override;
 const ADVariableValue & _backbone;
 const ADVariableValue & _enrichment;
 const ADVariableGradient & _gradient;
 ADMaterialProperty<Real> & _value;
 ADMaterialProperty<RealVectorValue> & _grad;
};
