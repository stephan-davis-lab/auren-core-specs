# Contributing — AUREN Core Specs

**Adopted by the maintainer for the v2.5 release · 2026-10-10**

AUREN Core Specs publishes a declarative behavioral specification, its explanatory material and evaluation resources. Contributions can improve the specification, documentation, scenarios, integration guidance and separately licensed validation code.

Read the [Code of Conduct](CODE_OF_CONDUCT.md), [Safety guidance](SAFETY.md) and the repository's `README.md`, `NOTICE.md` and applicable license files before contributing.

## Useful contributions

Concrete counterexamples, clearer wording, translations, accessibility improvements, scenario proposals and corrections to validation tools are welcome. Propose the smallest change that addresses the identified problem. Changes to consent, mode priority, crisis routing, privacy, human responsibility or reference handling need an explicit explanation of their effect.

Repository policies govern collaboration and reporting. Operational AUREN requirements belong in the versioned Core YAML, within the host's governing instructions, safety policies, permissions and actual capabilities. Logic and Guidance explain or supplement that Core; adding text to a community document does not amend it.

## Classify the finding

| Finding | What to show |
|---|---|
| Specification error | Two requirements conflict, or a requirement produces an identifiable problem. Cite the relevant paths or sections. |
| Unclear rule | Show the competing reasonable readings and a concrete case in which the distinction matters. |
| Implementation deviation | Identify the applicable rule and the integration's observed departure from it. |
| Model behavior not yet reproduced | Preserve the observation and its limits. Describe what is missing before assigning a cause or claiming a reproducible defect. |

These categories guide investigation. An observation may concern more than one category, and uncertainty is not a reason to hide it.

Use a [public issue](https://github.com/stephan-davis-lab/auren-core-specs/issues) for non-sensitive findings. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community conduct, [SECURITY.md](SECURITY.md) for exploitable weaknesses, credentials or private data, and [SAFETY.md](SAFETY.md) for harmful or boundary-crossing AI behavior.

### Contact and reporting routes

The maintainer is **Stephan A. Davis**. The public project contact is [stephan@stephanadavis.de](mailto:stephan@stephanadavis.de).

| Concern | Reporting route | Suggested email subject |
|---|---|---|
| Community conduct | Report privately to the maintainer by email; follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). | `AUREN Core — conduct concern` |
| Harmful or boundary-crossing AI behavior | Use a public issue for a non-sensitive synthetic example, or email the maintainer privately for sensitive details; follow [SAFETY.md](SAFETY.md). | `AUREN Core — safety concern` |
| Technical security vulnerability, credentials or private data | Use the private GitHub form when available, or the email fallback below; follow [SECURITY.md](SECURITY.md). | `AUREN Core — security report` |

For technical security reports:

1. If GitHub shows **Report a vulnerability** in this repository's Security area, use that private reporting form.
2. Otherwise, contact **Stephan A. Davis** at [stephan@stephanadavis.de](mailto:stephan@stephanadavis.de), with a subject such as `AUREN Core — security report`.

Do not publish sensitive details in issues or pull requests. For email, begin with the minimum information needed; ordinary email does not promise end-to-end encryption. The linked policies explain their respective reporting scope and limits.

Overlapping concerns can be reported together; you do not need to diagnose them first.

## Make a report reviewable

Provide the information you actually have:

1. **Source identity:** release or candidate, affected file and section or YAML path; commit or computed package hash if available.
2. **Expected behavior:** the applicable requirement and its limits, in your own words or a short quotation.
3. **Observed behavior:** the smallest useful synthetic or redacted example, preserving the relevant context and actual output.
4. **Delivery method:** distinguish a real exchange across turns from a transcript supplied inside one message. Identify actual message roles and loaded instructions where known.
5. **Environment and limits:** host, adapter and displayed model selection; report internal model ID, memory, retrieval or tool configuration only when actually known. Mark unknown values as unknown.
6. **Reproduction and proposal:** attempts made, differing results, possible impact and the smallest proposed correction.

Do not include passwords, access files, personal profiles or unredacted private screenshots. An authored scenario is an expected-behavior definition, not evidence that a model passed it. A proposed prompt is not an observed response.

## Propose a change

Open a focused issue or pull request explaining the problem, resulting behavior, affected files and relevant checks. For a larger architectural change, discuss its scope before preparing a large patch. Separate unrelated changes so each can be assessed.

Keep Core, Logic, Guidance, integration explanations and scenarios consistent when a requirement changes. Linked pages remain optional context; they must not silently become runtime instructions or automatic updates to the local Core.

AI assistance is welcome when you verify its sources and results. Do not present generated evidence as an executed test or call a review independent when its author also prepared or substantially shaped the reviewed material. Explain relevant dependencies without exposing private data.

## Verification and evidence

Use the checks documented for the exact version or candidate you are changing. Static validation can establish structure, paths and recorded byte identity; it cannot certify model behavior or the correctness of a semantic judgment.

Choose behavioral checks for the changed claim or integration. A change affecting ambiguous consent or interpretation scope should include relevant T03/T23 checks and appropriate allowed-behavior controls such as T25, T35 or T42. Do not generalize one integration's results to other hosts or models.

Editorial, community-policy and release-status changes do not automatically require a new full model test series. They still need appropriate consistency, link, license and packaging checks. An actual operational change may require targeted tests or a broader suite, depending on its effect.

Retain failed and inconclusive observations alongside later checks. Do not rewrite history, invent a root cause or claim a new model run for a static comparison. Keep evaluation scenarios, expected answers and audit originals separate from the operational context of a model under test.

Frozen candidates and completed reviews remain immutable. A changed candidate or publication package needs a new identity and the affected checks or reviews. Maintainer acceptance and a human release decision are distinct from a model's review verdict.

## Rights and acceptance

Submit only material you may contribute. The Core specification, Logic, Guidance, authored scenarios and repository documentation use **CC BY-SA 4.0**. Validator code uses its separate **MIT** license. Preserve existing attribution and file-specific licensing; identify third-party material and its applicable rights.

Contributions offered for inclusion in this CC BY-SA 4.0 material are submitted under CC BY-SA 4.0; contributions to files covered by the validator's MIT license are submitted under that MIT license. This applies to submissions through GitHub and other channels. By submitting material for inclusion, you confirm that you have the necessary rights and agree to its distribution under the applicable license. Identify third-party material or different terms before inclusion; they must be compatible with the affected material's license. This statement concerns material offered for incorporation into the project, not every message or private report.

Links to concepts, methods, websites or brands do not license the complete referenced material. Consult `NOTICE.md` for the repository's scope. Contributions do not imply transfer of your copyright to the maintainer.

The maintainer decides what enters the official repository. This contribution process does not add restrictions to reuse or adaptation permitted by the applicable licenses, and reuse does not imply official endorsement.

---

Copyright © 2026 Stephan A. Davis. This document is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
