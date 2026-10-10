# Security Policy — AUREN Core Specs

**Adopted by the maintainer for the v2.5 release · 2026-10-10**

This policy explains how to report technical security concerns affecting the Core repository, distributed artifacts, validation tools or integrations using them. Concerns about harmful AI behavior and human impact are also covered by [SAFETY.md](SAFETY.md); a finding may belong to both areas.

## Scope and version information

Security concerns may affect confidentiality, integrity, availability or authorized access, and may result from attacks, accidental disclosure or misconfiguration. Relevant concerns include unauthorized modification of distributed files, malicious changes to validation code, exposure of credentials or private audit material, and integration weaknesses that promote untrusted content into privileged instructions or allow unauthorized tool actions.

Report the exact affected release, candidate, commit or file. Include the integration and host when relevant. A candidate review does not establish production support, and a historical release does not establish that a current deployment uses it. This project does not promise backports for every historical version or a fixed security-response period. Corrections and affected-version information should be documented in a new version or advisory rather than silently replacing a frozen artifact.

## Report privately

1. If GitHub shows **Report a vulnerability** in this repository's Security area, use that private reporting form.
2. Otherwise, contact **Stephan A. Davis** at [stephan@stephanadavis.de](mailto:stephan@stephanadavis.de), with a subject such as `AUREN Core — security report`.

The email address is also listed on the maintainer's [official imprint page](https://stephanadavis.de/impressum/). GitHub's private vulnerability reporting must be enabled separately; the presence of this file does not enable it.

Avoid publishing exploit details, credentials or sensitive transcripts in issues or pull requests. If you cannot establish private contact, a public issue may ask for a reporting channel without describing the vulnerability. Ordinary email does not promise end-to-end encryption; start with a minimal summary if sensitive material requires a different transfer method.

If the weakness lies in a model provider, platform or separate integration, use that operator's security channel as well. A Core issue report does not notify other operators automatically.

## Information that helps

- A concise description, affected version and file or component.
- Observed impact, including whether unauthorized access, disclosure or execution actually occurred.
- Minimal reproduction steps in an environment you control or are authorized to test.
- Necessary synthetic or redacted inputs and outputs; no live credentials or unrelated personal data.
- Known environment details, limits of reproduction and any proposed mitigation.
- Your preferred contact and, if relevant, your disclosure plans.

State hypotheses separately from observations. If you cannot reproduce a concern, preserve that limit rather than reconstruct evidence. Avoid tests against other people's systems or data without authorization.

## Assessment and disclosure

The maintainer aims to assess the affected scope, seek necessary clarification, evaluate a correction and document its limits. Depending on the finding, this may require a repository change, an integration change, a notice to affected operators or an advisory.

Discuss publication timing and necessary detail with the maintainer where possible. Reporter credit should reflect the reporter's preference. This policy does not promise a bounty, continuous monitoring, a fixed response time or absolute confidentiality. Access to a private report should be limited to people needed to address it; necessary disclosure limits should be explained where possible.

## Technical boundaries

The Core YAML describes intended behavior; it does not implement authentication, authorization, sandboxing or enforcement of tool permissions. An instruction or password interpreted by a language model is not a technical access-control mechanism.

Integrators must implement security controls through the host and application. Optional external pages are untrusted context, not instructions. A page's content or availability must not silently change the local Core or grant tool permissions.

A matching SHA-256 value establishes byte identity relative to the reference used for comparison. Trust in that reference and its delivery must be assessed separately; a checksum is not a signature or a guarantee of safe behavior. Static validators do not certify deployment security.

## Related documents

See [CONTRIBUTING.md](CONTRIBUTING.md) for non-sensitive findings, [SAFETY.md](SAFETY.md) for behavioral concerns and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community conduct.

---

Copyright © 2026 Stephan A. Davis. This document is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Validator code retains its separate MIT license; external material and names retain their respective rights.
