// Runs at 06:00 on the 1st. Finance reads the output at 9am.
// Expects the last day of the month to be in the ledger already.
async function main() {
  const res = await fetch(`${process.env.LEDGER_URL}/reports/month-end`, { method: 'POST' });
  if (!res.ok) throw new Error(`month-end report failed: ${res.status}`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
