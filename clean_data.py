"""Extract the saved ledger, preserving word boundaries at HTML line breaks."""
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import csv
import json

ROOT = Path(__file__).parent

class LedgerParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        if tag in ('td', 'th'):
            self.cell = ''
        elif tag in ('br', 'p', 'div') and self.cell is not None:
            self.cell += ' '

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            if self.row is not None:
                self.row.append(' '.join(self.cell.split()))
            self.cell = None
        elif tag in ('p', 'div') and self.cell is not None:
            self.cell += ' '
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None

parser = LedgerParser()
parser.feed((ROOT / 'source.html').read_text())
data = []
for date, donor, amount in parser.rows:
    data.append(dict(date=datetime.strptime(date, '%m/%d/%Y').date().isoformat(),
                     donor=donor, amount=float(Decimal(amount.replace('$', '').replace(',', '')))))
# Reconcile the existing live-page records before merging historical sources.
old = json.loads((ROOT / 'data.json').read_text())
site_old = [r for r in old if r['date'] >= '2025-01-01']
assert {(r['date'],r['donor'],r['amount']) for r in data} == {(r['date'],r['donor'],r['amount']) for r in site_old}
site_count = len(data)
history = []
spacing_changes = []
source = ROOT / 'sources/UIJP-donations-2016-through-2020.csv'
with source.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    assert reader.fieldnames == ['Name', 'Amount', 'Date']
    for line, row in enumerate(reader, 2):
        donor = ' '.join(row['Name'].split())
        assert donor, f'Missing donor on line {line}'
        amount = Decimal(row['Amount'].replace('$', '').replace(',', '').strip())
        assert amount.is_finite() and amount >= 0 and amount == amount.quantize(Decimal('.01'))
        date = datetime.strptime(row['Date'].strip(), '%b %d, %Y').date().isoformat()
        assert '2016-01-01' <= date <= '2020-12-31'
        history.append(dict(date=date, donor=donor, amount=float(amount)))
        if donor != row['Name']:
            spacing_changes.append(dict(line=line, before=row['Name'], after=donor))
# Stable date ordering; consolidate exact matches only, preserving name variants.
data = sorted(data + history, key=lambda row: row['date'], reverse=True)
assert len(data) == site_count + len(history)
raw_count = len(data)
raw_total = sum((Decimal(str(r['amount'])) for r in data), Decimal(0))
seen, cleaned, removed = set(), [], []
for csv_row, row in enumerate(data, 2):
    key = (row['date'], row['donor'], Decimal(str(row['amount'])))
    if key in seen:
        removed.append(dict(original_csv_row=csv_row, **row))
    else:
        seen.add(key)
        cleaned.append(row)
# The review report is an immutable record of the original 4,097-row ledger.
with (ROOT / 'duplicate-rows.csv').open(newline='') as f:
    reviewed = list(csv.DictReader(f))
expected = {(r['date'],r['donor'],Decimal(r['amount'])):int(r['extra_rows']) for r in reviewed}
from collections import Counter
assert Counter((r['date'],r['donor'],Decimal(str(r['amount']))) for r in removed) == expected
removed_total = sum((Decimal(str(r['amount'])) for r in removed), Decimal(0))
data = cleaned
assert raw_total - removed_total == sum((Decimal(str(r['amount'])) for r in data), Decimal(0))
(ROOT / 'deduplication-report.json').write_text(json.dumps(dict(
    match_fields=['date','donor','amount'], original_rows=raw_count, cleaned_rows=len(data),
    removed_rows=len(removed), removed_total=str(removed_total),
    documentation='duplicate-rows.csv (original row numbers, unchanged)',
    removed=removed), indent=2))
(ROOT / 'data.json').write_text(json.dumps(data, ensure_ascii=False))
with (ROOT / 'donations.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'donor', 'amount'])
    writer.writeheader()
    writer.writerows(data)
from collections import Counter
import hashlib
by_year = {}
for row in data:
    year = row['date'][:4]
    entry = by_year.setdefault(year, dict(rows=0, cents=0))
    entry['rows'] += 1
    entry['cents'] += int(Decimal(str(row['amount'])) * 100)
report = dict(source_file=source.name, source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              imported_rows=len(history), source_site_rows=site_count, retained_site_rows=sum(r['date']>='2025-01-01' for r in data), combined_rows=len(data), original_combined_rows=raw_count, removed_exact_duplicates=len(removed),
              historical_total=str(sum((Decimal(str(r['amount'])) for r in history), Decimal(0))),
              combined_total=str(sum((Decimal(str(r['amount'])) for r in data), Decimal(0))),
              first_date=min(r['date'] for r in data), last_date=max(r['date'] for r in data),
              years=by_year, missing_years=[2021, 2022, 2023, 2024],
              historical_exact_duplicates_removed=sum(r['date']<'2021-01-01' for r in removed),
              historical_spacing_changes=spacing_changes,
              policy='Exact date/name/amount matches consolidated to one record; duplicate-rows.csv preserved. Whitespace normalized; spelling and capitalization preserved. Missing years are not zero giving.')
(ROOT / 'import-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
