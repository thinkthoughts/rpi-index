# ETH cross-formalization comparison (RPI-378.2)

**State:** statement/provenance audit; **not** a new Lean kernel or Comparator run.

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

**Development ownership:** keep new OpenAI-to-Anthropic Lean glue in `thinkthoughts/math` (or a small independent comparison package if pinned Mathlib versions make that necessary). Leave `thinkthoughts/formal-math` close to upstream, and use this index as provenance and dependency metadata rather than a Mathlib build target.
