// Entry point for the nightly cron: node src/run.js --date <YYYY-MM-DD|yesterday>
const { fetchSettlements, postToLedger } = require('./sync');

function parseDate(argv) {
  const i = argv.indexOf('--date');
  const value = i === -1 ? 'yesterday' : argv[i + 1];
  if (value !== 'yesterday') return value;
  const d = new Date(Date.now() - 24 * 60 * 60 * 1000);
  return d.toISOString().slice(0, 10);
}

async function main() {
  const date = parseDate(process.argv);
  const settlements = await fetchSettlements(date);
  if (process.argv.includes('--dry-run')) {
    console.log(`${settlements.length} settlements for ${date} (dry run)`);
    return;
  }
  await postToLedger(settlements);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
