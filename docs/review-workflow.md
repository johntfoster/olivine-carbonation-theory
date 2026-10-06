# Review and editorial evidence workflow

These helpers support simulated independent AI peer review. They do not create
review verdicts, imply journal acceptance or verify scientific claims themselves.

## Freeze a candidate

Complete scientific checks and the explicit manuscript build first. Ensure
`build/main.pdf` corresponds to the source revision. Never freeze during an edit
or build: filesystem copying is not an atomic scientific working-tree transaction.

```sh
python3 scripts/freeze_review.py --round round-01
```

The explicit default allowlist is `paper/`, `verification/`, `scripts/`, `docs/`,
`GOAL.md`, `README.md`, `LICENSES.md`, `CITATION.cff`, `research-project.yml`,
`Makefile`, and `build/main.pdf`. All must exist. Include all scientific sources,
parameters, figures, data and reproduction requirements required to understand
that candidate; add any new directories explicitly before freezing:

```sh
python3 scripts/freeze_review.py --round round-02 \
  --include paper --include verification --include scripts --include docs \
  --include GOAL.md --include README.md --include LICENSES.md \
  --include CITATION.cff --include research-project.yml --include Makefile \
  --include build/main.pdf --include parameters --include data
```

Supplying `--include` replaces the complete default list; it does not append.
Private attachments, credentials, live sibling dependencies, symlinks, Git state
and other reviewers' reports must not enter the payload. Exclusion of `.agent`,
harness copies, `.agent-runtime` and `reviews` is enforced. Review inputs must be
self-contained and public-source provenance must use citations/hashes, not copied
private material. Inspect the manifest coverage before assigning reviewers.

Each new round creates `.agent-runtime/review-snapshots/<round>/` with the copied
source tree, PDF, sorted `MANIFEST.json`, and `SNAPSHOT_ID`. The ID is SHA-256 of
the exact manifest bytes. Every file is read-only; directories are mode 0555.
Existing round names are rejected. Read-only permissions are an accidental-edit
guard, not a security boundary against the filesystem owner.

Each reviewer independently recomputes the manifest digest and every payload
hash, reads only that snapshot, and writes only
`reviews/<round>/reviewer-N.md`. They must not see other reports or counts.
Reports state the round and snapshot ID, stable finding IDs, source locations,
and one final verdict: ACCEPT, MINOR REVISION, MAJOR REVISION, or REJECT.
All three reports must be complete and valid before counting exact ACCEPT votes.
Acceptance applies only to that exact immutable snapshot.

## Prose-only editorial cycles

Keep the pre-cycle snapshot. Compare it to the edited repository:

```sh
python3 scripts/check_editorial_invariants.py \
  .agent-runtime/review-snapshots/round-01 .
```

For each manuscript TeX file this checks structural-token counts, digit-literal
multisets, ordered SHA-256 math-block hashes, citations/labels/reference tokens,
and command-symbol multisets. File sets must match. Bibliographies, figures,
scientific verification/evidence/data/parameters and scripts must be byte-identical.
Non-TeX `paper/` payload is also protected. Cache bytecode is excluded.

This is deliberately conservative and is **not proof of unchanged claims**.
Manually audit the diff for assumptions, scope, qualifications and scientific
meaning. The regular expressions do not implement every TeX macro grammar.
After each cycle run the checker, perform the manual audit, and rebuild explicitly.
Record real outcomes; never substitute a fixture test for manuscript evidence.
Fresh post-editorial independent review is required if the accepted source changed.
