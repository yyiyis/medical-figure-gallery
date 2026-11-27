"""Merge historical scans and publish photo-by-photo reviewed source figures."""

import argparse
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from publish_history import apply_report, write_review_summary
from scan_gallery import INDEX, image_size, json_section, request, set_section, update_stamp

BASE = Path('data/history-2026-11-27.json')
SUPPLEMENT = Path('data/history-supplement-2026-11-27.json')

# DOI, site title, tags, description of the figure, and inspected source dimensions.
CURATED = [
    ('10.1016/j.envint.2026.110581', '孕期室内环境与身心状态',
     '环境健康|早期暴露|孕期|暴露组',
     '三列分别安排室内暴露来源、孕期测量结果和实际干预场景，用图标区分三类环境指标。', (1600, 735)),
    ('10.1016/j.jacadv.2026.103303', '两种心肌瘢痕影像结果的对照',
     '心血管|桑基图|比较研究',
     '上方用桑基图连接两种影像的分类结果，下方对齐各瘢痕亚型的诊断指标。', (1600, 1089)),
    ('10.1016/j.jacadv.2026.103291', '从纵向病历构建先心病知识图谱',
     '心血管|研究流程图|知识图谱|纵向病历',
     '左到右展示病历输入、图谱表示和临床用途，下方对齐训练、验证和泛化检验。', (1599, 997)),
    ('10.1016/j.jacadv.2026.103278', '先天性心脏病的生命历程与非心脏多病共存',
     '生命历程|队列研究|UK Biobank|心血管|多病共存',
     '并列病例与一般人群，通过发病时间曲线和按器官系统排列的风险表呈现长期疾病负担。', (1600, 1070)),
    ('10.1093/ehjdh/ztag152', '心脏病学人工智能证据地图',
     '数字健康|系统综述|桑基图|心血管',
     '桑基图连接应用类型、数据模态与临床目标，条形图叠加各专科的证据数量和验证等级。', (1600, 1187)),
    ('10.1016/j.lanwpc.2026.101983', '乙肝病毒标志物变化与长期结局',
     '感染病学|队列研究|时间轴|多面板组图',
     '上方放随访时间轴与匹配设计，下方把肝病、癌症死亡、心血管死亡和疾病负担对齐。', (1284, 886)),
    ('10.1093/ehjopen/oeag151', '肥胖分层与心电结构改变',
     'UK Biobank|队列研究|心血管|代谢健康|肥胖',
     '按肥胖的新定义划分队列，用相同分层顺序组织心律失常累积风险和结构表型。', (1600, 1416)),
    ('10.1093/eurheartj/ehag519', '全谷物剂量与心代谢指标的证据汇总',
     '心血管|代谢健康|荟萃分析|森林图',
     '把共同的剂量刻度、不同代谢指标及证据等级排在同一框架内。', (1600, 1692)),
    ('10.1016/j.ebiom.2026.106542', '从 DNA 甲基化与表达组寻找慢性肾病信号',
     '组学|队列研究|表观遗传|研究流程图|慢性肾病',
     '将人群入组置顶，中段并列组学测量和关联分析，用编号把每个分析接到对应的结果。', (1600, 1130)),
    ('10.1183/13993003.01162-2026', '长新冠不同表型的呼吸道微生物组',
     '队列研究|组学|感染病学|呼吸医学|研究流程图',
     '左侧以时间轴交代多中心随访与采样，右侧把微生物组、表型和炎症指标放在对应的行。', (1600, 924)),
    ('10.1093/cid/ciag473', '原生关节感染的诊治综述图',
     '感染病学|概念与方法示意图|临床综述|医学插画',
     '关节插画居中，病因与危险因素分列，诊断、治疗及结局放在下方连续区域。', (1600, 1789)),
    ('10.1021/acs.est.6c03113', '孕期 PFAS、母体 DNA 甲基化与出生体格',
     '暴露组|PFAS|孕期|组学|表观遗传|环境健康|队列研究',
     '三列分别表示早期暴露、甲基化结果和出生结局，箭头对应论文中的直接及间接效应。', (1983, 1006)),
    ('10.1161/hypertensionaha.126.27526', '降压靶点与脂肪性肝病的遗传工具研究',
     '组学|孟德尔随机化|代谢健康|心血管|研究流程图',
     '平行排列遗传数据、工具变量与多来源证据，突出各方法的用途和同方向结果。', (1600, 1616)),
    ('10.1007/s11357-025-02090-x', '长寿队列的外周血转录组工作流',
     '老龄化|长寿|组学|转录组|队列研究|研究流程图',
     '两个长寿相关队列出发，分别连接时钟、死亡风险特征与衰老特征，再接到一般人群评估。', (1600, 803)),
]


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def combine(registry, reports):
    names = [j['name'] for group in registry['groups'] for j in group['journals']]
    coverage = {}
    items = {}
    for report in reports:
        if (report['mode'], report['start'], report['end']) != ('backfill', registry['start'], registry['end']):
            raise ValueError('Historical report does not match the stated first-publication dates')
        for entry in report['results']:
            name = entry['name']
            if name not in names:
                raise ValueError(f'Unregistered journal: {name}')
            if name not in coverage or not entry['errors']:
                coverage[name] = entry
        for row in report['items']:
            items.setdefault(row[10]['doi'].casefold(), row)
    results = [coverage.get(name, {'name':name, 'counts':{}, 'errors':['待完成历史目录盘点']}) for name in names]
    return {**reports[0], 'results': results, 'items': list(items.values()), 'candidates': len(items)}


