import math
import pytest
import staking

@pytest.fixture(autouse=True)
def reset_wallets():
    staking.wallets.clear()
    staking.wallets.update({"test-wallet": {"nun_tokens": 1000, "staked": 100, "rewards": 5.0}})

@pytest.fixture
def client():
    staking.app.config.update(TESTING=True)
    with staking.app.test_client() as client:
        yield client

def test_health_is_sandbox(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["mode"] == "sandbox-only"

def test_unknown_wallet_returns_404(client):
    assert client.get("/balance/missing").status_code == 404

@pytest.mark.parametrize("amount", [0, -1, True, "10", None, float("nan"), float("inf")])
def test_invalid_stake_amount_returns_400(client, amount):
    response = client.post("/stake", json={"wallet": "test-wallet", "amount": amount})
    assert response.status_code == 400

def test_stake_success(client):
    response = client.post("/stake", json={"wallet": "test-wallet", "amount": 50})
    assert response.status_code == 200
    data = response.get_json()
    assert data["nun_tokens"] == 950
    assert data["staked"] == 150
    assert data["rewards"] == pytest.approx(5.5)

def test_stake_rejects_insufficient_balance(client):
    assert client.post("/stake", json={"wallet": "test-wallet", "amount": 5000}).status_code == 400

def test_unstake_partial(client):
    response = client.post("/unstake", json={"wallet": "test-wallet", "amount": 40})
    assert response.status_code == 200
    assert response.get_json()["nun_tokens"] == 1040
    assert response.get_json()["staked"] == 60

def test_unstake_rejects_excess(client):
    assert client.post("/unstake", json={"wallet": "test-wallet", "amount": 101}).status_code == 400

def test_claim_clears_rewards(client):
    response = client.post("/claim", json={"wallet": "test-wallet"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["claimed"] == 5
    assert data["rewards"] == 0
    assert data["nun_tokens"] == 1005

def test_non_json_body_rejected(client):
    response = client.post("/stake", data="not-json", content_type="text/plain")
    assert response.status_code == 400

def test_claiming_twice_does_not_duplicate_rewards(client):
    first = client.post("/claim", json={"wallet": "test-wallet"})
    second = client.post("/claim", json={"wallet": "test-wallet"})
    assert first.status_code == 200
    assert first.get_json()["claimed"] == 5
    assert second.status_code == 200
    assert second.get_json()["claimed"] == 0
    assert second.get_json()["nun_tokens"] == 1005
