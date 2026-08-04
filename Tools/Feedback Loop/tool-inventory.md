# Tool inventory and selection

Inventory reviewed on 2026-08-04. The harness-local tested versions are Ruff 0.16.1, Mypy 1.20.2, Pytest 8.4.2, Bandit 1.9.4, Radon 6.0.1, and PyYAML 6.0.3. Target-native versions are still used when repository configuration requires them.

| Tool | Selection and consumer | Maturity signal | License | Limits |
| --- | --- | --- | --- | --- |
| [Ruff](https://docs.astral.sh/ruff/) | Selected for project-configured lint and format checks; style, simplification, performance, error, and verification consumers | Maintained by Astral, broad rule set and established project adoption | [MIT](https://github.com/astral-sh/ruff) | Version/rule behavior changes; runner uses target version/config and never `--fix` |
| [Mypy](https://mypy.readthedocs.io/) | Selected for static type/contracts evidence | Long-running typed-Python checker with current documentation | [MIT](https://mypy.readthedocs.io/en/stable/faq.html) | Diagnostics can reflect missing stubs/import setup; not runtime proof |
| [Pytest](https://docs.pytest.org/) | Selected for public-interface and regression checks | Established Python test framework; already configured by target | [MIT](https://docs.pytest.org/en/stable/license.html) | Executes project/plugin code; may require services or credentials, so run only authorized local tests |
| [Bandit](https://bandit.readthedocs.io/en/latest/) | Selected as local AST security signal for `security-review` | PyCQA security analyzer with JSON output | Apache-2.0 | Common-pattern detector only; false positives/negatives require source validation |
| [Radon](https://radon.readthedocs.io/en/stable/commandline.html) | Selected for cyclomatic-complexity evidence | Stable 6.x command interface | MIT | A metric is not a finding and cannot establish performance impact |
| `architecture-cycles` | Selected original stdlib adapter for imports in the explicit source root; architecture reviewer | Deterministic, covered by harness tests | Original harness code | Detects static Python import cycles, not dynamic imports or policy boundaries |
| Target architecture tests | Selected when present; architecture and verification consumers | Repository-owned executable contract | Target-project license | Only proves encoded boundaries and executes project code |
| Codex Security | Selected primary security reasoning capability; orchestration routes its output to the security lane | Built-in Codex security workflow | Service capability; no copied code | No standalone CLI; orchestration must persist and normalize its output |
| [pip-audit](https://github.com/pypa/pip-audit) | Candidate, unavailable in the isolated demonstration | PyPA-maintained dependency advisory client | Apache-2.0 | Advisory services/resolution can require network or private-index access; official security model warns resolution is installation-equivalent |
| [SonarQube/SonarScanner](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/scanner-environment/general-requirements) | Candidate, unavailable in the isolated demonstration | Mature server/scanner platform; target already contains `sonar-project.properties` | Edition/component-specific; no code copied | Requires a compatible scanner/server and often credentials/network; configuration presence is not an executable check |

## Minimal composition

Use target-native Ruff, Mypy, and Pytest first. Add the local AST cycle adapter, Radon, and Bandit as non-authoritative evidence. Route security reasoning through Codex Security. The adapter configuration, not reviewer prose, owns which lanes receive each normalized signal. Do not add import-linter while the target already has architecture tests and the deterministic cycle adapter; revisit it only when explicit dependency contracts need a dedicated engine. Keep pip-audit and Sonar unavailable until safe network/server prerequisites are approved.
