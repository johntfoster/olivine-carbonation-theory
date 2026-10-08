.PHONY: check paper site moose test verification-examples
check:
	tools/agentctl check
	python3 .agent/shared/tools/research_project.py check
paper:
	python3 scripts/build_paper.py
site:
	python3 scripts/build_site.py

moose:
	tools/moose-run make -C moose_app -j2
test:
	tools/moose-run python3 scripts/check_implementation.py
verification-examples:
	tools/moose-run python3 scripts/run_silica_verification.py
