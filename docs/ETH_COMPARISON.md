# ETH cross-formalization comparison (RPI-378.2, RPI-378.3)

**RPI-378.2 state:** statement/provenance audit of the pinned sources (no Lean kernel or Comparator
run in this index). **RPI-378.3 state:** complete; see the RPI-378.3 sections below and `RPI-ETH-010`.

## Pinned sources

| Source | Commit | Role |
|---|---|---|
| `openai/math` | `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a` | Original #SAT proof |
| `thinkthoughts/math`, `eth-bridge/component-B` | `81ec97cd23d21675cee4ee76768fffba33a61e17` | VPS-verified `¬ PositiveRateETH` theorem |
| `thinkthoughts/formal-math` (Anthropic fork) | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | `MainResults` statements and Anthropic proof |
| `TSavo/eth-bridge` | `34f9ca204bed7fa6c595e56966773726e98dd3fd` | Third-party `Claim → ETHIsFalse` bridge |

The `thinkthoughts/math` documentation was inspected on branch head `81708f93fa4a4f72931ebf87aaefeaa602f85ab2`, which records the C2 verified commit above. These commits pin *sources*, not a common build environment.

## Endpoint distinctions

| Reading point | Exact formal endpoint | Machine and input | What it establishes |
|---|---|---|---|
| RPI-ETH-001 | `SqrtLogSpace.Claim` / published `MainTheorem` | Primitive multitape machine, canonical CNF encoding | Subexponential exact fixed-width #SAT (published comparator claim) |
| RPI-ETH-008 | `OAI.Bridges.ETH.not_positiveRateETH` | Converter into canonical input and polynomial-overhead machine simulation | `¬ OAI.ParityWL.Complexity.PositiveRateETH`; verified on project's VPS |
| RPI-ETH-002 | `MainResults.MainTheorem` | Mathlib `Turing.FinTM2`, `encInput` | Uniform k-CNF counting bound under explicit formula restrictions |
| RPI-ETH-003 | `MainResults.ethIsFalse` | FinTM2, `encClauses 3` | `¬ (0 < MainResults.s 3)` |
| RPI-ETH-004 | Standard ETH | Conventional deterministic models/encodings | Reference statement, not an independently checked Lean equivalence |

OpenAI's [bridge report](https://github.com/thinkthoughts/math/blob/81708f93fa4a4f72931ebf87aaefeaa602f85ab2/docs/ETH_BRIDGE_REPORT.md) specifies `PositiveRateETH` as an existential positive rate that rules out any finite-alphabet multitape solver with polynomial-input-length factor `C (L+1)^d 2^(δ N)`. The theorem `not_positiveRateETH` has no premises and was reported built using Lean 4.34.1 with axioms `[propext, Classical.choice, Quot.sound]`.

Anthropic's [`MainResults.lean`](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean) defines `ETH := 0 < s 3` and `ETHIsFalse := ¬ ETH`. Its comments explicitly note that ordinary machine/encoding simulation statements are outside the Lean proofs.

