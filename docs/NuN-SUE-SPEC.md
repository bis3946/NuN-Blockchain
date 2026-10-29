# NuN Sentence Understanding Engine (NuN-SUE)
Status: design specification only; not yet integrated or runtime-verified.

## Goal
Interpret text sentences and route a structured, confidence-scored interpretation to an authorized NuN workflow. This module does not read brain activity, provide telepathy, or perform neuroplasticity/regeneration.

## Pipeline
1. Input validation: accept UTF-8 text; enforce configurable size limits; reject empty input.
2. Language and spelling: detect/accept an explicit language; provide spelling/normalization suggestions without silently changing the original.
3. Sentence segmentation and syntax: identify sentence boundaries and grammatical structure.
4. Semantic interpretation: produce a concise meaning representation.
5. Intent classification: question, request/command, assertion, preference, or unclear.
6. Context resolution: use only explicitly supplied conversation context; mark missing or conflicting context.
7. Confidence and ambiguity gate: low confidence or materially ambiguous intent must return needs_clarification rather than trigger an action.
8. Policy and authorization gate: classify read-only vs consequential actions; require explicit authorization for external writes, financial actions, or irreversible changes.
9. Routing: send the validated structured result to a named downstream module; do not execute arbitrary model-generated commands.
10. Audit: log timestamp, request ID, language, selected intent, confidence, routing decision, and policy result. Avoid logging secrets or unnecessary personal text.

## Suggested output contract
```json
{
  "request_id": "caller-generated-id",
  "language": "hr",
  "original_text": "Molim te provjeri status modula.",
  "normalized_text": "Molim te provjeri status modula.",
  "intent": "request",
  "meaning": "The user asks to check the module status.",
  "entities": [],
  "confidence": 0.0,
  "needs_clarification": false,
  "route": "status_reader",
  "action_allowed": false,
  "policy_reason": "No downstream action has been authorized by this interpretation alone."
}
```
The confidence value above is illustrative schema data, not a measured model score.

## Minimum acceptance tests
- Croatian and English input.
- Spelling correction preserves the original text.
- Question, command, assertion, and ambiguous utterance are distinguished.
- Pronouns/references without sufficient context trigger clarification.
- Prompt-injection text inside user content is treated as data, not as a policy override.
- Low confidence never triggers consequential action.
- Unauthorized routing and unknown module names are rejected.
- Logs exclude credentials and redact configured sensitive fields.

## Integration plan
- Inspect the actual repository tree and existing runtime before choosing implementation paths.
- Add the engine behind a narrow interface and keep it separate from staking/token logic.
- Add unit tests and deterministic fixtures before enabling routing.
- Run CI on a feature branch; review test results and security implications.
- Do not deploy to production until persistence, authentication/authorization, rate limits, monitoring, and rollback are addressed.

## Current limitations
The repository file-tree inspection did not succeed in this session, so no code integration or test execution is claimed. This document is a proposal only.