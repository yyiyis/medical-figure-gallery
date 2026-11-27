"""Merge historical scans and publish photo-by-photo reviewed source figures."""

import argparse
from datetime import datetime
import json
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from publish_history import apply_report, write_review_summary
from scan_gallery import INDEX, image_size, json_section, request, set_section, update_stamp

BASE = Path('data/history-2026-11-27.json')
SUPPLEMENT = Path('data/history-supplement-2026-11-27.json')

# DOI, site title, tags, description of the figure, and inspected source dimensions.
CURATED = [
    ('10.1021/ehp.6c00055', '把重复颗粒物暴露和肺功能变化放在同一张图上',
     '环境健康|空气污染|PM2.5|人体控制暴露|图文摘要|多面板组图',
     '三栏分别展示人体暴露舱、三天肺功能的变化及按性别分层的结果；用图标提示每个面板所测的结局。', (1505, 558)),
    ('10.1016/j.jacadv.2026.103192', '急性冠脉综合征住院后痴呆的随访设计',
     '老龄化|心血管|认知|队列研究|研究流程图|竞争风险',
     '四个比较组先以颜色和图标区分，再连接到共同结局与随访，底部按相同颜色对齐三个风险比较。', (1600, 2071)),
    ('10.1093/eurheartj/ehag562', '癌症生存者的心血管风险模型怎么比较',
     '心血管|肿瘤|风险预测|荟萃分析|组图',
     '分区呈现通用模型与癌症专用模型，同一行并列适用结局、样本信息和合并判别指标。', (1600, 1619)),
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
    ('10.1093/ehjdh/ztag147', '用 MIMIC-IV 验证心电图预测模型',
     'MIMIC-IV|心血管|风险预测|外部验证|多面板组图',
     '按研究设计、判别能力和校准组织三栏，用同色标记外部数据，并将应用条件独立放在底部。', (1600, 978)),
    ('10.1186/s12940-026-01327-2', '脐带血 PFAS 与儿童神经发育',
     '暴露组|生命历程|PFAS|上海出生队列|队列研究|时间轴',
     '将脐带血的暴露测量和两岁时的发育评估连接到同一流程，并单列研究结局。', (1600, 724)),
    ('10.1021/acs.jproteome.6c00385', '临床蛋白组筛选到脓毒症判别',
     '蛋白组|组学|研究流程图',
     '样本、蛋白组筛选和风险判别从左到右排列，用一致色块标记研究阶段。', (1254, 540)),
    ('10.1093/ehjqcco/qcag113', '早发房颤的遗传与临床表型',
     '心血管|基因组|医学插画|概念与方法示意图',
     '将重叠的基因型与表型聚在中轴，右侧依次给出临床解释步骤。', (1600, 843)),
    ('10.1007/s10654-026-01436-9', '新生儿维生素 D 与自身免疫结局',
     '生命历程|队列研究|研究流程图|地理地图',
     '地图交代人群来源，再用并列的比较路线说明主要分析和负对照。', (1599, 897)),
    ('10.1186/s13073-026-01668-0', '多组学描绘糖尿病心肌',
     '多组学|心血管|代谢健康|研究流程图',
     '通过组织采样、不同组学测量和结果组图串起多组学证据。', (1985, 1104)),
    ('10.1016/j.cmet.2025.12.004', '脂肪性肝病的昼夜代谢图谱',
     '昼夜节律|代谢组|肝病|概念与方法示意图',
     '以肝脏和昼夜循环组织图面，用连接线标出不同代谢过程的变化。', (1600, 1544)),
    ("10.1016/j.jacasi.2025.11.016", "GPS-CAD 跨国冠心病队列的设计", "心血管|多国研究|队列研究|研究流程图|GPS-CAD", "先用国旗交代参与地，再按顺序组织采集、模型构建和验证。", (3446, 4138)),
    ("10.1016/j.jacasi.2026.05.016", "房颤患者多病共存状态的变化", "多病共存|队列研究|房颤|状态转移|COOL-AF", "用三种颜色表示多病共存恶化、稳定和改善，流线从随访变化连到临床结局。", (3446, 3087)),
    ("10.1016/j.jacasi.2026.07.034", "西太平洋卒中负担、趋势与不平等", "GBD|环境健康|脑卒中|地理比较|分解分析|多面板组图", "以四格分别展示区域负担、负担变化的分解、不平等趋势和不同指数的关系。", (3446, 4295)),
    ("10.1016/j.jacasi.2025.10.022", "泰国老年队列的生活方式与心血管转归", "健康老龄化|心血管|队列研究|地理地图|时间轴|HART", "区域地图和雷达图用同一分层对照，纵向框架再呈现随访与诊断后的行为变化。", (3446, 4771)),
    ("10.1016/j.jacc.2026.05.029", "不用造影剂评估心肌瘢痕", "心血管|影像|多中心队列|研究流程图", "把多中心样本和成像方法放在结果前，配对展示不同影像方法对同一问题的判断。", (3446, 2563)),
    ("10.1016/j.jacc.2026.02.5116", "常规心脏 CT 影像组学与心衰预测", "心血管|影像组学|预测与验证|队列研究", "把取像、脂肪表型提取和后续心衰风险估计按分析顺序组织。", (3446, 2490)),
    ("10.1016/j.jacadv.2025.102481", "空气污染的代谢特征与心血管结局", "暴露组|环境健康|代谢组|心血管|队列研究", "以环境暴露、代谢特征和主要心血管事件展示同一套人群研究的三层信息。", (3446, 3154)),
    ("10.1093/ehjopen/oeag163", "代谢物、性别与房颤风险", "组学|代谢组|分层分析|心血管|队列研究", "从代谢物的由来出发，依次排研究设计、分性别的风险估计和可读的图示结论。", (1600, 1068)),
    ("10.1093/ehjdh/ztag149", "用全球心电图数据训练年龄预测模型", "数字健康|心电图|老龄化|预测与验证|研究流程图", "把全球数据分布、模型框架和评估放在同一条阅读线上，下方用不同小图解释预测表现。", (1600, 1099)),
    ("10.1093/ehjopen/oeag149", "冠心病患者的生物心理社会分群", "心血管|分群|队列研究|研究流程图", "把分群所用指标集中在左侧，然后按同一顺序标出各人群及随访风险。", (1600, 605)),
    ("10.1093/ehjdh/ztag144", "睡眠分期心率变异性与心血管风险", "心血管|老龄化|睡眠|心电图|多面板组图", "三列依次说明睡眠分期特征、聚类和新增的风险评估能力，各列底部归纳结果。", (1600, 1459)),
    ("10.1016/j.jacadv.2026.103198", "退伍军人队列的心衰表型与转归", "心血管|队列研究|多面板组图|状态转移", "在同一图上分区呈现病例识别、风险比较和不同心衰表型的转归路径。", (1600, 1260)),
    ("10.1093/ehjdh/ztag132", "用可穿戴信号描绘心血管事件的时间", "数字健康|心血管|队列研究|时间轴|研究设计", "把连续监测与临床事件对齐在同一时间轴，旁边列出不同生理信号及对应结局。", (1600, 978)),
    ("10.1016/j.jacadv.2026.103110", "社区社会经济条件与心衰再入院", "心血管|社会环境|队列研究|概念图", "用三个扇区组织社区、医疗和个人层因素，再连到临床随访的主要比较。", (1600, 1216)),
    ("10.1093/ehjdh/ztag128", "UK Biobank 高血压的多时点风险预测", "UK Biobank|队列研究|数字健康|预测与验证|热图", "先呈现预测时点和模型，再用一排小热图对齐各时间窗的解释结果。", (1599, 1022)),
    ("10.1093/ehjdh/ztag114", "车载连续生理监测的队列设计", "数字健康|队列研究|研究设计|多面板组图", "把人群、研究流程和车内测量分成三栏，颜色区分驾驶情景、测量设备和结局。", (1600, 1111)),
]