def reviewed_rows(reports, existing):
    reviewed = []
    archive = {row[10]['doi'].casefold(): row for report in reports for row in report['items']}
    known = {row[6] for row in existing}
    for doi, title, tags, note, dimensions in CURATED:
        entry = archive[doi]
        if entry[6] not in known:
            row = [*entry[:3], title, tags, note, *entry[6:10], dict(entry[10])]
            reviewed.append((row, dimensions))
    helix = '10.1136/bmjopen-2026-122608'
    helix_source = 'https://doi.org/' + helix
    if helix_source not in known:
        reviewed.append(([
            'figures', 'BMJ Open', 2026, 'HELIX 暴露组队列的地理分布与随访',
            '生命历程|暴露组|队列研究|地理地图|时间轴|组学',
            '图 1 把欧洲六个队列的位置和孕期、儿童期、青春期的样本与测量放在同一视野。',
            helix_source, 'https://pmc-oa-opendata.s3.amazonaws.com/PMC13504928.1/bmjopen-16-8-g001.webp',
            'Montazeri 等 · BMJ Open 图 1', 'by', {'doi':helix, 'published':'2026-08-20'},
        ], (1216, 448)))
    for row, dimensions in reviewed:
        if row[9] not in {'by','by-nc','by-nc-nd'} or not row[7].startswith('https://pmc-oa-opendata.s3.amazonaws.com/'):
            raise ValueError(f'Unexpected source or licence for {row[6]}')
        payload = request(row[7], limit=8_000_001)
        if len(payload) > 8_000_000 or image_size(payload) != dimensions:
            raise ValueError(f'Unexpected source dimensions for {row[6]}')
        doi = row[10]['doi']
        filename = doi.split('/')[-1].replace('.', '-') + '.webp'
        reference = Path('assets/reference') / filename
        target = INDEX.parent / reference
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        row[7] = reference.as_posix()
        row[10].update(width=dimensions[0], height=dimensions[1])
        row[10].pop('url', None)
    return [row for row, _ in reviewed]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--selection', default='')
    parser.add_argument('--if-new', action='store_true')
    args = parser.parse_args()
    reports = [load(BASE)]
    if SUPPLEMENT.exists():
        reports.append(load(SUPPLEMENT))
    if args.report and args.report not in (BASE, SUPPLEMENT):
        reports.append(load(args.report))
    document = INDEX.read_text(encoding='utf-8')
    if args.if_new:
        present = {row[6] for row in json_section(document, 'catalog')}
        if all('https://doi.org/' + entry[0] in present for entry in CURATED):
            return
    registry = json_section(document, 'journal-registry')
    medicine = next(group for group in registry['groups'] if group['title'] == '综合医学')
    if all(journal['name'] != 'BMJ Open' for journal in medicine['journals']):
        medicine['journals'].append({'name':'BMJ Open', 'pubmed':'BMJ Open'})
        document = set_section(document, 'journal-registry', registry)
    combined = combine(registry, reports)
    stamp = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    updated, chosen = apply_report(document, combined, args.selection, stamp)
    catalogue = json_section(updated, 'catalog')
    reviewed = reviewed_rows(reports, catalogue)
    progress = json_section(updated, 'collection-report')
    latest = progress['latest']
    latest['candidates'] += sum(row[0] == 'abstract' for row in reviewed)
    updated = set_section(set_section(updated, 'catalog', reviewed + catalogue), 'collection-report', progress)
    INDEX.write_text(update_stamp(updated, progress['history'], latest), encoding='utf-8')
    print(f"Merged {sum(not x['errors'] for x in combined['results'])} verified journal scans with {len(combined['items'])} candidates.")
    print(f'Added {len(reviewed)} manually sourced figures and {len(chosen)} explicitly selected abstracts.')
    if args.report:
        write_review_summary(load(args.report))


if __name__ == '__main__':
    main()
