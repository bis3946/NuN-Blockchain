# NuN Blockchain — API Sandbox Test Plan

Status: isolated planning branch; no production code changed and no runtime tests have been executed yet.

## Purpose
Validate the Flask API described by the repository README without using live funds, wallets, or a production network.

## Safety rules
- Run against a local disposable database and synthetic test accounts only.
- Never use real private keys, real tokens, or production balances.
- Keep secrets in environment variables; do not commit credentials.
- Do not expose a local service publicly through a tunnel during initial tests.

## Test cases
1. Startup: launch the documented Flask entry point in an isolated environment; record the actual command, dependency versions and exit status.
2. Health/readiness: verify a health endpoint exists; if missing, mark as a required implementation rather than assuming one.
3. Balance: test a synthetic account, unknown account, malformed input and empty state.
4. Stake/unstake/claim: test valid and invalid amounts, insufficient balance, repeated requests and idempotency.
5. Persistence: restart the service and confirm test state behaves as documented.
6. Security: validate input, authorization, error responses, secret handling and that no real funds can be moved.
7. Regression: run unit tests, API integration tests, lint/type checks where applicable and capture results.

## Acceptance criteria
- Every endpoint returns documented status codes and schemas.
- State changes are atomic and repeat requests cannot double-apply a transaction.
- Tests use disposable data and pass repeatably.
- No deployment or production transaction is performed by this plan.

## Current evidence
The repository README describes a Flask application launched via `staking.py` on localhost:5000 with balance, stake, unstake and claim endpoints. This is documentation, not proof that the service starts or that the endpoints pass tests.