The third-party [bridge](https://github.com/TSavo/eth-bridge/tree/34f9ca204bed7fa6c595e56966773726e98dd3fd) reports:

```lean
Bridge.ethIsFalse_of_claim :
  OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.Claim →
  MainResults.ETHIsFalse
```

Its published reproduction discussion warns that OpenAI's source theorem was checked on Lean 4.34.1 while the bridge re-elaborated the same statement text with Anthropic's Lean 4.33.1 / Mathlib dependencies. That is an explicit cross-toolchain qualification, not a single composed kernel certificate for both upstream developments.

## Open proof/audit obligations

1. **Definitions.** Compare `PositiveRateETH` and `MainResults.ETH` at the actual type/quantifier level, not by their names.
2. **Input language.** Account for repeated clauses, empty clauses, literal order, all-variable-occurrence restrictions, and bit encodings.
3. **Machine simulation.** Identify polynomial or constant-factor overhead in both directions and exactly what `¬ PositiveRateETH` means relative to `¬ (0 < s 3)`.
4. **Asymptotics.** Distinguish OpenAI's formalized exponent from its paper's sharper bound and from Anthropic's two-term bound.
5. **Reproduction.** Check the bridge against a trusted statement, run `#print axioms`, record Comparator/nanoda evidence, and do not mark any new relationship locally reproduced until logs exist.

**Resolution (RPI-378.3).** For the direction `¬ PositiveRateETH → MainResults.ETHIsFalse`,
obligations 1–4 are discharged in Lean by `RPI-ETH-010` (definitions and quantifiers: Phase A
below; input language: the verified converter; machine simulation: the linear-time `FinTM2`
simulation; asymptotics: polynomial absorption). Obligation 5 is recorded below: axioms, the VPS
Comparator run (Lean kernel, nanoda disabled), and a separate standalone nanoda replay. Following
rule 2 of the registry, `local_status` stays `not_reproduced_here`. The converse direction remains
open.

**Development ownership:** keep new OpenAI-to-Anthropic Lean glue in `thinkthoughts/math` (or a small independent comparison package if pinned Mathlib versions make that necessary). Leave `thinkthoughts/formal-math` close to upstream, and use this index as provenance and dependency metadata rather than a Mathlib build target.

## RPI-378.3 Phase A: definition-level audit of `¬ PositiveRateETH → ETHIsFalse`

**State:** complete. Patches 1–4 (RPI-378.3a–d) in `thinkthoughts/math` are VPS-verified; the
unconditional implication is registered as `RPI-ETH-010` with the edge
`RPI-ETH-008 → RPI-ETH-003`. Existing IDs are unchanged.

### The two predicates, side by side

| | `OAI.ParityWL.Complexity.PositiveRateETH` | `MainResults.ETH` |
|---|---|---|
| Form | `∃ δ>0, ¬∃ M C d, 0<C ∧ SATTimeBound M (C(L+1)^d·2^{δN})` | `0 < s 3`, `s 3 = ⨅ {δ : InTime 3 δ}` |
| Negation | one machine per rate `δ` | `s 3 = 0`, i.e. `InTime 3 δ` for every `δ > 0`, one machine per rate |
| Machine | ParityLifts multitape: finite alphabet, two-way infinite tapes, local moves, input on tape 0, answer by an output state | Mathlib `FinTM2`: finitely many stacks, one step runs a whole statement, halts with output `[b]`, all other stacks empty, state reset (`haltList`) |
| Instances | any `List (Clause N)`, width ≤ 3 by type; repeated and empty clauses allowed | `IsKCNF 3`: width ≤ 3 and `Nodup` |
| Input word | `encodeFormula`: `N`, clause count, widths, literals in self-delimiting binary | `encClauses 3`: `1ⁿ0`, then 3 slots per clause of `⌊log₂ 2n⌋+1` bits, low bit first, slot `2i+1+b` |
| Time | `C (L+1)^d 2^{δN}`, `C : ℝ`, polynomial in input length `L` | `⌊c 2^{δn}⌋₊`, `c : ℕ`, in `n` alone |
| Rate type | `δ : ℝ` | `δ : ℝ≥0` |

### Findings

1. **Validity.** `¬ PositiveRateETH → ETHIsFalse` holds mathematically. The quantifier
   structures match (one machine per rate on both sides). Anthropic's instances form a subset of
   ParityLifts' instances, and `Nodup` gives at most `(2n+1)^3` clauses, so both input words have
   length polynomial in `n` and ParityLifts' `(L+1)^d` factor is absorbed into `2^{δ'n}` for every
   `δ' > δ`.
2. **Vacuity guard.** Both conclusions are proved theorems in their own repositories, so the
   implication becomes informative only through a proof that is checked to avoid both upstream
   proofs. RPI-378.3a enforces this with an import and constant-closure audit.
3. **Mathlib agreement.** `FinTM2`, `TM2.stepAux`, `initList`, `haltList` and
   `TM2OutputsInTime` are identical at Mathlib `0df444a3` (Anthropic) and `d13f23b7`
   (`thinkthoughts/math`); the files differ only in proof scripts. `MainResults.lean` imports
   Mathlib alone, so a byte-identical copy (SHA-256
   `47f78a9550d95b37d8718dd1ee16ae824da893a5e17c319f737e6d0a5ed24944`) elaborates under Lean
   4.34.1.
