#pragma once
#include "Material.h"
class ADSkeletonVelocity : public Material
{
public:
 static InputParameters validParams();
 ADSkeletonVelocity(const InputParameters &);
protected:
 void computeQpProperties() override;
 std::vector<const ADVariableValue *> _rates;
 ADMaterialProperty<RealVectorValue> & _velocity;
};
