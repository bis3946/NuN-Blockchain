# NuN Blockchain Sandbox — Test Matrix

This is a test specification only. It does not claim that tests have run, and it is not a production deployment.

| Area | Case | Expected result |
|---|---|---|
| Health | GET /health | HTTP 200 with explicit sandbox mode and storage mode |
| Balance | Known test wallet | HTTP 200 with wallet identifier and balances |
| Balance | Unknown wallet | HTTP 404; no empty success response |
| JSON | Missing/malformed body | HTTP 400 with safe error message |
| Stake amount | Zero, negative, boolean, string, NaN, infinity | HTTP 400; no state mutation |
| Stake funds | Amount exceeds available balance | HTTP 400; no state mutation |
| Stake success | Positive amount within test balance | HTTP 200 and exact expected balance changes |
| Unstake | Amount exceeds staked balance | HTTP 400; no state mutation |
| Unstake success | Partial amount | Only requested amount moves from staked to liquid balance |
| Claim | Rewards available | Claimed amount reported and rewards reset to zero exactly once |
| Persistence | Restart process | Document that current in-memory state resets; do not call this durable storage |
| Security | No credentials supplied | Do not claim authenticated or production-safe behavior; authentication must be designed before exposure |

## Current status
Static review found that the current main-branch implementation has no `/health` endpoint, stores balances in memory, accepts unchecked request values, and has no visible authentication. The sandbox test branch is based on this implementation, so the tests above are acceptance criteria and are expected to fail until the corresponding implementation is added. No runtime tests have been executed by this document.

## Safe execution order
1. Use an isolated local environment and synthetic accounts only.
2. Add the health endpoint and input validation on the sandbox branch.
3. Implement the test cases and run them against a disposable test state.
4. Save the actual command output and dependency versions.
5. Do not merge until tests pass and authentication, persistence, and transaction integrity have been reviewed.
