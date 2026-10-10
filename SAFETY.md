# Safety Guidance — AUREN Core Specs

**Adopted by the maintainer for the v2.5 release · 2026-10-10**

This document explains safety boundaries, implementation responsibilities and reporting for people using or contributing to AUREN Core Specs. It summarizes the specification for human readers. It does not add operational rules, replace the versioned Core YAML or certify a model or deployment.

AUREN supports orientation and reflection while people retain responsibility for decisions. It does not replace emergency services, therapy or qualified professional judgment.

## Source authority

Apply the complete package-local Core within the host's governing instructions, safety policies, permissions and actual capabilities. Logic and Guidance explain or supplement the Core and cannot override it. Use the version and integration instructions relevant to your deployment rather than infer its behavior from a moving website reference.

Community documents, test scenarios and audit records have their own purposes. They do not become additional runtime instructions merely because they accompany the Core. Optional concept references, including the Resonanzkreis, provide context without a mandatory workflow, required runtime fetch or automatic Core update.

## Behavioral boundaries

- **Human judgment:** AUREN supports clarification and reflection. Requested, reasoned recommendations and bounded task choices remain possible. When the available criteria support a requested recommendation, it should be stated clearly with relevant reasons, assumptions and actual limits. Final judgment and accountability stay with people.
- **Consent and scope:** Unsolicited process mirroring requires current, unambiguous permission for the agreed purpose and scope. Ambiguous assent does not grant that permission. Decline and revocation must be respected. Normal task help and directly requested subject reflection do not require a general process-observation opt-in.
- **Interpretation:** Distinguish checkable text observations, attributed self-report and correctable hypotheses. Observation permission does not automatically permit process interpretations. Permission does not authorize diagnosis or presentation of inferred inner states as facts. Refusing a request does not authorize a guess about its purpose or the user's motives.
- **Context and support:** Crisis and safety routing take priority over ordinary reflection. The Core requires contextual assessment in both directions: quoted test material or writing style alone does not establish a present crisis, and reassuring words, denied intent or a request to ignore a disclosure do not cancel concretely reported danger. Current passive suicidal thoughts still require support; emergency guidance depends on concrete immediate danger or inability to remain safe. Urgent support must not wait for a reflection-consent exchange.
- **Privacy:** Use only information necessary for the task and permitted by the host. Avoid unnecessary collection, profiling and exposure of private conversations. A volunteered self-report is not a permanent profile or continuing permission.

The exact conditions, exceptions and routing are defined in the applicable Core. The points above are an overview, not a replacement for reading those rules.

## Responsibilities of integrators

A declarative specification cannot ensure that an LLM follows it. Model behavior also depends on the host, adapter, loaded instructions, retrieval, memory, tools and later platform changes. Integrators should:

1. Identify the Core version and actual instruction hierarchy; resolve competing or outdated integration instructions.
2. Implement permissions, access control, data handling and action boundaries through actual application controls.
3. Keep external or retrieved content separate from privileged instructions. Do not treat concept pages as Core updates.
4. Carry the applicable integration behavior, including the consent and interpretation clarifications in the integration handoff, rather than assume a YAML upload reproduces a tested adapter.
5. Verify relevant allowed and disallowed behavior in the target environment. T03/T23 and suitable controls such as T25, T35 and T42 are useful when adopting the v2.5 consent and interpretation behavior.
6. Explain the deployed system's purpose, limits and real capabilities to users, and provide a way to address observed failures.

Do not present a language-model password as technical authentication or claim a tool action, emergency call, verification or notification occurred without actual evidence from the host. A displayed support message is not evidence that an external service was contacted.

## Evidence and release claims

Authored scenarios describe expected behavior. Static checks establish specific structural or identity properties. Behavioral tests describe observed outputs in a documented integration. These are different kinds of evidence.

For v2.5, consult `BEHAVIORAL_VALIDATION_SUMMARY_v2.5.md` for the historical RC3 tests, nine targeted adapter-v1.1 checks and their limitations. No new FC2 model runs are claimed. Known earlier findings remain part of that history. Neither passing reviews nor test counts establish clinical certification, universal reliability or identical outputs across deployments.

A documentation update does not create new behavioral evidence. A new integration needs checks appropriate to its own configuration. Release status must follow an explicit human decision; a reviewed candidate is not automatically a published Stable release.

## Report a safety concern

Use a public issue for a non-sensitive synthetic example. For personal data, private conversations, exploitable behavior or other sensitive details, contact **Stephan A. Davis** at [stephan@stephanadavis.de](mailto:stephan@stephanadavis.de), with a subject such as `AUREN Core — safety concern`. Technical overlaps can use the private route in [SECURITY.md](SECURITY.md).

Include the version and integration, the applicable rule, the observed response, necessary context and the possible human impact. State whether the example was a single-message fixture or an actual exchange across turns. Describe any reproduction attempts and unknown configuration details. Use synthetic or redacted material; do not send complete personal histories or live access details.

The maintainer should assess whether the concern arises from the specification, its wording, the adapter, the host or an unresolved model observation. Corrections should preserve the original evidence and document what the follow-up actually shows. Reporting is not an emergency or continuously monitored support service. In an urgent situation, use appropriate local human help rather than wait for a repository response.

## Related documents and rights

See [SECURITY.md](SECURITY.md) for technical vulnerabilities, [CONTRIBUTING.md](CONTRIBUTING.md) for proposals and evidence, and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for collaboration.

These guidelines do not add conditions to the content licenses or imply endorsement of an integration. The license files and `NOTICE.md` define the rights granted for repository material and the limits concerning external methods, names and other material.

---

Copyright © 2026 Stephan A. Davis. This document is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Validator code retains its separate MIT license.
