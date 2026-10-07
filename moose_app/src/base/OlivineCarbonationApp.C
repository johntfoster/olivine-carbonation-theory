#include "OlivineCarbonationApp.h"
#include "AppFactory.h"
#include "Moose.h"
#include "MooseSyntax.h"
registerKnownLabel("OlivineCarbonationApp");
InputParameters OlivineCarbonationApp::validParams() { auto p=MooseApp::validParams(); p.set<bool>("use_legacy_material_output")=false; p.set<bool>("use_legacy_initial_residual_evaluation_behavior")=false; return p; }
OlivineCarbonationApp::OlivineCarbonationApp(const InputParameters & p) : MooseApp(p)
{ registerAll(_factory, _action_factory, _syntax); }
void OlivineCarbonationApp::registerAll(Factory & f, ActionFactory & a, Syntax &)
{ Registry::registerObjectsTo(f, {"OlivineCarbonationApp"}); Registry::registerActionsTo(a, {"OlivineCarbonationApp"}); }
void OlivineCarbonationApp::registerApps() { registerApp(OlivineCarbonationApp); }
extern "C" void OlivineCarbonationApp__registerAll(Factory & f, ActionFactory & a, Syntax & s)
{ OlivineCarbonationApp::registerAll(f,a,s); }
extern "C" void OlivineCarbonationApp__registerApps() { OlivineCarbonationApp::registerApps(); }
