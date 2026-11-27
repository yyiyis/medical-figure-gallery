#!/usr/bin/env python3
"""Publish a reviewed historical report produced by the gallery's cloud scan."""

import argparse
import html
import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote, urlsplit
from zoneinfo import ZoneInfo

from scan_gallery import INDEX, LICENSES, extend_catalog, json_section, set_section, update_stamp


PENDING = (
    'publisher_review', 'date_needs_confirmation', 'licence_unconfirmed',
    'figure_check_failed', 'missing_pmc_version', 'image_unavailable_or_small',
)


def coverage_markup(history):
    headers = ('期刊', '目录条目', '图文摘要候选', '待核对', '状态')
    head = ''.join(f'<th scope="col">{label}</th>' for label in headers)
    rows = []
    for result in history['results']:
        counts = result['counts']
        fetched = counts.get('metadata_read', 0)
        pending = sum(counts.get(key, 0) for key in PENDING)
        state = '需复扫' if result['errors'] else ('已读目录' if fetched else '索引未命中')
        values = (f'{fetched:,}', f"{counts.get('candidate', 0):,}", f'{pending:,}', state)
        cells = ''.join(f'<td>{value}</td>' for value in values)
        rows.append(f'<tr><th scope="row">{html.escape(result["name"])}</th>{cells}</tr>')
    return (
        '<details id="journal-scan-details"><summary>查看逐刊盘点</summary>'
        '<p>目录条目涵盖文章及其他类型记录。候选图须复核许可、清晰度和作图参考价值。'
        '待核对项包括首次线上日期、许可、原图缺失和分辨率。</p>'
        '<div style="overflow-x:auto"><table aria-label="2026 年历史目录扫描">'
        f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></details>'
    )


def valid_image_url(value):
    parsed = urlsplit(value)
    return parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username


def apply_report(document, report, selectors, published_at):
    registry = json_section(document, 'journal-registry')
    journals = {journal['name'] for group in registry['groups'] for journal in group['journals']}
    coverage = report['results']
    reported = [result['name'] for result in coverage]
    if (report['mode'] != 'backfill' or report['start'] != registry['start'] or report['end'] != registry['end']
            or len(reported) != len(journals) or set(reported) != journals):
        raise ValueError('The report must cover the registered historical period and all registered journals')
    if not any(result['counts'].get('metadata_read', 0) and not result['errors'] for result in coverage):
        raise ValueError('There is no successful source in the report')
    by_doi = {row[10]['doi'].strip().casefold(): row for row in report['items']}
    selected = {doi.strip().casefold() for doi in selectors.split(',') if doi.strip()}
    if not selected.issubset(by_doi):
        raise ValueError(f'Reviewed DOIs absent from report: {sorted(selected.difference(by_doi))}')
    curated = []
    for doi in sorted(selected):
        row = list(by_doi[doi])
        quality = dict(row[10], doi=doi)
        row[6] = 'https://doi.org/' + quote(doi, safe='/')
        row[10] = quality
        if (row[0] != 'abstract' or row[1] not in journals or row[9] not in LICENSES.values()
                or not valid_image_url(row[7]) or not valid_image_url(quality.get('url', row[7]))
                or not report['start'] <= date.fromisoformat(quality['published']).isoformat() <= report['end']
                or quality['width'] < 1200 or quality['height'] < 1):
            raise ValueError(f'Figure failed publication checks: {doi}')
        curated.append(row)
    catalogue, added = extend_catalog(json_section(document, 'catalog'), curated)
    progress = json_section(document, 'collection-report', {})
    history = {key: value for key, value in report.items() if key != 'items'}
    latest = {**history, 'stamp': published_at, 'candidates': len(added)}
    progress.update(history=history, latest=latest)
    changed = set_section(set_section(document, 'catalog', catalogue), 'collection-report', progress)
    panel = coverage_markup(history)
    old = r'<details id="journal-scan-details">.*?</details>'
    marker = '<div id="scope-groups" class="scope-grid"></div>'
    if re.search(old, changed, re.S):
        changed = re.sub(old, lambda _: panel, changed, count=1, flags=re.S)
    elif changed.count(marker) == 1:
        changed = changed.replace(marker, marker + '\n' + panel, 1)
    else:
        raise ValueError('The gallery journal scope markup changed')
    changed = changed.replace("count + ' 刊拟盘点 · '", "count + ' 刊目录 · '", 1)
    return update_stamp(changed, history, latest), added


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--selection', default='')
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding='utf-8'))
    document = INDEX.read_text(encoding='utf-8')
    now = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    updated, added = apply_report(document, report, args.selection, now)
    INDEX.write_text(updated, encoding='utf-8')
    counts = report['results']
    print(f"Saved coverage for {len(counts)} journals, {sum(row['counts'].get('metadata_read', 0) for row in counts):,} records, and {len(report['items'])} graphical abstract candidates.")
    for row in counts:
        if row['errors'] or not row['counts'].get('metadata_read'):
            print(f"Check source: {row['name']} {row['errors'] or 'no records'}")
    print(f'Included {len(added)} reviewed graphical abstracts.')


if __name__ == '__main__':
    main()
