.PHONY: check paper site
check:
	tools/agentctl check
	python3 .agent/shared/tools/research_project.py check
paper:
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build paper/main.tex
site:
	python3 .agent/shared/tools/research_project.py site
	python3 .agent/shared/tools/research_project.py links .agent-runtime/site
