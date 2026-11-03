# RPI Index

Reading Point Identifiers (RPI) give stable IDs to *statements and relationships*, not just papers. One paper may have several RPIs, and one comparison may connect RPIs from different repositories.

The index is a cross-project catalogue for [formalize.now](https://formalize.now/). Lean proofs and source-specific builds stay in their owning repositories; the index records where to find them, what they claim, and what has actually been checked.

## First case: ETH / OpenAI-378 / Anthropic

See [`data/eth.json`](data/eth.json). It separates:

- OpenAI's published #SAT bound and our separately VPS-verified `¬ PositiveRateETH` bridge (RPI-ETH-008), with the formal predicate identified separately (RPI-ETH-009);
- Anthropic's #SAT main theorem and its formal `ETHIsFalse` statement;
- textbook ETH and the machine/encoding correspondences needed to interpret formal propositions;
- the independently developed OpenAI-to-Anthropic bridge, without treating a reported check as our own reproduction.

The nine initial IDs are provisional but stable; `RPI-ETH-010` records the VPS-verified implication from ParityLifts' `¬ PositiveRateETH` to Anthropic's `ETHIsFalse`. New readings should add evidence and edges rather than silently change the meaning of an existing ID.

## Validation

```sh
python3 scripts/validate.py
```

No dependencies beyond Python 3 are required. Validation checks identifier uniqueness, required fields, relationship targets and allowed evidence states. It does **not** kernel-check Lean code.

## Registry rules

1. One RPI refers to one precisely described reading point (theorem, reference proposition, or implication).
2. Separate `source_status` (what authors or third parties report) from `local_status` (what this project has reproduced).
3. Name the exact repository, path and declaration when available; add commit hashes as soon as source snapshots are pinned.
4. Record implications as directed edges. A mathematical implication is never silently promoted to an equivalence.
5. Do not promote a proof across Lean versions on source-text identity alone without recording the compatibility qualification.

Next: pin the remaining Anthropic and third-party source commits, compare elaborated declaration types, and attach build/axiom/Comparator logs to each verified edge.
