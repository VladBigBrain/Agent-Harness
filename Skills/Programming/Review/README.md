# Python review branch

`python-review` coordinates thirteen read-only, tool-independent reviewers. Every reviewer applies domain principles to source evidence, may consume normalized evidence inputs supplied by orchestration, emits the common proposed-finding contract, and ends with `mutations_performed: false`.

## Reviewers

| Skill | Lane | Primary evidence |
| --- | --- | --- |
| `object-oriented-review` | `oop` | responsibilities, invariants, dependencies, substitutability |
| `functional-review` | `functional` | mutation, side effects, repeated transformations |
| `async-review` | `async` | awaits, task lifecycle, cancellation, blocking work |
| `architecture-review` | `architecture` | declared boundaries, import graph, dependency direction |
| `types-contracts-review` | `types` | signatures, models, producer/consumer states, validation boundaries |
| `error-handling-review` | `errors` | reachable failures, cleanup, retries, translations |
| `tests-review` | `tests` | public behavior map, failure/edge scenarios, stability and confidence |
| `performance-review` | `performance` | critical path, complexity, allocation/I/O evidence |
| `style-review` | `style` | project rules, readability, naming, imports, formatting conventions |
| `code-simplifier-review` | `simplification` | duplication, dead paths, branches, needless layers |
| `security-review` | `security` | trust boundaries, attacker paths, controls, affected assets |
| `dependency-review` | `dependencies` | manifests, imports, versions, advisory availability |
| `api-docs-review` | `api-docs` | public interfaces, schemas, docs, examples, tests |

## Composition

Run architecture review separately from technological review, but normalize both through `python-review`. A no-finding result remains a persisted artifact with an empty `findings` list. Deduplicate only identical root causes; preserve disagreements and confidence. No reviewer may approve its own proposal, select an analyzer, execute a check, or invoke a fixer.

The reviewers contain only domain principles, questions, finding criteria, and the shared evidence/output boundary. Concrete analyzers, commands, versions, signal routing, licenses, and execution limitations live in `Tools/Feedback Loop` and the orchestration adapters.
