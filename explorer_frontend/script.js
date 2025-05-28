
function update() {
  let wallet = document.getElementById('walletSelect').value;
  fetch(`/balance/${wallet}`).then(r => r.json()).then(d => {
    document.getElementById('balance').innerText = JSON.stringify(d, null, 2);
  });
}
function stake() {
  fetch('/stake', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({wallet: 'test-wallet', amount: 1000})}).then(update);
}
function unstake() {
  fetch('/unstake', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({wallet: 'test-wallet'})}).then(update);
}
function claim() {
  fetch('/claim', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({wallet: 'test-wallet'})}).then(update);
}
update();