PUBLISHER_ORIGINALS = {
    "10.1016/j.jacasi.2025.11.016": "https://ars.els-cdn.com/content/image/1-s2.0-S2772374725006957-ga1_lrg.jpg",
    "10.1016/j.jacasi.2026.05.016": "https://ars.els-cdn.com/content/image/1-s2.0-S2772374726003558-ga1_lrg.jpg",
    "10.1016/j.jacasi.2026.07.034": "https://ars.els-cdn.com/content/image/1-s2.0-S2772374726006277-ga1_lrg.jpg",
    "10.1016/j.jacasi.2025.10.022": "https://ars.els-cdn.com/content/image/1-s2.0-S2772374725006416-ga1_lrg.jpg",
    "10.1016/j.jacc.2026.05.029": "https://ars.els-cdn.com/content/image/1-s2.0-S0735109726066532-ga1_lrg.jpg",
    "10.1016/j.jacc.2026.02.5116": "https://ars.els-cdn.com/content/image/1-s2.0-S0735109726056524-ga1_lrg.jpg",
    "10.1016/j.jacadv.2025.102481": "https://ars.els-cdn.com/content/image/1-s2.0-S2772963X2500910X-ga1_lrg.jpg",
}

PLOS_CVD_DOI = '10.1371/journal.pmed.1005263'
PLOS_CVD_IMAGE = 'https://pmc-oa-opendata.s3.amazonaws.com/PMC13686484.1/pmed.1005263.g001.webp'

