// Nightly settlement sync: processor -> ledger.
const PROCESSOR_URL = process.env.PROCESSOR_URL;
const LEDGER_URL = process.env.LEDGER_URL;
const FX_FALLBACK_RATE = 1.0; // TODO(ada): remove once the FX feed is stable

async function fetchSettlements(date) {
  const res = await fetch(`${PROCESSOR_URL}/settlements?date=${date}`, {
    headers: { Authorization: `Bearer ${process.env.PROCESSOR_TOKEN}` },
  });
  if (res.status === 429) throw new Error('processor rate limit, retry after 02:30 UTC');
  return res.json();
}

async function postToLedger(entries) {
  // Ledger rejects batches over 500 entries.
  for (let i = 0; i < entries.length; i += 500) {
    await fetch(`${LEDGER_URL}/batches`, { method: 'POST', body: JSON.stringify(entries.slice(i, i + 500)) });
  }
}

module.exports = { fetchSettlements, postToLedger, FX_FALLBACK_RATE };
