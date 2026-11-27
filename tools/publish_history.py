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
        "title": "热带气旋与急性冠脉综合征",
        "tags": "环境健康|极端天气|心血管|人群研究",
        "note": "把气旋路径和全国医院病例并排放，上方交代样本，下方并列呈现就医延迟、滞后风险和应对含义。",
        "source": "https://doi.org/10.1093/eurheartj/ehag066",
        "image": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13549725.1/ehag066_sga.webp",
        "credit": "Li 等 · Oxford University Press / PubMed Central",
        "license": "by",
        "doi": "10.1093/eurheartj/ehag066",
        "date": "2026-02-18",
        "width": 1600,
        "height": 1481,
        "file": "ehj-ehag066.webp"
    },
    {
        "kind": "abstract",
        "journal": "European Heart Journal",
        "title": "儿童血压的遗传特征与成年健康",
        "tags": "生命历程|组学|人群遗传|心血管",
        "note": "左侧区分儿童发现与复现队列，并展示遗传重叠，右侧按器官归纳成年期结局。",
        "source": "https://doi.org/10.1093/eurheartj/ehag313",
        "image": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13533560.1/ehag313_ga.webp",
        "credit": "Xie 等 · Oxford University Press / PubMed Central",
        "license": "by",
        "doi": "10.1093/eurheartj/ehag313",
        "date": "2026-04-27",
        "width": 1600,
        "height": 1694,
        "file": "ehj-ehag313.webp"
    },
    {
        "kind": "abstract",
        "journal": "European Heart Journal",
        "title": "孕期母亲自身免疫病与子代心血管风险",
        "tags": "生命历程|早期暴露|心血管|队列研究",
        "note": "在同一张图里交代出生队列、父亲和表亲比较、可能的中介因素，并列展示估计值。",
        "source": "https://doi.org/10.1093/eurheartj/ehag316",
        "image": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13690822.1/ehag316_sga.webp",
        "credit": "Mo 等 · Oxford University Press / PubMed Central",
        "license": "by",
        "doi": "10.1093/eurheartj/ehag316",
        "date": "2026-04-22",
        "width": 1600,
        "height": 1695,
        "file": "ehj-ehag316.webp"
    },
    {
        "kind": "abstract",
        "journal": "European Heart Journal",
        "title": "乳腺癌治疗随访中的心脏变化与联合组学",
        "tags": "组学|蛋白组|代谢组|心血管|队列研究",
        "note": "用随访时间轴区分同次和跨次访视的分析，再用上下两层区分统计方法与发现。",
        "source": "https://doi.org/10.1093/eurheartj/ehag487",
        "image": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13359040.2/ehag487_sga.webp",
        "credit": "Ky 等 · Oxford University Press / PubMed Central",
        "license": "by",
        "doi": "10.1093/eurheartj/ehag487",
        "date": "2026-06-29",
        "width": 1600,
        "height": 1674,
        "file": "ehj-ehag487.webp"
    },
    {
        "kind": "figures",
        "journal": "Cell Reports Medicine",
        "title": "老年队列的代谢组与生活方式风险分层",
        "tags": "组学|代谢组|老龄化|队列研究|研究设计",
        "note": "图 1 用四个色块依次展示队列设计、代谢组测量、BMI 与代谢健康分层，以及生活方式和代谢评分的联合分析。",
        "source": "https://doi.org/10.1016/j.xcrm.2026.102907",
        "image": "https://ars.els-cdn.com/content/image/1-s2.0-S2666379126003241-gr1_lrg.jpg",
        "credit": "Chen 等 · Cell Reports Medicine 图 1",
        "license": "by-nc-nd",
        "doi": "10.1016/j.xcrm.2026.102907",
        "date": "2026-07-01",
        "width": 2822,
        "height": 4151,
        "file": "cell-reports-medicine-102907-fig1.jpg"
    },
    {
        "kind": "cover",
        "journal": "Emerging Infectious Diseases",
        "title": "维米尔《地理学家》",
        "tags": "封面|公共卫生|医学史",
        "note": "2026 年 6 月号所用封面画作。期刊用绘画中的光与观察，引出早期显微镜和对微生物的认识。",
        "source": "https://wwwnc.cdc.gov/eid/article/32/6/ac-3206_article",
        "image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2a/Johannes_Vermeer_-_The_Geographer_-_Google_Art_Project.jpg/1920px-Johannes_Vermeer_-_The_Geographer_-_Google_Art_Project.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "credit": "Johannes Vermeer · Städel Museum / Google Art Project · 公有领域",
        "license": "pd",
        "doi": "10.3201/eid3206.ac3206",
        "date": "2026-05-27",
        "width": 1920,
        "height": 2153,
        "file": "eid-2026-06-the-geographer.jpg"
    },
    {
        "kind": "figures",
        "journal": "Environment International",
        "title": "从出生到成年早期的多域暴露测量",
        "tags": "生命历程|暴露组|环境健康|表观遗传|研究设计",
        "note": "图 1 用同一条时间轴对齐四类暴露、不同时点的测量与 22 岁的 DNA 甲基化采样。",
        "source": "https://doi.org/10.1016/j.envint.2026.110430",
        "image": "https://ars.els-cdn.com/content/image/1-s2.0-S0160412026003880-gr1_lrg.jpg",
        "credit": "Opperbeck 等 · Environment International 图 1",
        "license": "by",
        "doi": "10.1016/j.envint.2026.110430",
        "date": "2026-07-27",
        "width": 3544,
        "height": 2681,
        "file": "environment-international-110430-fig1.jpg"
    },
    {
        "kind": "figures",
        "journal": "Nature Communications",
        "title": "化学暴露组网络的多层分群",
        "tags": "暴露组|网络图|组图",
        "note": "图 2 用局部放大和嵌套矩形表现从总体网络到细分群落的层级，再用下排图比较群落特征。",
        "source": "https://doi.org/10.1038/s41467-026-72402-y",
        "image": "https://media.springernature.com/original/springer-static/image/art%3A10.1038%2Fs41467-026-72402-y/MediaObjects/41467_2026_72402_Fig2_HTML.png",
        "credit": "Lombardo 等 · Nature Communications 图 2",
        "license": "by-nc-nd",
        "doi": "10.1038/s41467-026-72402-y",
        "date": "2026-04-27",
        "width": 1947,
        "height": 1942,
        "file": "nature-communications-72402-fig2.png"
    },
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


EDITORIAL = {
    "10.1016/j.jacadv.2026.102646": [
        "社会环境|多病共存|人群研究",
        "上下两层分别交代暴露和结局定义，再并排展示两种社会经济地位定义对疾病转移估计的影响。"
    ],
    "10.1016/j.jacadv.2026.102665": [
        "人群遗传|组学|研究设计",
        "发现队列和验证队列并排布置，再用人群风险分布说明研究如何定义冠心病韧性。"
    ],
    "10.1016/j.jacadv.2026.102968": [
        "癌症幸存者|多重暴露|人群研究",
        "用九个图标说明风险因素，再把三项结局的估计并排呈现。"
    ]
}

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
        if doi in EDITORIAL:
            tags, row[5] = EDITORIAL[doi]
            row[4] = '|'.join(dict.fromkeys((row[4] + '|' + tags).split('|')))
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
            if dimensions != expected:
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
