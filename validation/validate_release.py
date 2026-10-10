#!/usr/bin/env python3
"""Read-only Stable v2.5 package checks; no network, writes or model calls.
Copyright (c) 2026 Stephan A. Davis. SPDX-License-Identifier: MIT
"""
from pathlib import Path, PurePosixPath
from copy import deepcopy
import argparse
import hashlib
import json
import re
import sys
import zipfile
import yaml
from yaml.constructor import ConstructorError

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
CONFIG = {'fixed': {'core_body': '71ef4c028b6e0cd90ddc9c4569067bb7322214b46230136c0f75ea397738682c', 'core_text_after_release': 'cc9f8d321647da19c1b559f5eedace2f52674aeec550f350aca72d2c3c465a9f', 'logic_body': 'e7345248d735795ee7e79cff0ad44069ca67a1b77603656a4cfb1ad036f52cec', 'guidance_rules_excluding_status_prepared_on_and_official_release': '4156a7dfdeb851164cb10701b69c01df472d3ccad20d0a95f8ecd2a2e2d58ed8', 'adapter_body_excluding_single_status_sentence': 'd1f25744febee3b9bad5559ad34f68f42a419c35cd490731b7f175de82a304d2', 'scenario_yaml': '5a49e67b0a8c9e042022091afefad0cc06c1288efc43f1b707c39eb606b1d6f8', 'scenario_markdown': 'a471fcf4f9c8320e1045794d79a51bd36c70626e7669ac0bacbb1eda3c18cb93', 'cc_legal_code': '28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5', 'mit_license': '0e070fa80969201ae436b9f2c0d0d6d6899d00821b8a79041cc2b4a9a69095b5'}, 'policies': {'CODE_OF_CONDUCT.md': {'reviewed_r1_sha256': '0248536004e3a62aec22978d3fc947d9171650b60c0692dbc4e858932e69107b', 'body_without_status_sha256': '25808ac5c229eb5b42a9fe7fd6d0b0784979f02e0a9af72d55299b49762da3eb'}, 'CONTRIBUTING.md': {'reviewed_r1_sha256': '0c9501c2495f969dc86e22d7f9dd0c8f92a6ccacac490fdb5be0a3c852c9f05a', 'body_without_status_sha256': '1d2093e454c25e423eb7eb5e4d2b62d6775d9e68d38a61e174add339205b2d2a'}, 'SECURITY.md': {'reviewed_r1_sha256': '68b5ada36d919e5e51d53a2fc221ee8c196585c44ed2c3eed239a4ddd9d76b12', 'body_without_status_sha256': '8952a1e09c7b4aa349b9fd97793c1b74a3ceac44e32d453453b4c98e4a5b2ae2'}, 'SAFETY.md': {'reviewed_r1_sha256': '4ea29683411ce6dd94d5ca87761b163ca91982a3876c9a05fa56adbd6255fc47', 'body_without_status_sha256': 'e4a5849f450626b1de6f8aa3e57fd9dc5c9d902fb35fc87ddbae05d277ce0aff'}}, 'preserved_repository': {'auren-core-specs_v2.4.yaml': '990c83356a1465a059d6e518c11e28eaa870a6ae1592d6dc60b28694040da475', 'auren-core-logic_v2.4.md': 'ddd80e6eb6ea9f08b5a47ec6c65e15e7b6dff02beeacce210bc0ee9e30847092', 'Guidance4AIsystems_v2.4.txt': '7fdb7d8032de00a41b4d585887cbd025c840e24f17b1a303f8d8c9a9d7454761', 'exports/auren-core-specs_v2.4.yaml.txt': '990c83356a1465a059d6e518c11e28eaa870a6ae1592d6dc60b28694040da475'}, 'immutable_fc2': {'evidence/fc2/SOURCE_AND_SCOPE_at_freeze.json': '07528d87ccab1aebbd968e757b4eb6f3f32e8cc168cd4ff282980f597f71149e', 'evidence/fc2/RELEASE_GATES_at_freeze.json': '5e3882c57f7fff396c489d09c830c84b01cfcb4cea581a46e329c9a902c808ce', 'evidence/fc2/static-results_at_freeze.json': '2aa8c72c81b811e39dafb1b8342add5bcb6cf6c7938194a4c16137b529cb04aa', 'evidence/RESONANZKREIS_REFERENCE_ADDITION_FC2.md': '66fd321fc9224d70da51dbade0dbc5f0a4b0ca619a8e819c0a5af4fa4a5fe3a9', 'evidence/SAFETY_CALIBRATION_SOURCES_v2.5-rc3.md': 'a0ddc43ee174ba4eee0f8e9fa89231c3f4ae3bae1f9237fbaaa4e0d16900e44e', 'evidence/fc2/CHANGELOG_at_freeze.md': '211536df0501de3bea125225d932e3100b2275eb745a60120e25a97961339a55', 'evidence/previous_preparation/FC2_and_documents_R1_to_preparation_at_freeze.diff': '052b7085f1a4f08905f5395bfacfc614bece08af47f9691ade7e42cac3f48508', 'evidence/preparation_R1/RELEASE_STATUS_at_freeze.json': 'a618aecc5daa12da8c48187c5475a5be93a26d767ff5f4eefdf527f62373cdba', 'evidence/preparation_R1/SOURCE_AND_SCOPE_at_freeze.json': '66dc2ea6bd350d6893f860c488094181cb3017a8a2d0ea497ded1518320f73f9', 'evidence/preparation_R1/CHANGELOG_at_freeze.md.txt': '2686c2c0b0f78080bf759ce4109a0cba131b160aaf8ac519e2970e81f4a5bd53', 'evidence/preparation_R1/static-results_at_freeze.json': 'a26f2cbc894d281dfecd67efc8861e19e3e2e7f60616d8378b469ed59ef40225'}, 'source_hashes': {'public_FC2_sha256': '4461a67a69e9a242fd861282b3c5dc1d8999764d31205c564512eea7c9da9f59', 'internal_R1_sha256': '52ff0b91d34fe81bfd42021437271515da12abcca80ad9d33455dbe517808888', 'repository_documents_R1_sha256': 'a05dc4b1b75b87caab78d73d01f09ddd50e7dd7ff03960215f547c100e9363af'}, 'expected_release': {'status': 'stable', 'target_version': '2.5', 'prepared_on': '2026-10-10', 'baseline_version': '2.4', 'publication_status': 'not_published', 'behavioral_validation_status': 'documented_integration_runs_with_targeted_adapter_correction', 'external_currentness_checked': False, 'purpose': 'stable_release_of_reviewed_core', 'previous_candidate': '2.5-FC2', 'external_check_scope': 'prior_selected_safety_guidance_plus_single_resonance_reference_page_no_full_external_audit', 'source_final_candidate_id': 'FC2', 'release_preparation_id': 'v2.5-PUBLISH-PREP-R1-20261010', 'final_reviews_status': 'pass_on_frozen_FC2_and_Internal_R1', 'human_release_decision': 'approved', 'behavioral_evidence_scope': 'BEHAVIORAL_VALIDATION_SUMMARY_v2.5.md', 'status_snapshot': 'stable_approved_at_package_freeze; live_publication_and_deployment_not_asserted', 'approved_on': '2026-10-10', 'release_package_id': 'v2.5-STABLE-20261010'}, 'expected_report_hashes': {'AUREN_v2.5_FC2_R1_AUREN_Recheck_2026-10-09.md': 'a55f3a0c1ad9b754f0d93aa3d23d9e9c4416f6173dce7ce4f72f6420d3de2878', 'AUREN_v2.5_FC2_R1_ChatGPT_Gegenpruefung_2026-10-09.md': 'a238214698561903bd4e62b07b0fa8f4430b503c5966268a07afd88d9d8a7fb7', 'AUREN_v2.5_FC2_R1_Claude_FinalChallenge_2026-10-09.md': 'd0aef5566ff4bbcac5b03bc10d4ccc0701f98af32001d14ada36331809d1c942', 'AUREN_Core_v2.5_Begleitdokumente_R1_AUREN_Recheck_2026-10-10.md': '1575dcc5ec30c35aebd865647cfa047b7a05ace41079fbb80eaaf75487b49eda', 'AUREN_Core_v2.5_Begleitdokumente_R1_Recheck_Claude_2026-10-10.md': 'e278216ab2fdd54fbee7ca5847696e415cc9561a86f310399d3e25f646925d7f'}, 'guidance_metadata_paths': ['status', 'prepared_on', 'validation.official_release', 'source_hierarchy.context'], 'old_adapter_status': 'Behavioral evidence is integration-specific; final reviews and Stable clearance remain open; never claim release or certification.', 'prepared_adapter_status': 'Behavioral evidence is integration-specific. Reviews of frozen FC2 + Internal R1 are complete; Stable v2.5 was approved by the maintainer on 2026-10-10. This records package-freeze status; do not infer publication, deployment or certification.', 'prepared_policy_header': '**Adopted by the maintainer for the v2.5 release · 2026-10-10**\n', 'draft_policy_header': '**Draft for maintainer review · 2026-10-10 · Not yet adopted**\n', 'preparation_id': 'v2.5-PUBLISH-PREP-R1-20261010', 'prepared_full_file_hashes': {'auren-core-specs_v2.5.yaml': '5312902111108831a259034a48af93b459a90eaa4364f5f7076ef1ff9a4fba9c', 'auren-core-logic_v2.5.md': 'e2335c3bb91069267e3f9bce0d40f3b61e0f02135d2c5b08bcb16758b82aa3ee', 'Guidance4AIsystems_v2.5.txt': 'a1bbd868eeb2af8fd13df41dcc333a2fdd012d0c9d0e37eef5d375a27158deee', 'INTEGRATION_HANDOFF_v2.5.md': '038ac5b4d035985048c56b2ec16f7a0ac9d0c782a7e1591e99154460bb7643db'}, 'guidance_context_path_change': {'from': 'README_v2.5.md', 'to': 'README.md'}, 'notice_expected_sections': {'Excluded material': 'bb4b1cd4b1eb0fe77a6c264e407f7d496f68c4799f786a99b4cf6549460e975d', 'Names, marks, and endorsement': '8a36837a01c2029305c743a3b784478bd64add10257f4e0b7198e5a0aac454f9'}, 'expected_reporting_configuration': {'repository': 'stephan-davis-lab/auren-core-specs', 'checked_on': '2026-10-10', 'private_vulnerability_reporting': 'enabled_in_repository_ui', 'secret_protection': 'enabled_in_repository_ui', 'push_protection': 'enabled_in_repository_ui', 'notification_channels': ['GitHub', 'Email'], 'watch_events': ['Issues', 'Security alerts'], 'watch_saved_confirmation': 'maintainer_confirmed_in_chat', 'evidence_scope': 'screenshots_read; repository_subscription_save_confirmed_by_maintainer; no_setting_changed_by_Codex', 'report_submission_test': 'not_performed', 'notification_email_delivery_test': 'not_performed', 'public_security_policy': 'included_in_approved_stable_package; remote_publication_not_verified'}, 'expected_policy_adoption': 'confirmed_for_v2_5_release_in_maintainer_chat', 'expected_reporting_confirmation': 'configured_in_repository_ui_and_confirmed_by_maintainer', 'contribution_reporting_change': {'from': 'Use a public issue for non-sensitive findings. Follow [SECURITY.md](SECURITY.md) for exploitable weaknesses, credentials or private data. Follow [SAFETY.md](SAFETY.md) for harmful or boundary-crossing AI behavior. Overlapping concerns can be reported together; you do not need to diagnose them first.', 'to': "Use a [public issue](https://github.com/stephan-davis-lab/auren-core-specs/issues) for non-sensitive findings. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community conduct, [SECURITY.md](SECURITY.md) for exploitable weaknesses, credentials or private data, and [SAFETY.md](SAFETY.md) for harmful or boundary-crossing AI behavior.\n\n### Contact and reporting routes\n\nThe maintainer is **Stephan A. Davis**. The public project contact is [stephan@stephanadavis.de](mailto:stephan@stephanadavis.de).\n\n| Concern | Reporting route | Suggested email subject |\n|---|---|---|\n| Community conduct | Report privately to the maintainer by email; follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). | `AUREN Core — conduct concern` |\n| Harmful or boundary-crossing AI behavior | Use a public issue for a non-sensitive synthetic example, or email the maintainer privately for sensitive details; follow [SAFETY.md](SAFETY.md). | `AUREN Core — safety concern` |\n| Technical security vulnerability, credentials or private data | Use the private GitHub form when available, or the email fallback below; follow [SECURITY.md](SECURITY.md). | `AUREN Core — security report` |\n\nFor technical security reports:\n\n1. If GitHub shows **Report a vulnerability** in this repository's Security area, use that private reporting form.\n2. Otherwise, contact **Stephan A. Davis** at [stephan@stephanadavis.de](mailto:stephan@stephanadavis.de), with a subject such as `AUREN Core — security report`.\n\nDo not publish sensitive details in issues or pull requests. For email, begin with the minimum information needed; ordinary email does not promise end-to-end encryption. The linked policies explain their respective reporting scope and limits.\n\nOverlapping concerns can be reported together; you do not need to diagnose them first."}, 'reporting_email': 'stephan@stephanadavis.de', 'package_id': 'v2.5-STABLE-20261010', 'parent_preparation_sha256': '886307f975d759d30af9b3ad56d3a79ed37d29e7e6ed68ce53aadfab90a3f8dd', 'approval_record_path': 'evidence/STABLE_APPROVAL_AND_REPORTING_UPDATE_2026-10-10.md', 'approval_record_sha256': 'd65c8dbc5d3aa3795abb17b188a42ff5a2cb97640248619741e03611740455dd'}


class UniqueLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in result:
                raise ConstructorError('mapping', node.start_mark, 'duplicate key: ' + str(key), key_node.start_mark)
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def refs(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.endswith('_ref'):
                yield child
            if key.endswith('_refs'):
                require(isinstance(child, list), 'reference list expected')
                yield from child
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def resolve(value, path):
    require(isinstance(path, str), 'reference path must be text')
    for part in path.split('.'):
        require(isinstance(value, dict) and part in value, 'unresolved reference: ' + path)
        value = value[part]
    return value


def guidance_body(value):
    value = deepcopy(value)
    value.pop('status')
    value.pop('prepared_on')
    value['validation'].pop('official_release')
    require(value['source_hierarchy']['context'] == CONFIG['guidance_context_path_change']['to'], 'unexpected Guidance context path')
    value['source_hierarchy']['context'] = CONFIG['guidance_context_path_change']['from']
    return value


def adapter_excerpt(text):
    require(text.count('```text\n') == 1, 'exactly one public adapter excerpt expected')
    return text.split('```text\n', 1)[1].split('\n```', 1)[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pre-freeze', action='store_true', help='skip checks for the result record and manifest before they exist')
    parser.add_argument('--baseline-fc2', type=Path, help='read the exact frozen Public FC2 ZIP for direct comparisons')
    args = parser.parse_args()
    results = []
    cache = {}

    def check(name, fn):
        try:
            results.append({'check': name, 'status': 'pass', 'detail': fn()})
        except Exception as exc:
            results.append({'check': name, 'status': 'fail', 'detail': str(exc)})

    def load():
        for key, path in [('core', 'auren-core-specs_v2.5.yaml'), ('guidance', 'Guidance4AIsystems_v2.5.txt'), ('suite', 'evals/scenarios_v2.5.yaml')]:
            cache[key] = yaml.load((ROOT / path).read_text(encoding='utf-8'), Loader=UniqueLoader)
        cache['status'] = json.loads((ROOT / 'RELEASE_STATUS_v2.5.json').read_text(encoding='utf-8'))
        cache['scope'] = json.loads((ROOT / 'SOURCE_AND_SCOPE_v2.5.json').read_text(encoding='utf-8'))
        return 'Three YAML documents parsed with duplicate-key rejection; current metadata parsed.'

    check('parse_unique_yaml_and_current_metadata', load)
    if len(cache) != 5:
        return output(results, args)
    core = cache['core']['auren_core_spec']
    guidance = cache['guidance']['orientation_framework']
    suite = cache['suite']
    status = cache['status']
    scope = cache['scope']
    fixed = CONFIG['fixed']

    def identities():
        require(core['version'] == guidance['version'] == suite['suite_version'] == '2.5', 'version mismatch')
        require(core['release'] == CONFIG['expected_release'], 'Core release metadata is outside the exact Stable package definition')
        require(status['preparation_id'] == scope['preparation_id'] == CONFIG['preparation_id'], 'source preparation identity mismatch')
        require(status['package_id'] == scope['package_id'] == CONFIG['package_id'], 'Stable package identity mismatch')
        require(status['release_id'] == scope['release_id'] == status['release_tag'] == 'v2.5', 'public version or tag mismatch')
        require(status['source_preparation_sha256'] == scope['sources']['publication_preparation_R1_sha256'] == CONFIG['parent_preparation_sha256'], 'source preparation hash mismatch')
        require(status['reviewed_sources'] == CONFIG['source_hashes'], 'reviewed source objects changed')
        require(all(scope['sources'][k] == v for k, v in CONFIG['source_hashes'].items()), 'provenance source identity changed')
        return 'Stable version/tag v2.5, package identity and frozen source identities aligned.'

    check('exact_preparation_metadata_and_source_identities', identities)

    def core_identity():
        body = deepcopy(core)
        body.pop('version'); body.pop('release')
        require(sha(canonical(body)) == fixed['core_body'], 'full FC2 normative Core body changed')
        raw = (ROOT / 'auren-core-specs_v2.5.yaml').read_bytes()
        require(raw.count(b'  specification_contract:') == 1, 'Core text anchor ambiguous')
        require(sha(raw.split(b'  specification_contract:', 1)[1]) == fixed['core_text_after_release'], 'Core text after release metadata changed')
        require(core['model_references']['optional'] is True, 'model references no longer optional')
        require(core['model_references']['concepts']['resonance_cycle']['reference']['url'] == 'https://stephanadavis.de/perspektivensystemik/resonanzkreis/', 'reference changed')
        return 'Full Core semantic hash and unchanged text after the release block match FC2, including Resonanzkreis.'

    check('full_core_rules_and_text_preserved', core_identity)

    def guidance_identity():
        require(guidance['status'] == 'stable', 'unsupported Guidance release status')
        require(guidance['prepared_on'] == '2026-10-10', 'unexpected Guidance preparation date')
        require(guidance['validation']['official_release'] == 'human_approved_v2_5_at_package_freeze', 'Stable approval metadata differs from the recorded decision')
        require(sha(canonical(guidance_body(guidance))) == fixed['guidance_rules_excluding_status_prepared_on_and_official_release'], 'Guidance changed beyond the exact release metadata and context-path migration')
        return 'Every Guidance value preserved after exactly three release-metadata changes and the declared README context-path migration.'

    check('guidance_rules_preserved_with_exact_metadata_exceptions', guidance_identity)

    def logic_identity():
        raw = (ROOT / 'auren-core-logic_v2.5.md').read_bytes()
        anchor = b'The local YAML governs this narrative on conflict'
        require(raw.count(anchor) == 1, 'Logic anchor ambiguous')
        require(sha(raw.split(anchor, 1)[1]) == fixed['logic_body'], 'Logic body changed')
        return 'Logic body byte-identical after the fixed preface anchor.'

    check('logic_body_preserved', logic_identity)

    def adapters():
        excerpt = adapter_excerpt((ROOT / 'INTEGRATION_HANDOFF_v2.5.md').read_text(encoding='utf-8'))
        status_text = CONFIG['prepared_adapter_status']
        require(excerpt.count(status_text) == 1, 'unexpected adapter release/evidence sentence')
        require(sha(excerpt.replace(status_text, '', 1).encode()) == fixed['adapter_body_excluding_single_status_sentence'], 'adapter behavior changed')
        return 'Only one release/evidence sentence differs; all other bytes inside the public adapter excerpt are preserved.'

    check('public_adapter_behavior_preserved', adapters)

    def whole_files():
        for name, digest in CONFIG['prepared_full_file_hashes'].items():
            require(sha((ROOT / name).read_bytes()) == digest, 'protected prepared file changed: ' + name)
        return 'Full bytes of operative prepared files match their exact preparation definitions, including prefaces.'

    check('operative_files_exact_bytes', whole_files)

    def exports():
        original = (ROOT / 'auren-core-specs_v2.5.yaml').read_bytes()
        require(original == (ROOT / 'auren-core-specs_v2.5.yaml.txt').read_bytes() == (ROOT / 'exports/auren-core-specs_v2.5.yaml.txt').read_bytes(), 'YAML text exports differ')
        return 'All three v2.5 YAML/text copies are byte-identical.'

    check('yaml_text_exports_identical', exports)

    def scenarios():
        require(sha((ROOT/'evals/scenarios_v2.5.yaml').read_bytes()) == fixed['scenario_yaml'], 'scenario YAML changed')
        require(sha((ROOT/'evals/scenarios_v2.5.md').read_bytes()) == fixed['scenario_markdown'], 'scenario Markdown changed')
        entries = suite['scenarios']
        require([x['id'] for x in entries] == [f'T{i:02d}' for i in range(1,46)], 'scenario inventory changed')
        require(sum(1 + len(x.get('followups', [])) for x in entries) == 51, 'scenario stage count changed')
        for entry in entries:
            for path in refs(entry):
                resolve(core, path)
        return 'Both authored scenario files are byte-identical to FC2: 45 cases, 51 canonical stages and valid references.'

    check('scenario_bytes_inventory_and_references', scenarios)

    def routing():
        core_refs = list(refs(core))
        require(len(core_refs) == 54, 'Core reference inventory changed')
        for path in core_refs:
            resolve(core, path)
        order = core['mode_priority']['priority_order']
        require(order == guidance['response_priority'], 'mode priority mismatch')
        require(len(order) == len(set(order)) == 7, 'mode inventory changed')
        require(set(order) == set(core['mode_priority']['mode_map']), 'mode map incomplete')
        require(core['before_response_check']['priority_policy_ref'] == 'mode_priority', 'final priority differs')
        require(core['before_response_check']['routing_policy_ref'] == core['safety_and_ethics_guardrails']['law_1']['on_risk']['routing_policy_ref'], 'final routing differs')
        limits = guidance['question_limits']
        require(core['systemic_method_layer']['phase_0_contracting']['constraints']['max_contracting_questions'] == limits['normal_phase_0_contracting'] == 2, 'contracting budget differs')
        require(core['systemic_method_layer']['phase_0_contracting']['constraints']['max_observation_consent_offers'] == limits['additional_optional_consent_offer'] == 1, 'consent offer budget differs')
        require(core['dependency_prevention']['stabilization_before_reflection']['constraints']['max_orienting_questions'] == limits['stabilization_total'] == 1, 'stabilization budget differs')
        require(core['safety_and_ethics_guardrails']['crisis_protocol']['response_constraints']['max_questions'] == limits['crisis_total'] == 1, 'crisis budget differs')
        return '54 Core references, seven mode priorities, final routing and distinct question budgets align.'

    check('local_references_routing_and_question_budgets', routing)

    def policies():
        for name, hashes in CONFIG['policies'].items():
            text = (ROOT / name).read_text(encoding='utf-8')
            require(text.count(CONFIG['prepared_policy_header']) == 1, 'unexpected policy adoption header: ' + name)
            require(CONFIG['draft_policy_header'] not in text, 'old Draft line remains: ' + name)
            if name == 'CONTRIBUTING.md':
                change = CONFIG['contribution_reporting_change']
                require(text.count(change['to']) == 1, 'CONTRIBUTING reporting expansion missing or duplicated')
                text = text.replace(change['to'], change['from'], 1)
            require(sha(text.replace(CONFIG['prepared_policy_header'], '', 1).encode()) == hashes['body_without_status_sha256'], 'reviewed policy body changed outside the declared reporting expansion: ' + name)
            require(scope['reviewed_policy_identity'][name] == hashes, 'reviewed policy provenance differs: ' + name)
        return 'Three reviewed R1 policy bodies preserved; reversing the single CONTRIBUTING reporting expansion restores its reviewed R1 body.'

    check('reviewed_r1_policy_bodies_preserved', policies)

    def reporting_routes():
        contributing = (ROOT/'CONTRIBUTING.md').read_text(encoding='utf-8')
        for filename, subject in [('CODE_OF_CONDUCT.md', 'AUREN Core — conduct concern'), ('SAFETY.md', 'AUREN Core — safety concern'), ('SECURITY.md', 'AUREN Core — security report')]:
            policy = (ROOT/filename).read_text(encoding='utf-8')
            require('[' + filename + '](' + filename + ')' in contributing, 'policy route missing: ' + filename)
            require(subject in contributing and subject in policy, 'email subject mismatch: ' + filename)
            require('mailto:' + CONFIG['reporting_email'] in policy, 'policy contact mismatch: ' + filename)
        security = (ROOT/'SECURITY.md').read_text(encoding='utf-8')
        private_steps = security.split('## Report privately\n\n', 1)[1].split('\n\n', 1)[0]
        require(private_steps in contributing, 'private vulnerability form/email fallback differs from SECURITY')
        require('https://github.com/stephan-davis-lab/auren-core-specs/issues' in contributing, 'public issue route missing')
        require(status['reporting_email'] == CONFIG['reporting_email'], 'project contact differs')
        require(scope['current_policy_file_sha256'] == {name: sha((ROOT/name).read_bytes()) for name in CONFIG['policies']}, 'current policy provenance differs')
        return 'Conduct/safety/security routes, three subjects, project email and exact SECURITY private-report steps are consistent.'

    check('contribution_reporting_routes_consistent', reporting_routes)

    def history():
        for name, digest in {**CONFIG['preserved_repository'], **CONFIG['immutable_fc2']}.items():
            require(sha((ROOT / name).read_bytes()) == digest, 'historical source changed: ' + name)
        return 'Historical v2.4 files, FC2 evidence and preparation-R1 records preserved byte for byte.'

    check('historical_v2_4_and_fc2_evidence_preserved', history)

    def licensing():
        require(sha((ROOT/'LICENSE').read_bytes()) == fixed['cc_legal_code'], 'full CC legal code changed')
        require(sha((ROOT/'validation/LICENSE-MIT.txt').read_bytes()) == fixed['mit_license'], 'MIT license changed')
        notice = (ROOT / 'NOTICE.md').read_text(encoding='utf-8')
        for section, digest in CONFIG['notice_expected_sections'].items():
            chunk = notice.split('## ' + section + '\n\n', 1)[1].split('\n## ', 1)[0]
            require(sha(chunk.encode()) == digest, 'NOTICE rights section differs from its approved definition: ' + section)
        for name in [*CONFIG['policies'], 'validation/LICENSE-MIT.txt', 'auren-core-specs_v2.5.yaml', 'exports/auren-core-specs_v2.5.yaml.txt']:
            require(name in notice and (ROOT/name).is_file(), 'NOTICE file scope mismatch: ' + name)
        require('do not add restrictions to reuse permitted' in notice, 'policy/license distinction missing')
        return 'Full CC/MIT texts verified; confirmed external-material exclusions and retained mark-right section match exact definitions; NOTICE scope matches files.'

    check('license_texts_and_complete_notice_merge', licensing)

    def links():
        require({p.name for p in ROOT.glob('README*')} == {'README.md'}, 'README must be central and unique')
        require({p.name for p in ROOT.glob('CHANGELOG*')} == {'CHANGELOG.md'}, 'CHANGELOG must be central and unique')
        require({p.name for p in ROOT.glob('NOTICE*')} == {'NOTICE.md'}, 'NOTICE must be central and unique')
        require({p.name for p in ROOT.glob('LICENSE*')} == {'LICENSE'}, 'CC LICENSE must be central and unique')
        count = 0
        for path in ROOT.rglob('*.md'):
            for target in re.findall(r'\[[^\]\n]*\]\(([^)\s]+)\)', path.read_text(encoding='utf-8')):
                if target.startswith(('https:', 'http:', 'mailto:', '#')):
                    continue
                target = target.split('#', 1)[0]
                require((path.parent / target).resolve().is_file(), 'broken local Markdown target: ' + str(path.relative_to(ROOT)) + ': ' + target)
                count += 1
        for key in ('operational', 'narrative', 'context'):
            require((ROOT/guidance['source_hierarchy'][key]).is_file(), 'Guidance source path missing')
        require((ROOT/core['release']['behavioral_evidence_scope']).is_file(), 'behavioral summary missing')
        return f'{count} local Markdown targets and all operative source paths resolve; no external currentness claim.'

    check('central_documents_and_local_links', links)

    def evidence():
        require(status['stage'] == 'stable_approved', 'unsupported stage')
        require(status['human_release_decision'] == core['release']['human_release_decision'] == 'approved', 'recorded human Stable decision mismatch')
        require(scope['status'] == 'maintainer_approved_stable_at_package_freeze', 'scope status mismatch')
        require(status['approved_on'] == scope['approved_on'] == core['release']['approved_on'] == '2026-10-10', 'approval date mismatch')
        require(status['approval_record'] == scope['approval_record'] == CONFIG['approval_record_path'], 'approval record path mismatch')
        require(sha((ROOT/CONFIG['approval_record_path']).read_bytes()) == CONFIG['approval_record_sha256'], 'approval record changed')
        require(status['policy_adoption'] == scope['human_adoption'] == CONFIG['expected_policy_adoption'], 'policy adoption differs from recorded maintainer decision')
        require(status['reporting_route_confirmation'] == CONFIG['expected_reporting_confirmation'], 'reporting configuration claim differs from its evidence')
        require(status['reporting_configuration'] == scope['reporting_configuration'] == CONFIG['expected_reporting_configuration'], 'reporting scope or evidence limits changed')
        require(status['private_vulnerability_reporting'] == CONFIG['expected_reporting_configuration']['private_vulnerability_reporting'], 'reporting status mismatch')
        require(status['publication_status'] == core['release']['publication_status'] == 'not_published', 'publication preempted')
        require(status['public_sync'] == status['production_deployment'] == 'not_performed', 'deployment preempted')
        require(status['new_model_runs_in_this_preparation'] == scope['new_model_runs'] == 0, 'new model run claim')
        require(core['release']['external_currentness_checked'] is False, 'external currentness overclaim')
        actual_reports = {r['report_filename']: r['report_sha256'] for r in status['completed_reviews']}
        require(actual_reports == CONFIG['expected_report_hashes'], 'review-report identity mismatch')
        require(all(r['verdict'] == 'PASS' for r in status['completed_reviews']), 'review verdict changed')
        require(scope['private_material_included'] is False, 'scope claim mismatch')
        summary = (ROOT/'BEHAVIORAL_VALIDATION_SUMMARY_v2.5.md').read_text(encoding='utf-8')
        for marker in ['126 initiale Antworten + 18 Fortsetzungen', 'innerhalb jeweils einer User-Nachricht', '1 Fall FAIL (T03)', 'T23', 'interne Modell-ID bleibt unbekannt', 'Memory und Retrieval-Abdeckung bleiben unbekannt', 'keine neue Verhaltensevidenz']:
            require(marker in summary, 'evidence limitation absent: ' + marker)
        return 'Source reviews retain their exact scope; the human Stable decision is recorded, publication/deployment remain separate, and zero new model runs are claimed.'

    check('review_evidence_and_human_publication_boundaries', evidence)

    def public_scope():
        files = [p for p in ROOT.rglob('*') if p.is_file()]
        for path in files:
            name = path.relative_to(ROOT).as_posix()
            require(not path.is_symlink(), 'symlink in package')
            require(not any(part in {'.git', '__pycache__'} for part in path.relative_to(ROOT).parts), 'repository/cache internals included')
            require(path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.zip'}, 'image or nested archive in public payload')
            require(not re.search(r'(?i)(authorization_key|antwortbogen|nacht[e]?st_evidenz|greenshot)', name), 'private file name in public payload')
            text = path.read_text(encoding='utf-8')
            require(not re.search(r'AAC1\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}', text), 'credential-shaped data in public payload')
        return 'UTF-8 payload only; no private response originals, images, nested audit ZIP, credentials, symlinks or repository internals.'

    check('public_payload_scope', public_scope)

    if args.baseline_fc2:
        def baseline():
            raw = args.baseline_fc2.read_bytes()
            require(sha(raw) == CONFIG['source_hashes']['public_FC2_sha256'], 'baseline ZIP is not the frozen Public FC2')
            prefix = 'AUREN_Core_Specs_v2.5_Public_FinalCandidate_FC2/'
            with zipfile.ZipFile(args.baseline_fc2) as archive:
                require(archive.testzip() is None, 'baseline ZIP CRC error')
                for line in archive.read(prefix+'SHA256SUMS.txt').decode().splitlines():
                    digest, name = line.split('  ', 1)
                    require(sha(archive.read(prefix+name)) == digest, 'baseline manifest mismatch')
                original_core = yaml.load(archive.read(prefix+'auren-core-specs_v2.5.yaml'), Loader=UniqueLoader)['auren_core_spec']
                expected = deepcopy(original_core)
                expected['release'] = CONFIG['expected_release']
                require(expected == core, 'Core changed outside the exact release metadata definition')
                original_guidance = yaml.load(archive.read(prefix+'Guidance4AIsystems_v2.5.txt'), Loader=UniqueLoader)['orientation_framework']
                expected_guidance = deepcopy(original_guidance)
                expected_guidance['status'] = 'stable'
                expected_guidance['prepared_on'] = '2026-10-10'
                expected_guidance['validation']['official_release'] = 'human_approved_v2_5_at_package_freeze'
                require(original_guidance['source_hierarchy']['context'] == CONFIG['guidance_context_path_change']['from'], 'unexpected frozen context path')
                expected_guidance['source_hierarchy']['context'] = CONFIG['guidance_context_path_change']['to']
                require(expected_guidance == guidance, 'Guidance changed outside the three exact release metadata paths and README path')
                original_adapter = adapter_excerpt(archive.read(prefix+'INTEGRATION_HANDOFF_v2.5.md').decode())
                current_adapter = adapter_excerpt((ROOT/'INTEGRATION_HANDOFF_v2.5.md').read_text(encoding='utf-8'))
                expected_adapter = original_adapter.replace(CONFIG['old_adapter_status'], CONFIG['prepared_adapter_status'], 1)
                require(expected_adapter == current_adapter, 'public adapter changed outside the single permitted status sentence')
                for name in ['evals/scenarios_v2.5.md','evals/scenarios_v2.5.yaml']:
                    require(archive.read(prefix+name) == (ROOT/name).read_bytes(), 'scenario bytes differ directly from FC2')
            return 'Actual frozen ZIP identity and payload hashes checked; direct Core/Guidance whitelist, adapter and scenario comparisons pass.'
        check('direct_comparison_to_actual_frozen_fc2_zip', baseline)

    if not args.pre_freeze:
        def record():
            data = json.loads((ROOT/'validation/static-results_v2.5_stable.json').read_text(encoding='utf-8'))
            require(data['package'] == CONFIG['package_id'], 'validation record belongs to another package')
            require(data['phase'] == 'pre_freeze' and data['status'] == 'pass', 'pre-freeze validation record invalid')
            require(data['model_calls'] == 0 and data['human_approval_verified'] is False, 'validation overclaim')
            require(all(x['status'] == 'pass' for x in data['checks']), 'pre-freeze record contains failure')
            return 'Actual pre-freeze execution recorded; final manifest checks are performed separately after that record exists.'
        check('pre_freeze_execution_record', record)

        def manifest():
            rows = (ROOT/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
            entries = {}
            for row in rows:
                digest, name = row.split('  ', 1)
                require(re.fullmatch(r'[0-9a-f]{64}', digest) is not None, 'invalid digest')
                parts = PurePosixPath(name)
                require(not parts.is_absolute() and '..' not in parts.parts, 'unsafe manifest path')
                require(name not in entries and name != 'CHECKSUMS.sha256', 'duplicate or self manifest entry')
                path = ROOT/name
                require(path.is_file() and sha(path.read_bytes()) == digest, 'manifest hash mismatch: ' + name)
                entries[name] = digest
            actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() != 'CHECKSUMS.sha256'}
            require(set(entries) == actual, 'missing or unmanifested payload')
            return f'{len(entries)}/{len(entries)} payload hashes pass; checksum file self-hash excluded.'
        check('complete_frozen_manifest', manifest)

    return output(results, args)


def output(results, args):
    status = 'pass' if results and all(x['status'] == 'pass' for x in results) else 'fail'
    print(json.dumps({'package': CONFIG['package_id'], 'validation_kind': 'static_only', 'phase': 'pre_freeze' if args.pre_freeze else 'read_only_frozen_stable_package', 'status': status, 'checks': results, 'model_calls': 0, 'network_calls': 0, 'writes': 0, 'external_review_tool_execution_verified': False, 'human_approval_verified': False, 'human_release_decision_recorded': 'approved_in_maintainer_chat', 'semantic_or_safety_certification': False}, ensure_ascii=False, indent=2))
    return 0 if status == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
