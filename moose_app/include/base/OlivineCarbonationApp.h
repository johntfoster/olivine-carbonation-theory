#pragma once
#include "MooseApp.h"
class OlivineCarbonationApp : public MooseApp
{
public:
  static InputParameters validParams();
  OlivineCarbonationApp(const InputParameters &);
  static void registerApps();
  static void registerAll(Factory &, ActionFactory &, Syntax &);
};
