#!/usr/bin/env python3
"""Publish a reviewed historical report produced by the gallery's cloud scan."""

import argparse
import html
import json
import os
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote, urlsplit
from zoneinfo import ZoneInfo

from scan_gallery import INDEX, LICENSES, extend_catalog, image_size, json_section, request, set_section, update_stamp


FEATURED = [
    {
        "kind": "abstract",
        "journal": "European Heart Journal",
        "title": "夜间光照与心脏结构和功能",
        "tags": "环境健康|队列研究|心血管",
        "note": "把队列的夜间光照测量和心脏磁共振分析放在同一张摘要里。",
        "source": "https://doi.org/10.1093/eurheartj/ehag563",
        "image": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13773033.1/ehag563_sga.webp",
        "credit": "Dai 等 · Oxford University Press / PubMed Central",
        "license": "by",
        "doi": "10.1093/eurheartj/ehag563",
        "date": "2026-09-09",
        "width": 1600,
        "height": 1826,
        "file": "ehj-ehag563.webp"
    },
    {
        "kind": "figures",
        "journal": "npj Aging",
        "title": "人群多组学与表观遗传衰老的研究设计",
        "tags": "组学|老龄化|研究设计",
        "note": "图 1 将数据来源、研究问题、主要分析和后续验证排成四列。",
        "source": "https://doi.org/10.1038/s41514-026-00384-8",
        "image": "https://media.springernature.com/original/springer-static/image/art%3A10.1038%2Fs41514-026-00384-8/MediaObjects/41514_2026_384_Fig1_HTML.png",
        "credit": "Gai 等 · npj Aging 图 1",
        "license": "by-nc-nd",
        "doi": "10.1038/s41514-026-00384-8",
        "date": "2026-04-16",
        "width": 2050,
        "height": 1114,
        "file": "npj-aging-2026-384-fig1.png"
    },
    {
        "kind": "figures",
        "journal": "The Innovation Medicine",
        "title": "城市环境与 One Health 的概念框架",
        "tags": "环境健康|城市环境|概念图",
        "note": "图 1 用城市剖面连接多污染物暴露、建成环境、微气候和治理。",
        "source": "https://doi.org/10.59717/j.xinn-med.2026.100196",
        "image": "https://www.the-innovation.org/data/article/export-img?figureId=Figure1&articleId=697b36bfcf3295331f81a9bf",
        "credit": "Han、Gu 和 Ran · The Innovation Medicine 图 1",
        "license": "by",
        "doi": "10.59717/j.xinn-med.2026.100196",
        "date": "2026-01-31",
        "width": 1536,
        "height": 1066,
        "file": "innovation-medicine-100196-fig1.jpg"
    },
    {
        "kind": "cover",
        "journal": "Brain Health",
        "title": "Brain Health 创刊号封面",
        "tags": "封面|脑健康|老龄化",
        "note": "原刊封面将脑科学、实验室和身体活动放在同一景观中。期刊注明插图由 AI 辅助完成。",
        "source": "https://fliphtml5.com/cvlqh/BH-1-1-cover-to-cover/",
        "image": "https://genomicpress.com/wp-content/uploads/2026/04/Brain-Health-Cover-cropped3-scaled.png",
        "credit": "Julio Licinio / Genomic Press · 2026 年 5 月创刊号",
        "license": "by",
        "doi": "",
        "date": "2026-05",
        "width": 1600,
        "height": 2071,
        "file": "brain-health-2026-inaugural.png"
    }
]


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


