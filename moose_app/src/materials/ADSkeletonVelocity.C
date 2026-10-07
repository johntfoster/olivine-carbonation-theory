#include "ADSkeletonVelocity.h"
registerMooseObject("OlivineCarbonationApp", ADSkeletonVelocity);
InputParameters ADSkeletonVelocity::validParams()
{
 auto p=Material::validParams();
 p.addRequiredCoupledVar("displacements", "Skeleton displacement components at fixed X");
 p.addRequiredParam<MaterialPropertyName>("velocity", "Skeleton velocity output");
 return p;
}
ADSkeletonVelocity::ADSkeletonVelocity(const InputParameters & p)
 : Material(p), _velocity(declareADProperty<RealVectorValue>("velocity"))
{
 if (coupledComponents("displacements") != _mesh.dimension())
   paramError("displacements", "Provide one component per mesh dimension");
 if (_fe_problem.isTransient())
   for (unsigned int i=0; i<coupledComponents("displacements"); ++i)
     _rates.push_back(&adCoupledDot("displacements",i));
}
void ADSkeletonVelocity::computeQpProperties()
{
 _velocity[_qp]=ADRealVectorValue();
 for (unsigned int i=0; i<_rates.size(); ++i) _velocity[_qp](i)=(*_rates[i])[_qp];
}