4. **What the TSavo bridge establishes.** `Bridge.ethIsFalse_of_claim` starts from OpenAI's
   single-machine `SqrtLogSpace.Claim`, models `PrimitiveMachine` as a `Groundwork.Stepped`
   computation, compiles it with Anthropic's `Groundwork.exists_tm` (the state size is kept
   polynomial by OpenAI's space bound), reaches `Sat3.SubexpTM`, and closes with
   `WidthThree.ethFails_of_subexpTM`. Its Anthropic imports form a 31-module closure separate from
   the 804-module `Solution` closure, a clean trust base.
5. **Why RPI-378.3 needs a different route.** `¬ PositiveRateETH` supplies a different machine
   for each rate and no space bound. `exists_tm'` bounds time by `q (T+1)(|x|+S+1)^q` with one `q`
   that fuses degree and coefficient per machine, so per-rate machines would give `T^{q_δ+1}` with
   `q_δ` uncontrolled. ParityLifts' `Machine.preprocess_run` instead has a degree
   (`preprocessingDegree`) independent of the machine, and a direct two-stacks-per-tape simulation
   costs linear time. RPI-378.3 therefore composes in the ParityLifts model and crosses into
   `FinTM2` once, linearly.
6. **What is new.** (a) A linear-time simulation of ParityLifts multitape machines by Mathlib
   `FinTM2`, a fact Anthropic's `ThreeSatRateStatement.lean` cites as standard and leaves
   unproved; (b) a front end from `encClauses 3` to `encodeFormula`; (c) the first implication
   between the two formal ETH predicates themselves.
7. **Placement.** Lean development in `thinkthoughts/math` under `OAI/Bridges/AnthropicETH/`
   (Lean 4.34.1, next to `preprocess_run`), with `MainResults.lean` vendored under
   `Vendor/Anthropic/`. `thinkthoughts/formal-math` stays identical to upstream.

### RPI-378.3 patch plan

| Patch | Content | Status |
|---|---|---|
| 378.3a | Conditional reduction: `SimulationHypothesis → ConverterHypothesis → ¬ PositiveRateETH → ETHIsFalse`; length bounds, absorption, quantifier transfer, `s 3 = 0` | VPS-verified (`dc6c4a900`, 8977 jobs); axioms `[propext, Classical.choice, Quot.sound]`; module and constant audits passed |
| 378.3b | `SimulationHypothesis`: ParityLifts `Machine` → Mathlib `FinTM2`, `≤ 4 (|x| + s + 1)` steps for every machine | VPS-verified (`0ddefa897`, 8981 jobs); axioms `[propext, Classical.choice, Quot.sound]`; strengthened audit passed |
| 378.3c | `ConverterHypothesis`: verified `PolyProgram` front end `encClauses 3 φ ↦ encodeFormula (toFormula φ)` via `Machine.preprocess_run`, degree `(convProgram.degree + 1) · preprocessingDegree` for every machine | VPS-verified (`beec4dc6b`, 8984 jobs); axioms `[propext, Classical.choice, Quot.sound]`; strengthened audit passed |
| 378.3d | Unconditional `not_positiveRateETH_implies_ethIsFalse : ¬ PositiveRateETH → MainResults.ETHIsFalse`; Comparator challenge (byte-for-byte trusted slices, byte-identical `MainResults.lean`); named-exclusion audit | VPS-verified (`d6b79b7d1`, 8985 jobs): dependency audit passed, axioms `[propext, Classical.choice, Quot.sound]`, Comparator exit 0 with the Lean kernel (nanoda disabled), `Your solution is okay!`; separately, standalone nanoda replay accepted in the harness. Registered as `RPI-ETH-010` |

Details of 378.3a: `docs/RPI-378.3a_REPORT.md` on branch `eth-bridge/rpi-378.3a` of
`thinkthoughts/math`.

A possible Phase C, the converse (`FinTM2` → ParityLifts, plus deduplication on
`encodeFormula`), would turn the edge into the equivalence `¬ PositiveRateETH ↔ ETHIsFalse`
between the two formal predicates.