NATURE_HEAT_DOI = '10.1038/s44360-026-00220-z'
NATURE_HEAT_IMAGE = 'https://media.springernature.com/original/springer-static/image/art%3A10.1038%2Fs44360-026-00220-z/MediaObjects/44360_2026_220_Fig1_HTML.png'


MC_DOI = '10.1002/alz.71821'


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


NATURE_CLOCK_IMAGE = 'https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs42255-026-01504-0/MediaObjects/42255_2026_1504_Fig3_HTML.png'


def reviewed_rows(reports, existing):
    reviewed = []
    archive = {row[10]['doi'].casefold(): row for report in reports for row in report['items']}
    known = {row[6] for row in existing}
    for doi, title, tags, note, dimensions in CURATED:
        entry = archive[doi]
        if entry[6] not in known:
            row = [*entry[:3], title, tags, note, *entry[6:10], dict(entry[10])]
            if doi in PUBLISHER_ORIGINALS:
                row[7] = PUBLISHER_ORIGINALS[doi]
                row[8] = row[8].replace('PubMed Central 收录版', '出版社原图')
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
    mc_source = 'https://doi.org/' + MC_DOI
    if mc_source not in known:
        reviewed.append(([
            'figures', 'Alzheimer’s & Dementia', 2026, '中英美三队列的衰弱与认知随访',
            '多国多队列|CHARLS|HRS|ELSA|老龄化|认知|时间轴|研究流程图',
            '上半部用共同时间轴对齐三个队列的暴露与结局，下半部以同一配色说明各队列的纳入与排除。图 1。',
            mc_source, 'https://pmc-oa-opendata.s3.amazonaws.com/PMC13562614.1/ALZ-22-e71821-g004.webp',
            'Wang 等 · Alzheimer’s & Dementia 图 1', 'by', {'doi':MC_DOI, 'published':'2026-09-10'},
        ], (840, 911)))
    heat_source = 'https://doi.org/' + NATURE_HEAT_DOI
    if heat_source not in known:
        reviewed.append(([
            'figures', 'Nature Health', 2026, '欧洲城市高温死亡的时间与空间分布',
            '环境健康|公共卫生|地理地图|多面板组图|气候归因',
            '图 1 上方在同一时间轴比较两种气候情景，下方以城市地图并列死亡率和人为变暖归因比例。',
            heat_source, NATURE_HEAT_IMAGE,
            'Barnes 等 · Nature Health 图 1 · 底图 Natural Earth', 'by',
            {'doi':NATURE_HEAT_DOI, 'published':'2026-10-31'},
        ], (1817, 1299)))
    plos_source = 'https://doi.org/' + PLOS_CVD_DOI
    if plos_source not in known:
        reviewed.append(([
            'figures', 'PLOS Medicine', 2026, '给心血管风险模型画一张坐标图',
            '心血管|组学|风险预测|概念与方法示意图',
            '横轴是从亚临床病变到心衰的疾病进程，纵轴按预测数据由易到难排列，代表性模型放到对应位置。图 1。',
            plos_source, PLOS_CVD_IMAGE,
            'Tang、Gao · PLOS Medicine 图 1 · 图标来自 Openclipart、Wikimedia Commons 和 NIH/NHLBI',
            'by', {'doi':PLOS_CVD_DOI,'published':'2026-10-21'},
        ], (1600, 996)))
    landman_doi = '10.1038/s42255-026-01589-7'
    landman_source = 'https://doi.org/' + landman_doi
    if landman_source not in known:
        reviewed.append(([
            'figures', 'Nature Metabolism', 2026, '用环形条形图对照儿童心肾代谢表型',
            '老龄化|生命历程|组学|代谢健康|蛋白组|多面板组图|环形条形图',
            '六个面板沿同一圆周排列指标，按肥胖、血压、血糖、血脂、肾脏和肝脏领域配色，方便比较六个潜在因子的载荷。图 4。',
            landman_source, 'https://pmc-oa-opendata.s3.amazonaws.com/PMC13597307.1/42255_2026_1589_Fig4_HTML.webp',
            'Landman 等 · Nature Metabolism 图 4', 'by',
            {'doi':landman_doi,'published':'2026-09-11'},
        ], (1600, 1045)))
    clock_doi = '10.1038/s42255-026-01504-0'
    clock_source = 'https://doi.org/' + clock_doi
    if clock_source not in known:
        reviewed.append(([
            'figures', 'Nature Metabolism', 2026, '把不同班次的进食记录画成时钟',
            '代谢健康|时间营养|昼夜节律|数字健康|多面板组图|极坐标图',
            '左列的四个时钟并排显示不同班次的进食时刻，右侧用同一时间刻度比较进食窗口的分布。图 3。',
            clock_source, NATURE_CLOCK_IMAGE,
            'Tran 等 · Nature Metabolism 图 3', 'by',
            {'doi':clock_doi,'published':'2026-04-23'},
        ], (1731, 2571)))
    if 'https://doi.org/10.1093/ije/dyag151' not in known:
        reviewed.append(([
            'figures', 'International Journal of Epidemiology', 2026, '欧洲职业暴露队列如何分布',
            '暴露组|职业暴露|多国多队列|OMega-X|地理地图',
            '地图用圆点大小表示各国所纳入队列的总样本量，并用颜色和标注区分单国及多国队列。图 1。',
            'https://doi.org/10.1093/ije/dyag151',
            'https://pmc-oa-opendata.s3.amazonaws.com/PMC13487632.1/dyag151f1.webp',
            'Turner 等 · International Journal of Epidemiology 图 1',
            'by-nc', {'doi':'10.1093/ije/dyag151', 'published':'2026-08-19'},
        ], (1385, 1525)))
    if 'https://doi.org/10.1093/aje/kwag172' not in known:
        reviewed.append(([
            'figures', 'American Journal of Epidemiology', 2026, '把个人与地区的社会暴露放在同一张热图里',
            '社会流行病学|多病共存|CCHS|加拿大社区健康调查|热图|队列研究',
            '左侧按个人调查和地区人口普查分层，右侧并列男女六类社会暴露画像。深浅和颜色方向表示相对总体均值的偏离。图 2。',
            'https://doi.org/10.1093/aje/kwag172',
            'https://pmc-oa-opendata.s3.amazonaws.com/PMC13733519.1/kwag172f2.webp',
            'Giesinger 等 · American Journal of Epidemiology 图 2',
            'by-nc', {'doi':'10.1093/aje/kwag172', 'published':'2026-07-18'},
        ], (869, 1128)))
    if 'https://doi.org/10.1093/exposome/osag002' not in known:
        reviewed.append(([
            'figures', 'Exposome', 2026, '可穿戴采样器如何记录环境暴露',
            '环境健康|暴露组|可穿戴|概念与方法示意图',
            '左侧展示佩戴采样器的实际场景，右侧放大对应位置，解释环境中的化合物如何到达采样材料。图 5。',
            'https://doi.org/10.1093/exposome/osag002',
            'https://pmc-oa-opendata.s3.amazonaws.com/PMC13340902.1/nihms-2190067-f0005.jpg',
            'Okeme 等 · Exposome 图 5（PMC 收录的作者终稿）',
            'by-nc', {'doi':'10.1093/exposome/osag002','published':'2026-01-29'},
        ], (1800, 792)))
    for row, dimensions in reviewed:
        source = row[7]
        allowed = source.startswith('https://pmc-oa-opendata.s3.amazonaws.com/')
        allowed = allowed or source == PUBLISHER_ORIGINALS.get(row[10]['doi']) or source in {NATURE_HEAT_IMAGE, NATURE_CLOCK_IMAGE}
        if row[9] not in {'by','by-nc','by-nc-nd'} or not allowed:
            raise ValueError(f'Unexpected source or licence for {row[6]}')
        payload = request(row[7], limit=8_000_001)
        if len(payload) > 8_000_000 or image_size(payload) != dimensions:
            raise ValueError(f'Unexpected source dimensions for {row[6]}')
        doi = row[10]['doi']
        extension = Path(urlsplit(source).path).suffix.lower()
        if extension not in {'.webp', '.jpg', '.jpeg', '.png'}:
            raise ValueError(f'Unexpected file type for {row[6]}')
        filename = doi.split('/')[-1].replace('.', '-') + extension
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
        reviewed_dois = [entry[0] for entry in CURATED] + [MC_DOI, NATURE_HEAT_DOI, PLOS_CVD_DOI, '10.1038/s42255-026-01589-7', '10.1038/s42255-026-01504-0', '10.1093/ije/dyag151', '10.1093/aje/kwag172', '10.1093/exposome/osag002']
        if all('https://doi.org/' + doi in present for doi in reviewed_dois):
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
