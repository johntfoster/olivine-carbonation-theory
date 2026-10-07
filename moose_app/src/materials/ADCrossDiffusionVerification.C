#include "ADCrossDiffusionVerification.h"
registerMooseObject("OlivineCarbonationApp", ADCrossDiffusionVerification);
InputParameters ADCrossDiffusionVerification::validParams()
{
 auto p=Material::validParams(); p.addRequiredCoupledVar("p", "First backbone");
 p.addRequiredCoupledVar("q", "Second backbone"); return p;
}
ADCrossDiffusionVerification::ADCrossDiffusionVerification(const InputParameters & p)
 : Material(p), _p(adCoupledGradient("p")), _q(adCoupledGradient("q")),
 _flux_p(declareADProperty<RealVectorValue>("flux_p")), _flux_q(declareADProperty<RealVectorValue>("flux_q")),
 _Dpp(declareADProperty<RankTwoTensor>("Dpp")), _Dqq(declareADProperty<RankTwoTensor>("Dqq")),
 _Dpq(declareADProperty<RankTwoTensor>("Dpq")) {}
void ADCrossDiffusionVerification::computeQpProperties()
{
 _Dpp[_qp].zero(); _Dqq[_qp].zero(); _Dpq[_qp].zero();
 for (unsigned int i=0; i<3; ++i) { _Dpp[_qp](i,i)=1; _Dqq[_qp](i,i)=2; _Dpq[_qp](i,i)=0.25; }
 _flux_p[_qp]=-_p[_qp]-0.25*_q[_qp];
 _flux_q[_qp]=-0.25*_p[_qp]-2.0*_q[_qp];
}