def archive_featured(document):
    catalogue = json_section(document, 'catalog')
    known = {row[6] for row in catalogue}
    added = []
    for item in FEATURED:
        if item['source'] in known:
            continue
        reference = Path('assets') / 'reference' / item['file']
        stored = INDEX.parent / reference
        try:
            payload = request(item['image'], limit=8_000_001)
            if len(payload) > 8_000_000:
                raise ValueError('source image exceeds the archive size limit')
            dimensions = image_size(payload)
            expected = (item['width'], item['height'])
            if reference.suffix == '.webp':
                prefix = payload[:12]
                if len(payload) < 30 or prefix[:4] != b'RIFF' or prefix[8:12] != b'WEBP':
                    raise ValueError('source did not return the approved WebP image')
            elif dimensions != expected:
                raise ValueError(f'source image dimensions {dimensions} differ from {expected}')
        except (OSError, ValueError) as err:
            print(f"Deferred image: {item['title']}: {err}")
            continue
        stored.parent.mkdir(parents=True, exist_ok=True)
        stored.write_bytes(payload)
        info = {'date': item['date'], 'published': item['date'], 'width': item['width'],
                'height': item['height'], 'doi': item['doi'], 'size': f"{item['width']} × {item['height']}"}
        row = [item['kind'], item['journal'], 2026, item['title'], item['tags'], item['note'],
               item['source'], reference.as_posix(), item['credit'], item['license'], info]
        added.append(row)
    return set_section(document, 'catalog', added + catalogue), added


def write_review_summary(report):
    target = os.environ.get('GITHUB_STEP_SUMMARY')
    if not target:
        return
    grouped = {}
    for row in report['items']:
        grouped.setdefault(row[1], []).append(row)
    with Path(target).open('a', encoding='utf-8') as f:
        f.write('## 历史图文摘要候选\n\n')
        f.write(f"{report['start']} 至 {report['end']} · {len(report['items']):,} 张候选。"
                '逐张核对后可用 DOI 发布。\n\n')
        for journal, candidates in sorted(grouped.items()):
            f.write(f'<details><summary>{html.escape(journal)} · {len(candidates)} 张</summary>\n\n')
            f.write('| 图片或论文 | 首次线上 | 主题 | 尺寸 | 许可 | DOI |\n| --- | --- | --- | --- | --- | --- |\n')
            for row in candidates:
                info = row[10]
                doi = info['doi'].strip()
                title = html.escape(row[3]).replace('|', '&#124;').replace('\n', ' ')
                tag = html.escape(row[4]).replace('|', '、')
                preview = info.get('url', row[7])
                links = f'<a href="https://doi.org/{quote(doi, safe="/")}">{title}</a>'
                if valid_image_url(preview) and urlsplit(preview).hostname in {'ars.els-cdn.com', 'media.springernature.com'}:
                    links += f' · <a href="{html.escape(preview, quote=True)}">原图</a>'
                f.write(f"| {links} | {info['published']} | {tag} | {info['width']} × {info['height']} | {row[9]} | {html.escape(doi)} |\n")
            f.write('\n</details>\n\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--selection', default='')
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding='utf-8'))
    document = INDEX.read_text(encoding='utf-8')
    now = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    updated, added = apply_report(document, report, args.selection, now)
    updated, featured = archive_featured(updated)
    progress = json_section(updated, 'collection-report')
    latest = progress['latest']
    latest['candidates'] += sum(row[0] == 'abstract' for row in featured)
    latest['new_body_figures'] = sum(row[0] == 'figures' for row in featured)
    latest['new_covers'] = sum(row[0] == 'cover' for row in featured)
    updated = update_stamp(set_section(updated, 'collection-report', progress), progress['history'], latest)
    if latest['new_body_figures'] or latest['new_covers']:
        extra = f" 附加正文图 {latest['new_body_figures']} 张、封面 {latest['new_covers']} 张。"
        updated = re.sub(r'(<p id="coverage-status">.*?)</p>', lambda m: m[1] + extra + '</p>', updated, count=1, flags=re.S)
    INDEX.write_text(updated, encoding='utf-8')
    print(f'Added {len(featured)} individually reviewed abstracts, figures and covers.')
    write_review_summary(report)
    counts = report['results']
    print(f"Saved coverage for {len(counts)} journals, {sum(row['counts'].get('metadata_read', 0) for row in counts):,} records, and {len(report['items'])} graphical abstract candidates.")
    for row in counts:
        if row['errors'] or not row['counts'].get('metadata_read'):
            print(f"Check source: {row['name']} {row['errors'] or 'no records'}")
    print(f'Included {len(added)} reviewed graphical abstracts.')


if __name__ == '__main__':
    main()
