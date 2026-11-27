"""Keep a weekly candidate list and publish originals only after review."""

import argparse
from datetime import datetime
import html
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from publish_history import valid_image_url
from scan_gallery import INDEX, LICENSES, extend_catalog, image_size, json_section, request, set_section, update_stamp

QUEUE = Path('data/weekly-review.json')


def doi(row):
    return row[10]['doi'].casefold()


def save_original(row, report_size):
    row = list(row)
    metadata = dict(row[10])
    url = metadata.get('url', row[7])
    if row[9] not in LICENSES.values() or not valid_image_url(url):
        raise ValueError(f'Unexpected source or licence for {row[6]}')
    payload = request(url, limit=8_000_001)
    if len(payload) > 8_000_000 or image_size(payload) != report_size:
        raise ValueError(f'Unexpected source dimensions for {row[6]}')
    extension = Path(urlsplit(url).path).suffix.casefold()
    if extension not in {'.jpg', '.jpeg', '.png', '.webp'}:
        raise ValueError(f'Unexpected file type for {row[6]}')
    filename = re.sub(r'[^a-z0-9-]+', '-', doi(row)) + extension
    relative = Path('assets/reference') / filename
    target = INDEX.parent / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    metadata.pop('url', None)
    row[7], row[10] = relative.as_posix(), metadata
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--scan', type=Path)
    mode.add_argument('--reviewed')
    args = parser.parse_args()

    document = INDEX.read_text(encoding='utf-8')
    progress = json_section(document, 'collection-report')
    catalog = json_section(document, 'catalog')
    queue = json.loads(QUEUE.read_text(encoding='utf-8')) if QUEUE.exists() else {'items': []}
    published = {doi(row) for row in catalog if len(row) > 10 and row[10].get('doi')}
    pending = {doi(row): row for row in queue['items'] if doi(row) not in published}
    added = []
    if args.scan:
        report = json.loads(args.scan.read_text(encoding='utf-8'))
        if report['mode'] != 'weekly' or not any(not journal['errors'] for journal in report['results']):
            raise ValueError('A successful weekly scan is required')
        pending.update({doi(row): row for row in report['items'] if doi(row) not in published})
        queue['scan'] = {key: value for key, value in report.items() if key != 'items'}
    else:
        selected = {value.strip().casefold() for value in args.reviewed.split(',') if value.strip()}
        missing = selected - pending.keys() - published
        if missing or not selected:
            raise ValueError(f'Reviewed DOI list is empty or contains unrecognized entries: {sorted(missing)}')
        approved = []
        for key in sorted(selected & pending.keys()):
            row = pending[key]
            size = (row[10]['width'], row[10]['height'])
            approved.append(save_original(row, size))
        catalog, added = extend_catalog(catalog, approved)
        for row in added:
            pending.pop(doi(row))

    queue['items'] = sorted(pending.values(), key=lambda row: (row[10]['published'], doi(row)), reverse=True)
    now = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    last_scan = queue.get('scan', progress['latest'])
    abstracts = sum(row[0] == 'abstract' for row in added)
    latest = {**last_scan, 'stamp': now, 'candidates': abstracts, 'pending_review': len(pending)}
    progress['latest'] = latest
    updated = set_section(set_section(document, 'catalog', catalog), 'collection-report', progress)
    updated = update_stamp(updated, progress['history'], latest)
    figures = sum(row[0] == 'figures' for row in added)
    covers = sum(row[0] == 'cover' for row in added)
    note = f' 当前有 {len(pending)} 张周更候选待复核。'
    if figures or covers:
        note = f' 新增正文图 {figures} 张、封面 {covers} 张。' + note
    updated = re.sub(r'(<p id="coverage-status">.*?)</p>',
                     lambda match: match[1] + html.escape(note) + '</p>', updated, count=1, flags=re.S)
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    INDEX.write_text(updated, encoding='utf-8')
    print(f'{len(pending)} weekly candidates awaiting review; {len(added)} originals published.')


if __name__ == '__main__':
    main()
