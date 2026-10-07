#pragma once
#include "Material.h"
#include "RankTwoTensor.h"
/** Synthetic SPD two-component Onsager block used only by verification inputs. */
class ADCrossDiffusionVerification : public Material
{
public:
 static InputParameters validParams();
 ADCrossDiffusionVerification(const InputParameters &);
protected:
 void computeQpProperties() override;
 const ADVariableGradient & _p, & _q;
 ADMaterialProperty<RealVectorValue> & _flux_p, & _flux_q;
 ADMaterialProperty<RankTwoTensor> & _Dpp, & _Dqq, & _Dpq;
};
