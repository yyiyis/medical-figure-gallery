/* Language switch and figure translations. */
(() => {
  const title = document.querySelector('header h1');
  if (!title || document.querySelector('#gallery-language')) return;

  const exact = new Map([
    ['医学期刊图集', 'Medical Figure Gallery'],
    ['浏览图文摘要、正文组图和期刊封面。点图可在本页放大。', 'Browse graphical abstracts, article figures, and journal covers. Select a figure to enlarge it.'],
    ['本图集整理已公开发表的文献图表，供个人学习与科研作图参考。每张图标明出处及适用许可，转载或商用请遵循相应条款。', 'This gallery brings together published research figures for personal study and reference. Each image lists its source and applicable licence. Follow the licence terms when reusing an image.'],
    ['期刊范围', 'Journal coverage'],
    ['按学科浏览期刊。已收录的图片可在本页查看。', 'Browse journals by discipline. Available figures can be previewed here.'],
    ['查看逐刊盘点', 'View coverage by journal'],
    ['目录条目涵盖文章及其他类型记录。候选图须复核许可、清晰度和作图参考价值。待核对项包括首次线上日期、许可、原图缺失和分辨率。', 'Indexed records include articles and other publication types. Figures are reviewed for licensing, legibility, and design value. Pending records may require checks on publication date, licence, image availability, or resolution.'],
    ['2026 年历史目录扫描', '2026 journal archive coverage'],
    ['期刊', 'Journal'], ['目录条目', 'Indexed records'], ['图文摘要候选', 'Graphical abstract candidates'],
    ['待核对', 'Pending checks'], ['状态', 'Status'], ['已读目录', 'Indexed'], ['暂无预览', 'No preview yet'],
    ['2026 原刊归档', '2026 journal archive'],
    ['综合医学', 'General Medicine'], ['心血管病学', 'Cardiovascular Medicine'],
    ['流行病学与公共卫生', 'Epidemiology and Public Health'], ['环境健康', 'Environmental Health'],
    ['老年医学与老龄化研究', 'Geriatrics and Aging'], ['内分泌与代谢', 'Endocrinology and Metabolism'],
    ['神经病学与脑健康', 'Neurology and Brain Health'], ['呼吸医学', 'Respiratory Medicine'],
    ['感染病学', 'Infectious Diseases'], ['数字医学', 'Digital Medicine'],
    ['遗传学与组学', 'Genetics and Omics'], ['综合科学与生命科学', 'General and Life Sciences'],
    ['图片类别', 'Figure types'], ['全部', 'All'], ['期刊封面', 'Journal covers'],
    ['图文摘要', 'Graphical abstracts'], ['正文组图', 'Article figures'], ['全部期刊', 'All journals'],
    ['筛选期刊', 'Filter by journal'], ['搜索图集', 'Search the gallery'],
    ['搜索，例如 UKB、组学或桑基图', 'Search, e.g. UKB, omics, or Sankey'],
    ['清除筛选', 'Clear filters'], ['包含仅有出处的条目', 'Include source-only entries'],
    ['单栏看大图', 'Single-column view'], ['医学期刊图片', 'Medical journal figures'],
    ['找不到匹配的样例。可以换个关键词或清除筛选。', 'No matching figures. Try another keyword or clear the filters.'],
    ['没找到匹配的样例。可以换个关键词或清除筛选。', 'No matching figures. Try another keyword or clear the filters.'],
    ['主题', 'Topic'], ['全部主题', 'All topics'], ['研究设计', 'Study design'], ['全部设计', 'All study designs'],
    ['数据来源', 'Data source'], ['全部数据来源', 'All data sources'],
    ['作图方式', 'Figure design'], ['全部作图方式', 'All figure designs'],
    ['心血管', 'Cardiovascular'], ['组学', 'Omics'], ['老龄化', 'Aging'], ['衰老', 'Biological aging'],
    ['代谢健康', 'Metabolic health'], ['神经与认知', 'Neurology and cognition'], ['认知', 'Cognition'],
    ['肿瘤', 'Oncology'], ['数字健康', 'Digital health'], ['公共卫生', 'Public health'],
    ['生命历程', 'Life course'], ['队列研究', 'Cohort study'], ['随机试验', 'Randomized trial'],
    ['病例对照', 'Case-control'], ['病例交叉', 'Case-crossover'], ['横断面', 'Cross-sectional'],
    ['系统综述与荟萃分析', 'Systematic review and meta-analysis'],
    ['预测与验证', 'Prediction and validation'], ['定性研究', 'Qualitative study'],
    ['上海出生队列', 'Shanghai Birth Cohort'], ['研究流程图', 'Study workflow'], ['时间轴', 'Timeline'],
    ['森林图与点区间图', 'Forest and interval plots'], ['桑基图与状态转移', 'Sankey and state transitions'],
    ['地理地图', 'Geographic map'], ['分类树与网络图', 'Classification trees and networks'],
    ['概念与方法示意图', 'Concept or methods diagram'], ['多面板组图', 'Multi-panel figure'],
    ['热图', 'Heatmap'], ['图标与插画', 'Icons and illustrations'],
    ['原始出处 ↗', 'Original source ↗'], ['仅收录出处', 'Source link only'], ['图像未修改', 'Unmodified image'],
    ['原始尺寸', 'Actual size'], ['适应窗口', 'Fit to window'], ['关闭', 'Close'],
    ['图片预览', 'Figure preview'], ['图片加载中…', 'Loading figure…'], ['原图加载中…', 'Loading original…'],
    ['重试', 'Retry'], ['图片加载失败。', 'The image could not load.'],
    ['图片暂时无法加载，可打开原始出处。', 'The image is temporarily unavailable. See the original source.'],
    ['图片加载失败，可关闭后重试或打开原始出处。', 'The image could not load. Close and retry or open the original source.'],
  ]);

  const tagPairs = [
    ['人群研究','Population study'], ['暴露组','Exposome'], ['多国多队列','Multi-country cohorts'],
    ['多国研究','Multinational study'], ['地理比较','Geographic comparison'], ['多组学','Multi-omics'],
    ['代谢组','Metabolomics'], ['蛋白组','Proteomics'], ['基因组','Genomics'],
    ['转录组','Transcriptomics'], ['表观遗传','Epigenetics'], ['人群遗传','Population genetics'],
    ['影像组学','Radiomics'], ['医学插画','Medical illustration'], ['医学史','History of medicine'],
    ['空气污染','Air pollution'], ['职业暴露','Occupational exposure'], ['孕期','Pregnancy'],
    ['早期暴露','Early-life exposure'], ['人体控制暴露','Controlled human exposure'],
    ['剂量反应','Dose–response'], ['联合暴露','Joint exposures'], ['多重暴露','Multiple exposures'],
    ['连续暴露','Continuous exposure'], ['可穿戴','Wearables'], ['影像','Imaging'],
    ['心电图','Electrocardiography'], ['心衰','Heart failure'], ['房颤','Atrial fibrillation'],
    ['脑卒中','Stroke'], ['脑健康','Brain health'], ['慢性肾病','Chronic kidney disease'],
    ['肝病','Liver disease'], ['肥胖','Obesity'], ['睡眠','Sleep'], ['体力活动','Physical activity'],
    ['多病共存','Multimorbidity'], ['临床试验','Clinical trial'], ['临床队列','Clinical cohort'],
    ['多中心队列','Multicenter cohort'], ['队列设计','Cohort design'], ['临床综述','Clinical review'],
    ['系统综述','Systematic review'], ['荟萃分析','Meta-analysis'], ['生态学研究','Ecological study'],
    ['孟德尔随机化','Mendelian randomization'], ['外部验证','External validation'],
    ['风险预测','Risk prediction'], ['偏倚','Bias'], ['年龄效应','Age effects'],
    ['比较研究','Comparative study'], ['分解分析','Decomposition analysis'],
    ['多状态模型','Multistate model'], ['分层','Stratification'], ['分层分析','Stratified analysis'],
    ['再分类','Reclassification'], ['分群','Clustering'], ['组间比较','Group comparison'],
    ['结局','Outcomes'], ['疾病轨迹','Disease trajectories'], ['竞争风险','Competing risks'],
    ['社会流行病学','Social epidemiology'], ['社会环境','Social environment'], ['营养','Nutrition'],
    ['全球负担','Global burden'], ['城市环境','Urban environment'], ['极端天气','Extreme weather'],
    ['气候归因','Climate attribution'], ['生态学研究','Ecological study'], ['癌症幸存者','Cancer survivors'],
    ['健康老龄化','Healthy aging'], ['长寿','Longevity'], ['时间营养','Chrononutrition'],
    ['昼夜节律','Circadian rhythms'], ['纵向病历','Longitudinal health records'], ['实施研究','Implementation research'],
    ['加拿大社区健康调查','Canadian Community Health Survey'], ['开滦研究','Kailuan Study'],
    ['影像流行病学','Imaging epidemiology'], ['情景比较','Scenario comparison'],
    ['概念框架','Conceptual framework'], ['概念图','Concept diagram'], ['方法示意','Methods diagram'],
    ['网络图','Network diagram'], ['知识图谱','Knowledge graph'], ['分类图','Classification diagram'],
    ['多面板','Multi-panel'], ['组图','Composite figure'], ['桑基图','Sankey diagram'],
    ['趋势图','Trend chart'], ['状态转移','State transitions'], ['流程图','Flowchart'], ['信息图','Infographic'],
    ['森林图','Forest plot'], ['热图','Heatmap'], ['极坐标图','Polar chart'], ['环形图','Radial chart'],
    ['环形条形图','Radial bar chart'], ['封面','Cover'], ['封面设计','Cover design'],
    ['视觉隐喻','Visual metaphor'], ['综述','Review'],
  ];
  for (const [source, translation] of tagPairs) exact.set(source, translation);
  const cardTranslations = new Map([
  [
    "四国队列如何比较临床前与临床肥胖",
    "Comparing preclinical and clinical obesity across four national cohorts"
  ],
  [
    "图 2 让每个队列的两个圆环沿用同一配色，分别以全体参与者和符合综合体格肥胖标准者为分母，突出临床肥胖占比怎样变化。",
    "Figure 2 gives each cohort two rings in the same color. The outer comparison uses all participants as the denominator. The second uses those meeting composite anthropometric obesity criteria, showing how the share with clinical obesity changes."
  ],
  [
    "把重复颗粒物暴露和肺功能变化放在同一张图上",
    "Repeated particulate exposure and changes in lung function"
  ],
  [
    "三栏分别展示人体暴露舱、三天肺功能的变化及按性别分层的结果；用图标提示每个面板所测的结局。",
    "Three columns show the human exposure chamber, lung function over three days, and results by sex. Icons identify the outcomes in each panel."
  ],
  [
    "急性冠脉综合征住院后痴呆的随访设计",
    "Tracking dementia after hospitalization for acute coronary syndrome"
  ],
  [
    "四个比较组先以颜色和图标区分，再连接到共同结局与随访，底部按相同颜色对齐三个风险比较。",
    "Colors and icons distinguish four groups before they converge on a common outcome and follow-up. The same colors align three risk comparisons below."
  ],
  [
    "癌症生存者的心血管风险模型怎么比较",
    "Comparing cardiovascular risk models for cancer survivors"
  ],
  [
    "分区呈现通用模型与癌症专用模型，同一行并列适用结局、样本信息和合并判别指标。",
    "Separate blocks show general and cancer-specific models, with outcomes, sample information and pooled discrimination estimates aligned in the same row."
  ],
  [
    "用 MIMIC-IV 验证心电图预测模型",
    "Validating an ECG prediction model in MIMIC-IV"
  ],
  [
    "按研究设计、判别能力和校准组织三栏，用同色标记外部数据，并将应用条件独立放在底部。",
    "Three columns cover study design, discrimination and calibration. A consistent color marks the external data, and the bottom states the conditions for use."
  ],
  [
    "脐带血 PFAS 与儿童神经发育",
    "Cord-blood PFAS and child neurodevelopment"
  ],
  [
    "将脐带血的暴露测量和两岁时的发育评估连接到同一流程，并单列研究结局。",
    "A single workflow connects cord-blood exposure measurement to developmental assessment at age two. Outcomes are shown separately."
  ],
  [
    "临床蛋白组筛选到脓毒症判别",
    "From clinical proteomic screening to sepsis classification"
  ],
  [
    "样本、蛋白组筛选和风险判别从左到右排列，用一致色块标记研究阶段。",
    "Samples, proteomic screening and risk classification run left to right. Consistent blocks mark each stage."
  ],
  [
    "早发房颤的遗传与临床表型",
    "Genetic and clinical phenotypes of early-onset atrial fibrillation"
  ],
  [
    "将重叠的基因型与表型聚在中轴，右侧依次给出临床解释步骤。",
    "Overlapping genotypes and phenotypes are grouped along the center, with the steps of clinical interpretation to the right."
  ],
  [
    "新生儿维生素 D 与自身免疫结局",
    "Neonatal vitamin D and autoimmune outcomes"
  ],
  [
    "地图交代人群来源，再用并列的比较路线说明主要分析和负对照。",
    "A map establishes where the cohort comes from. Parallel paths show the main analysis and the negative control."
  ],
  [
    "多组学描绘糖尿病心肌",
    "Profiling diabetic myocardium with multi-omics"
  ],
  [
    "通过组织采样、不同组学测量和结果组图串起多组学证据。",
    "The figure connects tissue sampling, different omics measurements and composite results."
  ],
  [
    "脂肪性肝病的昼夜代谢图谱",
    "A circadian metabolic atlas of fatty liver disease"
  ],
  [
    "以肝脏和昼夜循环组织图面，用连接线标出不同代谢过程的变化。",
    "The liver and the daily cycle organize the graphic. Connecting lines mark changes in specific metabolic processes."
  ],
  [
    "GPS-CAD 跨国冠心病队列的设计",
    "Design of the multinational GPS-CAD coronary disease cohort"
  ],
  [
    "先用国旗交代参与地，再按顺序组织采集、模型构建和验证。",
    "Flags show the participating countries. The following panels trace data collection, model development and validation."
  ],
  [
    "房颤患者多病共存状态的变化",
    "Multimorbidity transitions in atrial fibrillation"
  ],
  [
    "用三种颜色表示多病共存恶化、稳定和改善，流线从随访变化连到临床结局。",
    "Three colors distinguish worsening, stable and improving multimorbidity. Flow lines connect changes during follow-up to clinical outcomes."
  ],
  [
    "西太平洋卒中负担、趋势与不平等",
    "Stroke burden, trends and inequality in the Western Pacific"
  ],
  [
    "以四格分别展示区域负担、负担变化的分解、不平等趋势和不同指数的关系。",
    "Four panels show regional burden, decomposition of changes, inequality trends and relationships between indices."
  ],
  [
    "泰国老年队列的生活方式与心血管转归",
    "Lifestyle and cardiovascular outcomes in older Thai adults"
  ],
  [
    "区域地图和雷达图用同一分层对照，纵向框架再呈现随访与诊断后的行为变化。",
    "Maps and radar charts use the same grouping. A longitudinal diagram shows follow-up and changes in behavior after diagnosis."
  ],
  [
    "不用造影剂评估心肌瘢痕",
    "Assessing myocardial scar without a contrast agent"
  ],
  [
    "把多中心样本和成像方法放在结果前，配对展示不同影像方法对同一问题的判断。",
    "The multicenter sample and imaging methods come first. Paired images show how different modalities address the same question."
  ],
  [
    "常规心脏 CT 影像组学与心衰预测",
    "Routine cardiac CT radiomics for heart failure prediction"
  ],
  [
    "把取像、脂肪表型提取和后续心衰风险估计按分析顺序组织。",
    "Acquisition, fat phenotype extraction and estimation of later heart failure risk follow the order of analysis."
  ],
  [
    "空气污染的代谢特征与心血管结局",
    "Metabolic signatures of air pollution and cardiovascular outcomes"
  ],
  [
    "以环境暴露、代谢特征和主要心血管事件展示同一套人群研究的三层信息。",
    "Environmental exposure, metabolic signatures and major cardiovascular events form three layers of the same population study."
  ],
  [
    "代谢物、性别与房颤风险",
    "Metabolites, sex and atrial fibrillation risk"
  ],
  [
    "从代谢物的由来出发，依次排研究设计、分性别的风险估计和可读的图示结论。",
    "The graphic traces metabolite origins, study design, sex-specific estimates and a visual summary."
  ],
  [
    "用全球心电图数据训练年龄预测模型",
    "Training an age predictor on global ECG data"
  ],
  [
    "把全球数据分布、模型框架和评估放在同一条阅读线上，下方用不同小图解释预测表现。",
    "The geographic spread of the data, model architecture and evaluation follow one reading path. Small charts explain predictive performance below."
  ],
  [
    "冠心病患者的生物心理社会分群",
    "Biopsychosocial profiles in coronary heart disease"
  ],
  [
    "把分群所用指标集中在左侧，然后按同一顺序标出各人群及随访风险。",
    "The clustering inputs are grouped on the left. Profiles and follow-up risks use the same ordering across panels."
  ],
  [
    "睡眠分期心率变异性与心血管风险",
    "Sleep-stage heart rate variability and cardiovascular risk"
  ],
  [
    "三列依次说明睡眠分期特征、聚类和新增的风险评估能力，各列底部归纳结果。",
    "Three columns cover sleep-stage features, clustering and added value for risk assessment. Each ends with a brief finding."
  ],
  [
    "退伍军人队列的心衰表型与转归",
    "Heart failure phenotypes and outcomes in veterans"
  ],
  [
    "在同一图上分区呈现病例识别、风险比较和不同心衰表型的转归路径。",
    "Separate regions show how cases were identified, how risks were compared and how outcomes varied by phenotype."
  ],
  [
    "用可穿戴信号描绘心血管事件的时间",
    "Timing cardiovascular events using wearable signals"
  ],
  [
    "把连续监测与临床事件对齐在同一时间轴，旁边列出不同生理信号及对应结局。",
    "Continuous monitoring and clinical events share a timeline. The side panel lists physiological signals and corresponding outcomes."
  ],
  [
    "社区社会经济条件与心衰再入院",
    "Neighborhood socioeconomic conditions and heart failure readmission"
  ],
  [
    "用三个扇区组织社区、医疗和个人层因素，再连到临床随访的主要比较。",
    "Three sectors organize neighborhood, healthcare and individual factors, then link them to the main follow-up comparison."
  ],
  [
    "UK Biobank 高血压的多时点风险预测",
    "Predicting hypertension over multiple time horizons in UK Biobank"
  ],
  [
    "先呈现预测时点和模型，再用一排小热图对齐各时间窗的解释结果。",
    "Prediction horizons and models come first. A row of small heatmaps aligns interpretations across time windows."
  ],
  [
    "车载连续生理监测的队列设计",
    "Cohort design for continuous in-vehicle physiological monitoring"
  ],
  [
    "把人群、研究流程和车内测量分成三栏，颜色区分驾驶情景、测量设备和结局。",
    "Three columns cover participants, protocol and in-car measurements. Color distinguishes driving scenarios, devices and outcomes."
  ],
  [
    "中英美三队列的衰弱与认知随访",
    "Frailty and cognition across cohorts in China, the UK and the US"
  ],
  [
    "上半部用共同时间轴对齐三个队列的暴露与结局，下半部以同一配色说明各队列的纳入与排除。图 1。",
    "A shared timeline aligns exposures and outcomes across all three cohorts. The lower panels use the same colors for eligibility and exclusions. Figure 1."
  ],
  [
    "欧洲城市高温死亡的时间与空间分布",
    "When and where heat-related deaths occur in European cities"
  ],
  [
    "图 1 上方在同一时间轴比较两种气候情景，下方以城市地图并列死亡率和人为变暖归因比例。",
    "Figure 1 uses a shared timeline for two climate scenarios. Maps beneath compare mortality rates and fractions attributable to human-caused warming."
  ],
  [
    "给心血管风险模型画一张坐标图",
    "A two-axis map of cardiovascular risk models"
  ],
  [
    "横轴是从亚临床病变到心衰的疾病进程，纵轴按预测数据由易到难排列，代表性模型放到对应位置。图 1。",
    "The horizontal axis follows disease progression from subclinical changes to heart failure. The vertical axis orders models by how demanding their input data are. Figure 1."
  ],
  [
    "用环形条形图对照儿童心肾代谢表型",
    "Radial bars for childhood cardiometabolic phenotypes"
  ],
  [
    "六个面板沿同一圆周排列指标，按肥胖、血压、血糖、血脂、肾脏和肝脏领域配色，方便比较六个潜在因子的载荷。图 4。",
    "Six panels place indicators around the same circle. Colors group obesity, blood pressure, glycemia, lipids, kidney and liver measures to compare factor loadings. Figure 4."
  ],
  [
    "把不同班次的进食记录画成时钟",
    "Clock plots of eating patterns across work shifts"
  ],
  [
    "左列的四个时钟并排显示不同班次的进食时刻，右侧用同一时间刻度比较进食窗口的分布。图 3。",
    "Four clocks compare mealtimes across shifts. A common time scale on the right shows the distribution of eating windows. Figure 3."
  ],
  [
    "欧洲职业暴露队列如何分布",
    "Mapping occupational exposure cohorts across Europe"
  ],
  [
    "地图用圆点大小表示各国所纳入队列的总样本量，并用颜色和标注区分单国及多国队列。图 1。",
    "Circle size reflects total cohort size by country. Colors and labels distinguish national and multinational cohorts. Figure 1."
  ],
  [
    "把个人与地区的社会暴露放在同一张热图里",
    "A heatmap of individual and area-level social exposures"
  ],
  [
    "左侧按个人调查和地区人口普查分层，右侧并列男女六类社会暴露画像。深浅和颜色方向表示相对总体均值的偏离。图 2。",
    "The left separates survey and census measures. The right compares six exposure profiles by sex, with hue and intensity encoding deviations from the overall mean. Figure 2."
  ],
  [
    "可穿戴采样器如何记录环境暴露",
    "How a wearable sampler records environmental exposure"
  ],
  [
    "左侧展示佩戴采样器的实际场景，右侧放大对应位置，解释环境中的化合物如何到达采样材料。图 5。",
    "A photo shows how the device is worn. A close-up explains how environmental compounds reach the sampling material. Figure 5."
  ],
  [
    "从 DNA 甲基化与表达组寻找慢性肾病信号",
    "DNA methylation and gene expression signals in chronic kidney disease"
  ],
  [
    "将人群入组置顶，中段并列组学测量和关联分析，用编号把每个分析接到对应的结果。",
    "Enrollment comes first. Omics measurements and association analyses appear side by side, with numbers linking each analysis to its results."
  ],
  [
    "长新冠不同表型的呼吸道微生物组",
    "Airway microbiome profiles in long COVID"
  ],
  [
    "左侧以时间轴交代多中心随访与采样，右侧把微生物组、表型和炎症指标放在对应的行。",
    "A timeline on the left shows multicenter follow-up and sampling. Rows on the right align microbiome, phenotype and inflammatory measures."
  ],
  [
    "原生关节感染的诊治综述图",
    "A visual overview of native joint infection"
  ],
  [
    "关节插画居中，病因与危险因素分列，诊断、治疗及结局放在下方连续区域。",
    "A joint illustration anchors separate columns for causes and risk factors. The lower section follows diagnosis, treatment and outcomes."
  ],
  [
    "孕期 PFAS、母体 DNA 甲基化与出生体格",
    "Prenatal PFAS, maternal DNA methylation and size at birth"
  ],
  [
    "三列分别表示早期暴露、甲基化结果和出生结局，箭头对应论文中的直接及间接效应。",
    "Three columns show early exposure, methylation and birth outcomes. Arrows correspond to the estimated direct and indirect effects."
  ],
  [
    "降压靶点与脂肪性肝病的遗传工具研究",
    "Genetic proxies for blood pressure targets and fatty liver disease"
  ],
  [
    "平行排列遗传数据、工具变量与多来源证据，突出各方法的用途和同方向结果。",
    "Parallel tracks show genetic data, instruments and different evidence sources, clarifying what each method addresses and where results agree in direction."
  ],
  [
    "长寿队列的外周血转录组工作流",
    "Peripheral blood transcriptomics in longevity cohorts"
  ],
  [
    "两个长寿相关队列出发，分别连接时钟、死亡风险特征与衰老特征，再接到一般人群评估。",
    "Two longevity cohorts feed analyses of clocks, mortality signatures and aging features, followed by evaluation in the general population."
  ],
  [
    "孕期室内环境与身心状态",
    "Indoor exposures and well-being during pregnancy"
  ],
  [
    "三列分别安排室内暴露来源、孕期测量结果和实际干预场景，用图标区分三类环境指标。",
    "Columns show indoor exposure sources, measurements during pregnancy and practical intervention settings. Icons distinguish the three environmental domains."
  ],
  [
    "两种心肌瘢痕影像结果的对照",
    "Comparing two imaging measures of myocardial scar"
  ],
  [
    "上方用桑基图连接两种影像的分类结果，下方对齐各瘢痕亚型的诊断指标。",
    "A Sankey diagram links the two imaging classifications. Diagnostic metrics for scar subtypes are aligned below."
  ],
  [
    "从纵向病历构建先心病知识图谱",
    "Building a congenital heart disease knowledge graph from longitudinal records"
  ],
  [
    "左到右展示病历输入、图谱表示和临床用途，下方对齐训练、验证和泛化检验。",
    "The figure moves from records to graph representation and clinical uses, with model development, validation and generalization tests aligned below."
  ],
  [
    "先天性心脏病的生命历程与非心脏多病共存",
    "Congenital heart disease and noncardiac multimorbidity over the life course"
  ],
  [
    "并列病例与一般人群，通过发病时间曲线和按器官系统排列的风险表呈现长期疾病负担。",
    "Curves and organ-system risk tables compare long-term disease burden in cases and the general population."
  ],
  [
    "心脏病学人工智能证据地图",
    "An evidence map of artificial intelligence in cardiology"
  ],
  [
    "桑基图连接应用类型、数据模态与临床目标，条形图叠加各专科的证据数量和验证等级。",
    "A Sankey diagram connects applications, data modalities and clinical objectives. Bars display the amount and validation level of evidence by specialty."
  ],
  [
    "乙肝病毒标志物变化与长期结局",
    "Changes in hepatitis B markers and long-term outcomes"
  ],
  [
    "上方放随访时间轴与匹配设计，下方把肝病、癌症死亡、心血管死亡和疾病负担对齐。",
    "The follow-up timeline and matching design sit above aligned comparisons of liver disease, cancer deaths, cardiovascular deaths and disease burden."
  ],
  [
    "肥胖分层与心电结构改变",
    "Obesity categories and cardiac electrical and structural changes"
  ],
  [
    "按肥胖的新定义划分队列，用相同分层顺序组织心律失常累积风险和结构表型。",
    "The cohort follows updated obesity definitions. Cumulative arrhythmia risk and structural phenotypes use the same order of groups."
  ],
  [
    "全谷物剂量与心代谢指标的证据汇总",
    "Evidence on whole-grain dose and cardiometabolic markers"
  ],
  [
    "把共同的剂量刻度、不同代谢指标及证据等级排在同一框架内。",
    "A common dose scale aligns different metabolic markers and their evidence grades."
  ],
  [
    "HELIX 暴露组队列的地理分布与随访",
    "HELIX exposome cohorts: geography and follow-up"
  ],
  [
    "图 1 把欧洲六个队列的位置和孕期、儿童期、青春期的样本与测量放在同一视野。",
    "Figure 1 combines the locations of six European cohorts with samples and measurements collected in pregnancy, childhood and adolescence."
  ],
  [
    "热带气旋与急性冠脉综合征",
    "Tropical cyclones and acute coronary syndrome"
  ],
  [
    "把气旋路径和全国医院病例并排放，上方交代样本，下方并列呈现就医延迟、滞后风险和应对含义。",
    "Cyclone paths and nationwide hospital cases appear side by side. Panels below compare delays in seeking care, lagged risk and implications for response."
  ],
  [
    "儿童血压的遗传特征与成年健康",
    "Genetics of childhood blood pressure and adult health"
  ],
  [
    "左侧区分儿童发现与复现队列，并展示遗传重叠，右侧按器官归纳成年期结局。",
    "The left distinguishes childhood discovery and replication samples and shows genetic overlap. The right organizes adult outcomes by organ system."
  ],
  [
    "孕期母亲自身免疫病与子代心血管风险",
    "Maternal autoimmune disease and offspring cardiovascular risk"
  ],
  [
    "在同一张图里交代出生队列、父亲和表亲比较、可能的中介因素，并列展示估计值。",
    "A single figure presents birth cohorts, comparisons with fathers and cousins, potential mediators and the corresponding estimates."
  ],
  [
    "乳腺癌治疗随访中的心脏变化与联合组学",
    "Cardiac changes and multi-omics during breast cancer treatment"
  ],
  [
    "用随访时间轴区分同次和跨次访视的分析，再用上下两层区分统计方法与发现。",
    "A follow-up timeline separates within-visit and between-visit analyses. The upper and lower sections distinguish methods from findings."
  ],
  [
    "老年队列的代谢组与生活方式风险分层",
    "Metabolomic and lifestyle risk stratification in older adults"
  ],
  [
    "图 1 用四个色块依次展示队列设计、代谢组测量、BMI 与代谢健康分层，以及生活方式和代谢评分的联合分析。",
    "Four colored blocks show cohort design, metabolomic profiling, BMI and metabolic-health groups, and a joint analysis of lifestyle and metabolic scores. Figure 1."
  ],
  [
    "维米尔《地理学家》",
    "Vermeer’s The Geographer"
  ],
  [
    "2026 年 6 月号所用封面画作。期刊用绘画中的光与观察，引出早期显微镜和对微生物的认识。",
    "The June 2026 cover uses light and observation in the painting to introduce early microscopy and the study of microorganisms."
  ],
  [
    "从出生到成年早期的多域暴露测量",
    "Measuring multiple domains of exposure from birth to early adulthood"
  ],
  [
    "图 1 用同一条时间轴对齐四类暴露、不同时点的测量与 22 岁的 DNA 甲基化采样。",
    "Figure 1 puts four exposure domains, repeated assessments and DNA methylation sampling at age 22 on one timeline."
  ],
  [
    "化学暴露组网络的多层分群",
    "Hierarchical clustering in chemical exposome networks"
  ],
  [
    "图 2 用局部放大和嵌套矩形表现从总体网络到细分群落的层级，再用下排图比较群落特征。",
    "Figure 2 uses a zoomed view and nested rectangles to show communities within an overall network. Lower panels compare the communities."
  ],
  [
    "用九个图标说明风险因素，再把三项结局的估计并排呈现。",
    "Nine icons introduce the risk factors before three outcome estimates are shown side by side."
  ],
  [
    "发现队列和验证队列并排布置，再用人群风险分布说明研究如何定义冠心病韧性。",
    "Discovery and validation cohorts are shown in parallel. Risk distributions illustrate how coronary resilience is defined."
  ],
  [
    "上下两层分别交代暴露和结局定义，再并排展示两种社会经济地位定义对疾病转移估计的影响。",
    "Two rows define exposure and outcomes. Side-by-side results show how two definitions of socioeconomic status affect disease transition estimates."
  ],
  [
    "夜间光照与心脏结构和功能",
    "Nighttime light exposure and cardiac structure and function"
  ],
  [
    "把队列的夜间光照测量和心脏磁共振分析放在同一张摘要里。",
    "One abstract combines cohort light measurements with cardiac MRI analyses."
  ],
  [
    "人群多组学与表观遗传衰老的研究设计",
    "Design of a population multi-omics study of epigenetic aging"
  ],
  [
    "图 1 将数据来源、研究问题、主要分析和后续验证排成四列。",
    "Figure 1 presents data sources, research questions, primary analyses and subsequent validation in four columns."
  ],
  [
    "城市环境与 One Health 的概念框架",
    "A One Health framework for urban environments"
  ],
  [
    "图 1 用城市剖面连接多污染物暴露、建成环境、微气候和治理。",
    "Figure 1 uses a cross-section of a city to link multiple pollutants, the built environment, microclimate and governance."
  ],
  [
    "Brain Health 创刊号封面",
    "Inaugural cover of Brain Health"
  ],
  [
    "原刊封面将脑科学、实验室和身体活动放在同一景观中。期刊注明插图由 AI 辅助完成。",
    "The cover places brain science, laboratory work and physical activity in one landscape. The journal credits AI-assisted illustration."
  ],
  [
    "CRP 与一般人群的心血管风险",
    "C-reactive protein and cardiovascular risk in the general population"
  ],
  [
    "左栏交代人群和测量，右侧三列依次展示累积发病、调整后风险和增量预测价值。",
    "A left panel introduces the population and measurements. Three right panels show cumulative incidence, adjusted risk and added predictive value."
  ],
  [
    "联合生物标志物与 SCORE2",
    "Combining biomarkers with SCORE2"
  ],
  [
    "左侧交代队列和指标组合，右侧用两个并排的点区间图比较筛查识别人数和估计的用药效率。",
    "The left introduces the cohort and biomarker combinations. Two interval plots compare people identified by screening and estimated prescribing efficiency."
  ],
  [
    "多病共存指标的分类图",
    "A classification of multimorbidity indices"
  ],
  [
    "从疾病、药物等主干向外分叉，沿线标出怎样组合与加权，再把代表性指标放在各分支末端。",
    "Branches start from conditions and medicines, mark combinations and weighting methods, and end with representative indices."
  ],
  [
    "代谢年龄建模与验证",
    "Developing and validating a metabolomic age model"
  ],
  [
    "用三层分别讲模型开发、全样本应用和对 PREVENT 的增量预测。每层末端直接画出该步骤产出了什么。",
    "Three layers cover model development, full-cohort application and incremental performance over PREVENT. Each shows what the step produces."
  ],
  [
    "全身 MRI 队列的样本与数据构建",
    "Building a whole-body MRI cohort for analysis"
  ],
  [
    "并排的时间轴交代病例和对照的事件窗口。旁边用两个颜色分组说明影像与非影像数据怎么进入分析。",
    "Parallel timelines define event windows for cases and controls. Two color groups show how imaging and other data enter the analysis."
  ],
  [
    "老年人心血管健康轨迹与结局",
    "Cardiovascular health trajectories and outcomes in older adults"
  ],
  [
    "Central Illustration 把长期健康轨迹和随访结局放进一张图，适合参考重复测量队列的叙述顺序。",
    "The central illustration connects long-term cardiovascular health trajectories to outcomes in a repeated-measures cohort."
  ],
  [
    "PM₂.₅ 组分与心血管疾病",
    "PM₂.₅ components and cardiovascular disease"
  ],
  [
    "图文摘要压缩研究问题，正文再展开地域分布、暴露–反应和分层结果。",
    "The graphical abstract condenses the research question. Article figures expand on spatial distribution, exposure–response and stratified results."
  ],
  [
    "中国成人肥胖指标与风险阈值",
    "Obesity measures and risk thresholds in Chinese adults"
  ],
  [
    "用独立区块交代人群、肥胖指标和结局，把几种容易混淆的测量放在同一区域。",
    "Distinct blocks introduce the population, obesity measures and outcomes; related measurements are grouped for comparison."
  ],
  [
    "空气污染与 COPD、胃肠疾病的转归",
    "Air pollution and transitions involving COPD and gastrointestinal disease"
  ],
  [
    "左侧交代样本怎么筛，右侧画出不同疾病状态之间如何转移。",
    "The left shows sample selection. The right depicts transitions between disease states."
  ],
  [
    "更年期研究的方法与结果概览",
    "Methods and findings in menopause research"
  ],
  [
    "用小曲线先说明个体时间差异怎样把群体变化变平，再显示按距绝经时间对齐的实例。",
    "Small curves explain how individual timing differences flatten the group average, followed by an example aligned to time since menopause."
  ],
  [
    "老龄人群纵向数据建设中的挑战与应对",
    "Challenges and responses in building longitudinal aging data"
  ],
  [
    "把访谈结果排成四列，从数据建设阶段连到挑战、应对做法和政策优先项。流线让同一种做法能回应多个问题这一层关系可见。",
    "Four columns connect stages of data development to challenges, responses and policy priorities. Flows show how one response can address several challenges."
  ],
  [
    "膀胱癌治疗后的分组与临床转归",
    "Treatment groups and clinical outcomes in bladder cancer"
  ],
  [
    "用两张桑基图从不同起点追踪同一队列。左图按维持治疗分组，右图按既往治疗暴露类型分组，二者共用结局分类。",
    "Two Sankey diagrams follow the same cohort from different starting points: maintenance therapy and prior treatment exposure. Both use the same outcome categories."
  ],
  [
    "从心脏影像定义表型到比较风险",
    "From cardiac imaging phenotypes to risk comparisons"
  ],
  [
    "用同一组心脏示意图贯穿表型定义和风险对照，四格分别交代测量、临床结局、遗传信号和风险评分。",
    "The same heart diagrams connect phenotype definitions to risk comparisons. Four panels cover measurements, outcomes, genetic signals and risk scores."
  ],
  [
    "日常活动与久坐的联合暴露",
    "Joint exposure to everyday activity and sedentary behavior"
  ],
  [
    "上半用两组日常活动图标和天平解释为什么要联合看暴露。下半用对应位置的森林图回答不同暴露组合的风险。",
    "Icons and a balance illustrate the rationale for examining both exposures. Aligned forest plots below show risk for each combination."
  ],
  [
    "空气污染、心血管病和癌症的共同风险",
    "Shared risks between air pollution, cardiovascular disease and cancer"
  ],
  [
    "左栏用重叠关系画心血管病和癌症的共享风险，右栏从室内外暴露沿着人体图引向共同机制。",
    "Overlaps on the left identify shared risk factors. The right uses a human figure to connect indoor and outdoor exposures to common mechanisms."
  ],
  [
    "换用 PREVENT 后的风险分层变化",
    "Risk reclassification after switching to PREVENT"
  ],
  [
    "把旧模型和新模型的风险组画在两边，用流线标出人群往上或往下移动，再用旁注解释最重要的变化。",
    "Risk groups under the two models appear on opposite sides. Flows trace upward and downward movement, with annotations highlighting the largest changes."
  ],
  [
    "久坐行为与心肾代谢结局",
    "Sedentary behavior and cardiovascular, kidney and metabolic outcomes"
  ],
  [
    "先用两张色块图展示不同久坐时长与活动水平的组合，再用结局图展开对各类疾病的比较。",
    "Two color-coded charts show combinations of sedentary time and activity. Outcome plots then compare associations across diseases."
  ],
  [
    "同一个年龄效应的两种研究设计",
    "Two study designs for estimating age effects"
  ],
  [
    "上半用蓝、红两条路径对照横断面与个体内纵向变化，下半放三个小图说明出生队列、年龄非线性和选择性参与各会怎样改变估计。",
    "Blue and red paths compare cross-sectional and within-person longitudinal changes. Three panels show how birth cohort, nonlinear age patterns and selective participation affect the estimates."
  ],
  [
    "从诊断前病历轨迹识别神经退行性疾病亚型",
    "Identifying neurodegenerative subtypes from prediagnostic health records"
  ],
  [
    "最上方先画出诊断前时间窗，再把病历编码、模型分型和独立队列验证顺着图往下排。",
    "A prediagnosis window comes first, followed by record coding, model-based subtyping and validation in an independent cohort."
  ],
  [
    "老龄化、空气污染与归因死亡的增减路径",
    "Aging, air pollution and changes in attributable deaths"
  ],
  [
    "用箭头把人口年龄结构和背景死亡率的变化连到归因死亡，各情景从输入到结果始终使用同一套颜色。",
    "Arrows link shifts in population age structure and background mortality to attributable deaths. Each scenario keeps the same color from input to outcome."
  ],
  [
    "污染极端事件、暴露–反应与健康预警",
    "Extreme pollution, exposure–response and health alerts"
  ],
  [
    "中间用漏斗把多地证据接到暴露–反应曲线。右边单独画出方法可用于什么，把预警和负担估算分成两个画面。",
    "A funnel merges multisite evidence into an exposure–response curve. Separate panels on the right show applications to early warnings and burden estimation."
  ],
  [
    "用 ICU 实际数据做外部验证",
    "External validation using routine ICU data"
  ],
  [
    "左侧并排摆出试验和 ICU 数据来源，并列清楚入组与对照组。右侧按顺序画缺失处理、加权和结局分析。",
    "The left aligns trial and ICU sources, eligibility and comparators. The right follows missing data handling, weighting and outcome analysis."
  ],
  [
    "从计划到落地的分娩安全干预",
    "From planning to delivery of a childbirth safety intervention"
  ],
  [
    "上方串起清单设计、教练实施和预期作用，下方把多次到访画成一条时间线，让读者看见干预实际上怎样交付。",
    "The upper section links checklist design, coaching and intended effects. A timeline of visits below shows how the intervention is delivered."
  ],
  [
    "从可穿戴信号到居家检测",
    "From wearable signals to at-home testing"
  ],
  [
    "把参与者从佩戴设备、收到提示到查看结果的步骤画在左边，右边放真实应用界面，说明干预在参加者一侧长什么样。",
    "The left traces wearing the device, receiving a prompt and checking results. App screens on the right show what participants see."
  ],
  [
    "用《星月夜》表现复杂系统中的秩序",
    "The Starry Night as an image of order in complex systems"
  ],
  [
    "编辑借互相连成涡流的笔触，表达怎样从局部观测看见复杂系统的整体结构。封面选的是一个能承载主题的画面。",
    "The cover uses interconnected brushstrokes to represent how local observations reveal large-scale structure in complex systems."
  ],
  [
    "用古希腊陶杯表现突发公共卫生事件",
    "An ancient Greek cup and public health emergency response"
  ],
  [
    "把人物与怪兽的冲突集中在陶杯中央的圆形构图里，用一件古物对应当期对突发事件应对的讨论。",
    "A circular composition frames the conflict between a person and a monster. The cover uses the artifact to introduce the issue’s discussion of emergency response."
  ],
  [
    "痴呆风险因素的生命历程信息图",
    "Dementia risk factors across the life course"
  ],
  [
    "用早年、中年、晚年三段配色组织风险因素，最后汇到总体归因估计。",
    "Colors group early-, mid- and later-life factors and connect them to an overall population attributable estimate."
  ],
  [
    "久坐与未来心血管疾病",
    "Sedentary behavior and future cardiovascular disease"
  ],
  [
    "Central Illustration 把腕戴加速度计、人群和结局放在同一区域，给剂量–反应和时间替代结果各留出位置。",
    "The central illustration groups wrist accelerometry, the cohort and outcomes, with space for dose–response and time-substitution results."
  ],
  [
    "体力活动与心血管病患者死亡风险",
    "Physical activity and mortality among people with cardiovascular disease"
  ],
  [
    "把加速度计测量接到随访设计和不同死因的结果。",
    "Accelerometer measurements connect to follow-up and cause-specific mortality findings."
  ],
  [
    "STEP 4 随机试验的体重变化",
    "Weight change in the STEP 4 randomized trial"
  ],
  [
    "先交代问题和结论，下方三列给人群、干预和结果。组间差留出显眼位置。",
    "The research question and conclusion come first. Three columns show participants, intervention and results, with the between-group difference prominent."
  ],
  [
    "北京清洁空气行动与肺癌生存",
    "Beijing’s Clean Air Action and survival after lung cancer"
  ],
  [
    "三栏依次交代研究设计、关联结果和模型估计的收益。",
    "Three columns show the study design, associations and model-estimated benefits."
  ],
  [
    "临床试验设计与数据图样例",
    "Examples of trial design and data displays"
  ],
  [
    "在官方选集中比较试验设计图、森林图和多面板结果图的信息密度。",
    "The journal’s collection allows comparison of trial diagrams, forest plots and the density of multi-panel results."
  ],
  [
    "用树木年轮画生命历程",
    "Tree rings as a visual metaphor for the life course"
  ],
  [
    "把生命阶段变成年轮，用像钟表指针的裂缝表现生物年龄偏离。",
    "Life stages are represented by growth rings. A clock-hand-like crack makes biological age deviation visible."
  ],
  [
    "机器人眼中的生物年龄",
    "Biological age through the eyes of a robot"
  ],
  [
    "让机器人给人画肖像，把实际看到的人和模型描绘的生物年龄放进同一场景。",
    "A robot paints a portrait, bringing the observed person and the model’s representation of biological age into one scene."
  ],
  [
    "健康老龄化的社会决定因素",
    "Social determinants of healthy aging"
  ],
  [
    "把社会条件画成需要由人共同建设的雕像。",
    "A sculpture built by multiple people stands for the social conditions that support healthy aging."
  ],
  [
    "近百万全基因组序列里的个体遗传变异",
    "Individual genetic variation across nearly a million genomes"
  ],
  [
    "左侧以人体轮廓交代两个人群数据库和遗传祖源分组，右侧用收窄的梯形逐层呈现单人携带的变异，再以独立圆点标出少见的变异类型。",
    "A human silhouette introduces the two databases and ancestry groups. Narrowing bands then show variation per person, with separate circles for uncommon variant classes."
  ],
  [
    "南亚人群的脂蛋白(a)在两队列中如何比较",
    "Comparing lipoprotein(a) across two South Asian cohorts"
  ],
  [
    "上下两幅南亚地图用同一地理框架呈现 MASALA 与 UK Biobank，便于在两个数据来源间对照各地区人群的脂蛋白(a)水平。",
    "Two maps use the same geographic frame to compare lipoprotein(a) by region of ancestry in MASALA and UK Biobank."
  ],
  [
    "运动和膳食如何对应不同心肾代谢分期",
    "Physical activity and diet across cardiovascular–kidney–metabolic stages"
  ],
  [
    "顶部交代 UK Biobank、两类行为暴露和结局，中间用一条分期带连接下方的两组分析，方便沿同一分期读结果。",
    "The top summarizes UK Biobank, two behavioral exposures and outcomes. A shared stage band aligns the two analyses below."
  ],
  [
    "用组学连接心肾代谢综合征分期与癌症风险",
    "Linking cardiovascular–kidney–metabolic stages to cancer risk with omics"
  ],
  [
    "把心肾代谢分期排成阶梯，在两个人体插画之间按行摆放主要分析、蛋白组、代谢组和癌症结局。",
    "A staircase marks syndrome stages. Rows between two anatomical illustrations summarize the main analysis, proteomics, metabolomics and cancer outcomes."
  ],
  [
    "同一预防决策下的多个心血管风险时间窗",
    "Comparing cardiovascular risk horizons for prevention decisions"
  ],
  [
    "左栏交代研究设计，右栏用同色编码的趋势图和条形图，分别回答谁会接受治疗以及长期会获益多少。",
    "The left introduces the study design. Color-matched charts on the right show who would be treated and how much they might benefit over time."
  ],
  [
    "心血管疾病的共享与特异代谢图谱",
    "Shared and disease-specific metabolomic signatures of cardiovascular disease"
  ],
  [
    "三列把队列与数据整合、跨疾病代谢图谱和标志物发现排成连续流程，中间用同一视图呈现疾病间的相似性与差异。",
    "Three columns connect cohort data integration, a cross-disease metabolic atlas and biomarker discovery. The center compares shared and distinct signatures."
  ],
  [
    "把医患性别配对与基层慢病管理排成矩阵",
    "A matrix of physician–patient sex pairings in primary care"
  ],
  [
    "两套数据使用同样的医患图标和矩阵布局，三列依次对照患病、治疗与控制，箭头方向编码关联方向。",
    "Both datasets use the same icons and grid for prevalence, treatment and control. Arrows encode the direction of the association."
  ],
  [
    "钠摄入与心衰风险的暴露和结局图",
    "Sodium intake and heart failure risk"
  ],
  [
    "用地图交代队列来源，中间列用食物图标表示暴露，右侧把剂量–反应曲线和人群归因比例并列。",
    "A map introduces the cohort and food icons show the exposure. The right compares the dose–response curve with the population attributable fraction."
  ],
  [
    "疫情前后空气污染与急性心梗如何同图比较",
    "Comparing air pollution and acute myocardial infarction around the pandemic"
  ],
  [
    "左栏以图标和时间趋势交代污染暴露，右栏成对呈现两阶段的估计，用一致的污染物标签连接两边。",
    "Icons and timelines introduce exposure on the left. The right pairs estimates from the two periods using the same pollutant labels."
  ],
  [
    "跨国肝移植队列的地区差异",
    "Regional variation in a multinational liver transplantation cohort"
  ],
  [
    "地图、分布图和结局估计分栏排列，上方先说明多中心队列，下方用短句概括研究意义。",
    "Maps, distributions and outcome estimates occupy separate columns. Cohort details appear above and concise implications below."
  ],
  [
    "乌克兰连续危机下的孕产与围产结局",
    "Maternal and perinatal outcomes during successive crises in Ukraine"
  ],
  [
    "三组面板使用同一组年份，分别呈现分娩活动、产妇结局和围产结局，支持读者逐年对照。",
    "Three panels share the same years and show delivery activity, maternal outcomes and perinatal outcomes for year-by-year comparison."
  ],
  [
    "中英队列怎样对照家族史与不同年龄的心血管风险",
    "Comparing family history and cardiovascular risk by age in Chinese and UK cohorts"
  ],
  [
    "在共同研究框架下，将年龄趋势曲线与效应量放在两栏，以一致的布局对照中国和英国队列。",
    "A shared design aligns age trends and effect estimates and uses the same layout for the Chinese and UK cohorts."
  ],
  [
    "从抗阻训练到老年肌肉代谢组",
    "From resistance training to the muscle metabolome in older adults"
  ],
  [
    "三个横向框依次表示训练、样本与质谱、主要结果，末栏用并排数据图回扣前面的测量。",
    "Three frames follow training, sampling and mass spectrometry, then the findings. Side-by-side plots connect the results back to the measurements."
  ]
]);
  for (const [source, translation] of cardTranslations) exact.set(source,translation);
  const newCardTranslations = [
  [
    "免疫检查点治疗后的心脏多模态随访",
    "Multimodal cardiac follow-up after immune checkpoint therapy"
  ],
  [
    "纵向主线分开基线、治疗和随访；横向分支放入检查项目和心脏影像，结局另列。",
    "A vertical timeline separates baseline, treatment and follow-up. Horizontal branches add assessments and imaging, with outcomes listed separately."
  ],
  [
    "把 AI 临床工作流的实施和成本放在一张图里",
    "Visualizing clinical workflow implementation and costs of AI"
  ],
  [
    "上半部并列人群、实施前后的流程和资源数据；中间成排的柱图使用同一顺序对齐两阶段的指标。",
    "The upper panels align the cohort, workflow changes and resource data. A row of bar charts uses the same order to compare measures before and after implementation."
  ],
  [
    "空间组学呈现肥胖相关的结直肠组织变化",
    "Spatial omics of obesity-related changes in colorectal tissue"
  ],
  [
    "顶部列出三类测量平台，下方用连续的组织剖面串起正常黏膜、过渡上皮和免疫环境重塑。",
    "The top lists measurement platforms. A sequence of tissue cross-sections below follows normal mucosa, transitional epithelium and remodeling of the immune environment."
  ],
  [
    "心肌影像风险分层的训练与验证",
    "Development and validation of cardiac imaging risk stratification"
  ],
  [
    "左侧从多中心样本分出开发集和验证集，中段用影像配对解释风险分层，右侧用相同的仪表图标表示不同风险。",
    "The multicenter sample splits into development and validation sets. Paired images explain classification, and matching gauges communicate levels of risk."
  ],
  [
    "自我对照病例系列里如何比较入组条件",
    "Comparing eligibility in a self-controlled case series"
  ],
  [
    "三栏分别给出研究人群、同一人内的时间比较和入组条件对结果解释的影响。",
    "Three columns show the population, within-person time comparison and how eligibility criteria affect interpretation."
  ],
  [
    "中国人群嗜酸性粒细胞的分布与分层",
    "Eosinophil count distributions and subgroups in the Chinese population"
  ],
  [
    "把样本、总体分布、分层曲线以及相关因素分别放入四个对齐的面板。",
    "Four aligned panels present the sample, overall distribution, subgroup curves and correlates."
  ],
  [
    "从关节衰老到关节健康寿命",
    "From joint aging to joint healthspan"
  ],
  [
    "四个窄框从关节生物学过渡到表型评估、分型照护和共同目标，保持同一列宽和阅读顺序。",
    "Four columns lead from joint biology through phenotype assessment and tailored care to a shared goal."
  ],
  [
    "在普通人群参照下比较老年心衰的生存",
    "Comparing heart failure survival against a matched population reference"
  ],
  [
    "上下两层重用年龄组配色。先比较绝对生存，再与年龄和性别匹配的普通人群参照比较。",
    "The same age-group colors connect absolute survival at the top with comparisons against an age- and sex-matched population reference below."
  ],
  [
    "由妊娠结局连到远期心血管风险",
    "Connecting pregnancy outcomes to later cardiovascular risk"
  ],
  [
    "两个生命阶段的人体轮廓夹住中间的风险连接，每侧以成列图标组织对应因素。",
    "Silhouettes at two life stages frame the risk pathway. Matching columns of icons organize the factors at each stage."
  ],
  [
    "把延迟干预和长期随访画成两条线",
    "Parallel timelines for delayed intervention and long-term follow-up"
  ],
  [
    "在平行时间线上标注干预与交叉的时点，右侧小图沿对应随访顺序展示结果。",
    "Parallel timelines mark intervention and crossover. Small charts to the right follow the same sequence of visits."
  ],
  [
    "抗血小板策略的历史时间带",
    "A timeline of antiplatelet strategies"
  ],
  [
    "平行箭头带分别追踪几类策略的演变，箭头分支和末端节点保留策略的延续与变化。",
    "Parallel arrow bands trace how strategies evolved. Branches and endpoints distinguish continuity from change."
  ],
  [
    "老年冠心病人群的多胺、体能与代谢测量",
    "Polyamines, fitness and metabolic measures in older adults with coronary disease"
  ],
  [
    "同一张图中把摄入、循环浓度和体能端点分区排列，散点图沿用各端点的图标提示。",
    "The panels distinguish intake, circulating concentrations and fitness endpoints. The corresponding icons guide readers through the scatterplots."
  ],
  [
    "从病历文本到可比较的心血管风险分数",
    "From health record text to comparable cardiovascular risk scores"
  ],
  [
    "上方分开方法与模型设计，下方按相同分组并列方案及性能，不让模型细节遮住读者关心的对照。",
    "The upper panels separate inputs from model design. Outcome charts below compare approaches in a consistent order."
  ],
  [
    "用反事实场景表达早孕心血管健康",
    "Visualizing counterfactual scenarios for early pregnancy cardiovascular health"
  ],
  [
    "左侧环形图组织早孕可变指标，通过一条箭头连到右侧的情景估计和妊娠结局。",
    "A ring organizes potentially modifiable factors. A single arrow leads to scenario estimates and pregnancy outcomes."
  ],
  [
    "童年不良经历与成年心血管健康",
    "Childhood adversity and adult cardiovascular health"
  ],
  [
    "把童年经历、生活方式指标与成年结局放在一条图解路径上，旁边按相同分层呈现风险估计。",
    "The left links childhood experiences, lifestyle measures and adult outcomes. The adjacent estimates use the same subgroup structure."
  ],
  [
    "心肾代谢分期与预期寿命",
    "Cardiovascular–kidney–metabolic stages and life expectancy"
  ],
  [
    "同一组颜色贯穿分期图标、人数和生存曲线，便于把某一分期一路追到寿命估计。",
    "The same colors connect stage icons, sample counts and survival curves, letting readers trace a stage through to life expectancy."
  ],
  [
    "冠心病人群周边绿地与随访死亡",
    "Neighborhood greenness and mortality in coronary heart disease"
  ],
  [
    "图中先用居住环境和绿化指标定位暴露，下面按一致的分层组织几组曲线和效应量。",
    "The upper section uses residential context and greenness measures to define exposure. The lower section aligns curves and estimates by subgroup."
  ],
  [
    "儿童机会指数如何连接到肺高压结局",
    "Linking the Child Opportunity Index to pulmonary hypertension outcomes"
  ],
  [
    "三个平行区块展示社会机会、人口特征与就医条件，自上而下汇到同一个临床结局。",
    "Parallel blocks show opportunity, population characteristics and access to care before converging on a shared outcome."
  ],
  [
    "把物质使用、心理状况和妊娠结局放在一张图里",
    "Substance use, psychological conditions and pregnancy outcomes in one figure"
  ],
  [
    "连续的插画和路径连接暴露、分组和妊娠结局，关键估计留在路径附近，便于对照。",
    "Illustrations and flows connect exposures, groups and pregnancy outcomes. Key estimates sit beside the relevant parts of the path."
  ],
  [
    "从住址空气污染连接到两次心脏影像",
    "Connecting residential air pollution to repeated cardiac imaging"
  ],
  [
    "把长时段暴露、反复影像测量与心脏结构变化放在左右相邻的区域，时间信息跟随对应数据。",
    "The graphic aligns long-term exposure, repeated imaging and changes in cardiac structure, with timing beside the corresponding data."
  ],
  [
    "中年体能、冠脉钙化与晚年痴呆",
    "Midlife fitness, coronary calcium and dementia in later life"
  ],
  [
    "用三个并列区块区分样本、两种中年测量和晚年结局，再把联合比较靠近测量区域。",
    "Three blocks separate the cohort, two midlife measures and later outcomes. Joint comparisons remain close to the measurements they use."
  ],
  [
    "多祖源人群的心衰遗传变异图谱",
    "Genetic variation in heart failure across ancestries"
  ],
  [
    "分区介绍样本与病因、祖源及变异结果，人数构成和几个结果面板统一编码。",
    "Separate sections introduce the cohort, etiologies, ancestry and findings. The displays use consistent visual codes for key groups."
  ],
  [
    "用瀑布图比较心血管风险管理情景",
    "A waterfall chart for cardiovascular risk management scenarios"
  ],
  [
    "把风险因子控制情景排在同一参照下，以逐步变化的柱形表达各情景的预计贡献。",
    "Scenarios share a reference. Successive steps show the projected contribution of each change in risk factor control."
  ],
  [
    "全国登记队列中的房颤表型图谱",
    "A nationwide phenome-wide map of atrial fibrillation"
  ],
  [
    "一侧用地图和人群图标说明数据覆盖与分析，另一侧按心血管结局和分层总结发现。",
    "A map and participant icons establish coverage and methods. The other side organizes findings by cardiovascular outcome and subgroup."
  ],
  [
    "MOSAAIC 多族裔人群研究的队列设计",
    "Design of the MOSAAIC multiethnic cohort"
  ],
  [
    "地图展示参与地区，图标与时间条分别描述样本框架和招募安排，左侧留出研究身份和社区目标。",
    "A map shows participating regions. Icons and a timeline explain sampling and recruitment, while the left introduces the study and community goals."
  ],
  [
    "房颤患者的心肾代谢表型与多系统结局",
    "Cardiovascular–kidney–metabolic phenotypes and multisystem outcomes in atrial fibrillation"
  ],
  [
    "用固定分群颜色连接左侧患者特征、右上多系统风险矩阵和右下随访曲线。",
    "Consistent cluster colors link participant features on the left to the risk matrix and follow-up curves on the right."
  ],
  [
    "如何呈现超声视频与文本模型的比较",
    "Comparing vision–language models for echocardiography"
  ],
  [
    "三列分别交代视频和报告、图文模型结构以及性能比较，底部图标单列表达潜在使用场景。",
    "Three columns cover videos and reports, model design and performance. A separate lower row presents intended uses."
  ],
  [
    "东南亚的主要死亡风险如何随年龄变化",
    "Age patterns in leading mortality risk factors across Southeast Asia"
  ],
  [
    "两侧热图使用同样的年龄顺序和风险颜色，按性别对照各年龄组最重要的死亡风险。图 3。",
    "Paired heatmaps share age order and risk colors to compare leading mortality risks by age and sex. Figure 3."
  ],
  [
    "用同一套地图比较二手烟暴露",
    "Mapping second-hand smoke exposure with a shared scale"
  ],
  [
    "上下两组图沿用同一色阶和地区放大框，让读者在总体分布和拥挤地区之间切换。图 1。",
    "Both map sets use the same color scale and regional insets, making global patterns and crowded regions comparable. Figure 1."
  ],
  [
    "两个人群队列中的眼底影像与房颤",
    "Retinal imaging and atrial fibrillation in two population cohorts"
  ],
  [
    "同一张图并列队列来源、眼底影像与视网膜指标，再分开显示已有房颤和新发房颤的结果。图 1。",
    "One schematic aligns the cohorts, retinal images and derived measures before separating prevalent and incident atrial fibrillation. Figure 1."
  ],
  [
    "荷兰高温和寒冷相关超额死亡的空间分布",
    "Mapping excess mortality associated with heat and cold in the Netherlands"
  ],
  [
    "热与冷分别采用暖色和冷色，两行用相同地理轮廓对照行政区与市镇尺度。图 3。",
    "Warm and cool palettes distinguish heat and cold. Two rows compare districts and municipalities using the same geographic outline. Figure 3."
  ],
  [
    "在队列时间轴上标出索引日和观察窗",
    "Showing the index date and observation windows on a cohort timeline"
  ],
  [
    "用一条日历时间轴放在索引日前后的共同位置，分色注明回溯窗、随访窗和各自读取的数据。图 1。",
    "A calendar axis anchors the index date. Separate colors show the look-back and follow-up windows and which data come from each. Figure 1."
  ],
  [
    "极端高温下老年人的适应能力",
    "Adaptive capacity and extreme heat in older people"
  ],
  [
    "把个人储备与环境资源放在上方并列，中间汇到适应能力，下方分开呈现可能的健康转归。图 1。",
    "Individual reserves and contextual resources form parallel inputs. They converge on adaptive capacity, which connects to different health trajectories. Figure 1."
  ],
  [
    "从排放物和生命周期追踪塑料的健康负担",
    "Tracing the health burden of plastics through emissions and life-cycle stages"
  ],
  [
    "上部分用桑基图连起地理分组、生命周期、排放物和健康负担，下部用一组面板展开各类贡献。图 5。",
    "The Sankey diagram connects regions, life-cycle stages, emissions and health burden. Panels below show contributors for each impact category. Figure 5."
  ],
  [
    "四种复合暴露指标如何改变同一张地图",
    "How four composite exposure methods change the same map"
  ],
  [
    "上排用法国同一组市镇比较四种方法的空间结果，下排对齐各指标的总体分布。图 1。",
    "The top compares four methods across the same French municipalities. The bottom aligns the distribution from each method. Figure 1."
  ],
  [
    "把暴露之间的相关性画成圆形网络",
    "Visualizing exposure correlations as circular networks"
  ],
  [
    "两个圆形网络用节点颜色区分暴露类别，右侧累积分布补上不能从连线密度直接读出的相关性强弱。图 5。",
    "Two circular networks use color to distinguish exposure categories. A cumulative distribution complements network density with correlation magnitudes. Figure 5."
  ],
  [
    "医学影像",
    "Medical imaging"
  ],
  [
    "空间组学",
    "Spatial omics"
  ],
  [
    "表型组",
    "Phenome"
  ],
  [
    "瀑布图",
    "Waterfall chart"
  ],
  [
    "童年",
    "Childhood"
  ],
  [
    "自我对照病例系列",
    "Self-controlled case series"
  ]
];
  for (const [source, translation] of newCardTranslations) exact.set(source, translation);

  const reviewed2026Translations = [
  [
    "数字病房与常规房颤照护怎么对照",
    "Comparing a digital ward with usual atrial fibrillation care"
  ],
  [
    "左栏对齐两种照护路径和匹配队列，右栏按临床结局、再次就诊与成本分层。",
    "The left column aligns care pathways and matched cohorts. The right column separates clinical outcomes, repeat visits and costs."
  ],
  [
    "用窦性心律超声图像识别房颤",
    "Identifying atrial fibrillation from sinus-rhythm echocardiograms"
  ],
  [
    "三条横向流程分别交代模型开发、独立检验与后续随访。",
    "Three horizontal tracks separate model development, independent testing and subsequent follow-up."
  ],
  [
    "Tromsø 队列中糖尿病与心梗风险的性别差异",
    "Sex differences in myocardial infarction risk in the Tromsø Study"
  ],
  [
    "先用地图交代队列，再把男女发病曲线、调整后风险和各因素的贡献并排。",
    "A map locates the cohort. Adjacent panels align incidence curves, adjusted risks and individual risk-factor contributions by sex."
  ],
  [
    "把心电向量放回心脏成像空间",
    "Placing electrocardiographic vectors in cardiac imaging space"
  ],
  [
    "左侧按时间交代心电测量，右侧用心脏影像和两根向量解释测量指标。",
    "Serial ECG measurements sit on the left. Cardiac imaging on the right anchors the two vectors used in the analysis."
  ],
  [
    "按射血分数比较急性冠脉综合征后的用药",
    "Comparing treatment after acute coronary syndrome across ejection fractions"
  ],
  [
    "上方交代加权队列，下方用相邻图表对照不同射血分数下的生存结果。",
    "The weighted cohort sits above paired displays of survival across ejection fractions."
  ],
  [
    "在一张图里区分抗血小板方案的直接和间接比较",
    "Direct and indirect comparisons of antiplatelet strategies"
  ],
  [
    "上半部画出三条给药路径，下半部按临床结局对齐直接和间接证据。",
    "Treatment pathways appear above outcome rows that align the direct and indirect comparisons."
  ],
  [
    "用同一组颜色连接休克表型与三日转归",
    "Tracking cardiogenic shock phenotypes over three days"
  ],
  [
    "左栏定义三种表型，右栏用风险矩阵和三日流向图保留同一表型颜色。",
    "The left column defines three phenotypes. A risk matrix and a three-day flow diagram reuse the same colors."
  ],
  [
    "用共享对照连接两项药物试验",
    "Connecting two drug trials through a shared comparator"
  ],
  [
    "左栏用共享对照解释跨试验比较，中栏把随访曲线和效应估计放在一起。",
    "The shared comparator explains the cross-trial design on the left. The middle pairs follow-up curves with effect estimates."
  ],
  [
    "从细胞外囊泡提取到心脏淀粉样变蛋白组",
    "From extracellular vesicles to proteomic patterns in cardiac amyloidosis"
  ],
  [
    "上半部把样本与囊泡分离接到蛋白热图，下半部列出两类差异信号。",
    "Sample collection and vesicle isolation lead to a protein heatmap, with two sets of distinguishing signals below."
  ],
  [
    "社区心肾代谢照护试验的图文摘要",
    "A community trial of integrated cardiometabolic care"
  ],
  [
    "上下分区把招募、干预对照和主要结局接起来，干预组颜色从分组沿用至结果。",
    "Stacked panels connect recruitment, randomized groups and the primary outcome. Group colors carry through to the results."
  ],
  [
    "顺序到达的心电和胸片怎样进入同一个模型",
    "Combining sequential ECGs and chest radiographs in one model"
  ],
  [
    "用四格对照临床工作流、模型模块、数据来源与外部验证。",
    "Four panels align the clinical workflow, model architecture, data sources and external validation."
  ],
  [
    "用放射状图组织克隆性造血和心血管风险",
    "A radial map of clonal hematopoiesis and cardiovascular risk"
  ],
  [
    "中心用环状图组织克隆组分，左右两翼分别交代移植前风险和心血管影响。",
    "A central ring organizes clonal components, flanked by pre-transplant risks and cardiovascular outcomes."
  ],
  [
    "两种心肌标志物怎样组合做术后风险分层",
    "Combining cardiac biomarkers for postoperative risk stratification"
  ],
  [
    "上方地图定位多中心队列，下方并排放判别曲线、标志物重叠与组合风险。",
    "A map locates the multicenter cohort above aligned discrimination curves, biomarker overlap and joint risk groups."
  ],
  [
    "把年轻人死因趋势和人群差异放在同一张摘要图",
    "Showing mortality trends and population differences in one abstract"
  ],
  [
    "上方用图标串联人群、死因和统计结果，下方并排展示时间趋势和地理差异。",
    "A row of icons connects population, cause of death and analysis. Lower panels place temporal and geographic comparisons side by side."
  ],
  [
    "把证据网络和治疗效应逐行对照",
    "Aligning evidence networks and treatment effects by outcome"
  ],
  [
    "相同方案图标贯穿左列的治疗清单，中右列按结局对齐证据网络与森林图。",
    "Treatment icons define the options on the left. Evidence networks and forest plots align in outcome rows on the right."
  ],
  [
    "移植后高血压研究的时间轴与结局分支",
    "A timeline with three outcome branches after stem-cell transplantation"
  ],
  [
    "先用时间轴定位移植和检查窗口，再向下分三条路线展示随访结局。",
    "The timeline anchors transplantation and assessment windows, followed by three parallel outcome branches."
  ],
  [
    "自主神经指标与癌症死亡风险的对照矩阵",
    "A comparison matrix for autonomic markers and cancer mortality"
  ],
  [
    "把不同指标放在列、癌种放在行，以一致颜色表示风险升降和未观察到关联。",
    "Markers form columns and cancer sites form rows. Shared colors distinguish higher, lower and null associations."
  ],
  [
    "把病历文字转成结构化心肌炎证据",
    "Turning clinical notes into structured myocarditis evidence"
  ],
  [
    "三层依次呈现研究目标、分层信息提取及对照评估，顶部图标与方法分支呼应。",
    "Three tiers show the objective, hierarchical extraction and comparative evaluation. Icons connect the inputs to their method branches."
  ],
  [
    "心电模型、超声表型与外部队列的对照",
    "Aligning ECG predictions, ultrasound phenotypes and external replication"
  ],
  [
    "左至右呈现心电推断、匹配的超声数据和相关性，底部单列外部复现。",
    "Left-to-right panels connect ECG inference, matched echocardiography and correlations. External replication appears below."
  ],
  [
    "用同一颜色系统跟踪主动脉狭窄分期",
    "Reusing stage colors across aortic stenosis panels"
  ],
  [
    "心脏损害分级、瓣膜图标和结局曲线使用相同的层级顺序与颜色。",
    "Cardiac damage stages, valve illustrations and outcome curves follow the same category order and color scheme."
  ],
  [
    "从首个警示信号到确诊和随访",
    "From early warning signs to diagnosis and follow-up"
  ],
  [
    "围绕诊断时点分段，用上下对齐的文字和图标标出警示、转诊与远期结局。",
    "An aligned timeline marks warning signs, referral and long-term outcomes around the diagnosis date."
  ],
  [
    "房颤分型的开发、外部验证与策略比较",
    "Developing, validating and applying atrial fibrillation phenotypes"
  ],
  [
    "训练和外部应用置于左侧，右侧按相同分型颜色对照预后与消融策略。",
    "Training and external application sit on the left. Matching phenotype colors connect prognosis and ablation comparisons on the right."
  ],
  [
    "把多维衰弱的测量和结局压缩到三栏",
    "A three-column design for multidimensional frailty"
  ],
  [
    "中间用四个图标解释衰弱评分，两边分别放队列和一年结局。",
    "Four icons explain the frailty score between the cohort overview and one-year outcomes."
  ],
  [
    "孕期和产后心血管筛查的双路径图",
    "Two pathways for cardiovascular screening in pregnancy and postpartum"
  ],
  [
    "以颜色区分孕期与产后筛查，再把两条路径接到确诊和阳性预测值。",
    "Color distinguishes screening in pregnancy and postpartum. Both pathways lead to confirmation and positive predictive values."
  ],
  [
    "从多普勒频谱到每次检查的自动输出",
    "From Doppler spectra to examination-level output"
  ],
  [
    "三栏按输入、自动分析和检查层面输出排列，保留原始多普勒信号的局部示例。",
    "Three columns show the input, automated analysis and examination-level output, with a sample Doppler trace in context."
  ],
  [
    "地图、病例与社会因素如何组成先心病研究摘要",
    "Mapping sites, patients and social factors in congenital heart disease"
  ],
  [
    "地图定位参与中心，第二层交代治疗路径，底层把社会因素与临床决策并排。",
    "A map locates participating centers. Treatment paths lead to a comparison of social factors and clinical decisions."
  ],
  [
    "图解心电人工智能的诊断证据汇总",
    "A visual synthesis of diagnostic evidence for AI-enabled ECGs"
  ],
  [
    "第一层解释心电输入、模型和参考检查，第二层独立汇总诊断指标与统计图。",
    "The top tier introduces inputs, models and the reference test. A separate tier summarizes diagnostic metrics and plots."
  ],
  [
    "用同一时间轴连接用药、血红蛋白与癌症检出",
    "An aligned timeline for anticoagulation, hemoglobin and cancer detection"
  ],
  [
    "上方按时间顺序放两次测量和癌症观察窗，下方用对应的小图展示风险比较。",
    "The timeline identifies two measurements and the cancer observation window above the corresponding risk comparisons."
  ],
  [
    "把多模态模型、风险判别与影像解释同图排列",
    "Aligning a multimodal model with risk and imaging explanations"
  ],
  [
    "上半部对照影像与结构化数据的融合，下半部并列判别表现、变量重要性和影像解释。",
    "The upper pipeline combines images and structured data. Lower panels align discrimination, variable importance and image explanations."
  ],
  [
    "用眼底照片筛查亚临床动脉粥样硬化",
    "Screening for subclinical atherosclerosis with retinal images"
  ],
  [
    "用四个对应模块交代临床问题、数据、模型与输出，底部列出可能的使用场景。",
    "Four aligned modules show the clinical problem, data, model and output, with potential uses summarized below."
  ],
  [
    "用颜色贯穿移植物示意与试验证据",
    "Carrying graft colors from surgical diagrams to trial evidence"
  ],
  [
    "上方用颜色和图形区分搭桥策略，下方在森林图与试验网络复用这些颜色。",
    "Color and shape distinguish bypass strategies above and reappear in the forest plot and evidence network below."
  ],
  [
    "镜像呈现人工和自动超声测量",
    "Mirroring manual and automated echocardiography measurements"
  ],
  [
    "左右两栏保留同一参考检查与测量项目，只改变人工和自动测量的比较对象。",
    "Both columns use the same reference examination and measurements. The comparison changes from human readers to AI."
  ],
  [
    "把四个队列、糖尿病风险刻度和长期曲线对齐",
    "Aligning cohorts, diabetes risk bands and long-term outcomes"
  ],
  [
    "左上列出开发和验证数据，右侧沿同一颜色阶梯对照不同风险组的长期结局。",
    "Development and validation data appear on the left. Color-ordered risk bands correspond to long-term curves on the right."
  ],
  [
    "用分支队列解释遗传变异与妊娠相关心肌病",
    "A branching cohort graphic for genetic variants and pregnancy-associated cardiomyopathy"
  ],
  [
    "从携带同一类变异的人群出发，先按妊娠经历分支，再交代心肌病和随访比较。",
    "The diagram starts with variant carriers, branches by pregnancy history and then shows cardiomyopathy and follow-up comparisons."
  ],
  [
    "儿童家族性高胆固醇血症的两步筛查",
    "Two-step screening for familial hypercholesterolemia in children"
  ],
  [
    "左栏说明入组和筛查流程，右栏用分布和阳性检出图联系阈值与结果。",
    "Enrollment and screening steps sit on the left. Distribution and detection plots on the right connect thresholds with findings."
  ],
  [
    "从儿童期开始降脂治疗的远期比较",
    "Long-term comparisons of lipid lowering from childhood"
  ],
  [
    "三组定义置顶，以下用同一尺度比较效应区间，并并列展示临床结局构成。",
    "The three group definitions sit above estimates aligned to a common scale and side-by-side clinical outcome distributions."
  ],
  [
    "把临床队列、UK Biobank 与机制证据拼在一张图里",
    "Combining clinical, biobank and mechanistic evidence in one graphic"
  ],
  [
    "左侧按三类证据分区，右侧将基因和代谢通路接到组织表型。",
    "Three tiers on the left establish the evidence sources. The right connects genetic and metabolic pathways to tissue phenotypes."
  ],
  [
    "血脂异常怎样连到肿瘤和心血管疾病",
    "Linking dyslipidemia, cancer and cardiovascular disease"
  ],
  [
    "用环形布局展示肿瘤、心血管病与脂质治疗的相互影响，沿环排列路径图标。",
    "A circular layout connects cancer, cardiovascular disease and lipid management, with icons positioned along the pathways."
  ],
  [
    "把试验代表性和性别分层结果放在一张图里",
    "Showing trial representation alongside sex-stratified results"
  ],
  [
    "把女性入组比例和效应差异独立分区，用相同的图形符号把代表性接到证据缺口。",
    "Separate panels display representation and treatment effects. Consistent symbols connect recruitment to evidence gaps."
  ],
  [
    "用一张图解释 PCSK9 观察性比较的设计",
    "A one-figure summary of an observational PCSK9 comparison"
  ],
  [
    "先交代设计和人群，再按治疗比较与敏感性分析对齐随访曲线。",
    "Study design and population come first, followed by aligned follow-up curves for treatment comparisons and sensitivity analyses."
  ],
  [
    "随机分配、随访与结局的分层排版",
    "Layering randomization, follow-up and outcomes"
  ],
  [
    "主线沿随机分配走向随访，下方按主次要结局逐行比较两组。",
    "The top tracks randomization into follow-up. Lower rows compare the groups by primary and secondary outcomes."
  ],
  [
    "四个面板对照心肾代谢综合征的性别差异",
    "Four panels for sex differences in cardiovascular–kidney–metabolic syndrome"
  ],
  [
    "四个区域依次放分期定义、性别构成、临床风险与干预比较。",
    "Four areas present stage definitions, sex distribution, clinical risk and intervention comparisons."
  ],
  [
    "SCORE2-HF 怎样把地区差异放进风险表达",
    "How SCORE2-HF shows regional differences in risk"
  ],
  [
    "各地区的风险色贯穿校准地图与病例比较，下方示例展示同一个人群画像的绝对风险差异。",
    "Consistent regional colors link the calibration map to example profiles that illustrate differences in absolute risk."
  ],
  [
    "把心衰模型放进两个临床病例对照",
    "Comparing two clinical cases with the LIFE-Preserved model"
  ],
  [
    "左侧说明 LIFE-Preserved 的模型要素，右侧用镜像病例同尺度比较不同时间窗的风险。",
    "Model components sit on the left. Mirrored cases on the right compare risks at matched time horizons."
  ]
];
  for (const [source, translation] of reviewed2026Translations) exact.set(source, translation);

  globalThis.GalleryLanguage = {
    searchText(item) {
      return [exact.get(item[3]), exact.get(item[5])].filter(Boolean).join(' ');
    },
  };

  const storedText = new WeakMap();
  const storedAttributes = new WeakMap();
  const date = new Intl.DateTimeFormat('en', {month:'short', year:'numeric', timeZone:'UTC'});
  const english = new URL(location.href).searchParams.get('lang') === 'en';
  let useEnglish = english;

  function translate(text) {
    if (exact.has(text)) return exact.get(text);
    if (text.includes(' · ')) return text.split(' · ').map(translate).join(' · ');
    const count = text.match(/^(全部|期刊封面|图文摘要|正文组图) (\d+)$/);
    if (count) return exact.get(count[1]) + ' ' + count[2];
    const month = text.match(/^(\d{4})年(\d{1,2})月$/);
    if (month) return date.format(new Date(Date.UTC(Number(month[1]), Number(month[2]) - 1)));
    if (text.startsWith('放大查看：')) return 'Enlarge: ' + translate(text.slice(5));
    return text
      .replace(/^显示 (\d+) \/ (\d+) (张图片|条记录)$/, (_,a,b,kind) => 'Showing ' + a + ' of ' + b + (kind === '张图片' ? ' figures' : ' records'))
      .replace(/([\d,]+) 刊目录/g, '$1 journals')
      .replace(/([\d,]+) 刊可预览/g, '$1 journals with previews')
      .replace(/([\d,]+) 张图$/g, '$1 figures')
      .replace(/计划盘点 ([\d-]+) 至 ([\d-]+) 首次线上发表的文章。/g, 'Online publication dates: $1 to $2.')
      .replace(/历史目录已扫描 (\d+)\/(\d+) 刊，共读取 ([\d,]+) 条记录。/g, 'Indexed $1 of $2 journals and $3 records.')
      .replace(/最近发布 ([\d-]+ [\d:]+)（北京时间）。/g, 'Last published $1 (China Standard Time).')
      .replace(/本次扫描 ([\d-]+) 至 ([\d-]+)，新增 (\d+) 张图文摘要。/g, 'Scan: $1 to $2. Added $3 graphical abstracts.')
      .replace(/另有 (\d+) 刊待完成历史目录盘点。/g, '$1 journals are pending archive review.')
      .replace(/图片加载失败。/g, 'The image could not load.')
      .replace(/出版社原图/g, 'Publisher image')
      .replace(/PubMed Central 收录版/g, 'PubMed Central version')
      .replace(/ 等(?=\s|·|，|$)/g, ' et al.')
      .replace(/图\s*(\d+)/g, 'Figure $1');
  }

  function translateNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      if (!storedText.has(node)) storedText.set(node,node.data);
      const input = storedText.get(node);
      const trimmed = input.trim();
      const output = useEnglish && trimmed ? input.replace(trimmed,translate(trimmed)) : input;
      if (node.data !== output) node.data = output;
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE || node.matches('script, style, #gallery-language')) return;
    const supported = ['alt','aria-label','placeholder'];
    let values = storedAttributes.get(node);
    for (const key of supported) {
      if (!node.hasAttribute(key)) continue;
      if (!values) {
        values = new Map();
        storedAttributes.set(node,values);
      }
      const current = node.getAttribute(key);
      let record = values.get(key);
      if (!record || record.rendered !== current) record = {original:current, rendered:current};
      const output = useEnglish ? translate(record.original) : record.original;
      values.set(key,{original:record.original, rendered:output});
      if (current !== output) node.setAttribute(key,output);
    }
    for (const child of node.childNodes) translateNode(child);
  }

  const toggle = document.createElement('button');
  toggle.id = 'gallery-language';
  toggle.className = 'plain';
  toggle.type = 'button';
  toggle.style.flexShrink = '0';
  const heading = document.createElement('div');
  heading.style.cssText = 'display:flex;justify-content:space-between;align-items:flex-start;gap:12px';
  title.before(heading);
  heading.append(title,toggle);
  const footer = document.createElement('footer');
  footer.className = 'wrap';
  footer.style.cssText = 'padding:14px 0 24px;border-top:1px solid var(--edge);color:var(--muted);font-size:13px';
  footer.textContent = '技术支持 · OpenAI Codex';
  document.querySelector('main').after(footer);
  exact.set('技术支持 · OpenAI Codex', 'Technical support · OpenAI Codex');

  const roots = [document.querySelector('title'), document.querySelector('header'),
    document.querySelector('main'), footer, document.querySelector('#viewer')].filter(Boolean);

  function apply() {
    document.documentElement.lang = useEnglish ? 'en' : 'zh-CN';
    toggle.textContent = useEnglish ? '中文' : 'English';
    toggle.lang = useEnglish ? 'zh-CN' : 'en';
    toggle.setAttribute('aria-label',useEnglish ? '切换到中文' : 'Switch to English');
    for (const root of roots) translateNode(root);
  }

  toggle.addEventListener('click',() => {
    useEnglish = !useEnglish;
    const url = new URL(location.href);
    if (useEnglish) url.searchParams.set('lang','en');
    else url.searchParams.delete('lang');
    history.replaceState(history.state,'',url);
    apply();
  });
  apply();

  const observer = new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'attributes') translateNode(record.target);
      else for (const node of record.addedNodes) translateNode(node);
    }
  });
  for (const root of roots.slice(1)) {
    observer.observe(root,{subtree:true, childList:true, attributes:true,
      attributeFilter:['alt','aria-label','placeholder']});
  }
})();

/* Search and filters. */
(() => {
  'use strict';
  const articleDatasets = {
    "10.1016/j.jacasi.2026.07.034": ["GBD"],
    "10.1016/j.jacasi.2026.05.016": ["COOL-AF"],
    "10.1016/j.jacasi.2025.11.016": ["GPS-CAD"],
    "10.1016/j.jacasi.2025.10.022": ["HART"],
    "10.1038/s44360-026-00220-z": ["ERA5-Land","E-OBS","CMIP6","Eurostat","WorldPop"],
    "10.59717/j.xinn-med.2025.100164": ["MIMIC-IV"],
    "academic.oup.com/ehjdh/article/5/5/591/7730212": ["UK Biobank"],
    '10.1016/j.ebiom.2026.106542': ['Pros-RODAM'],
    '10.1007/s11357-025-02090-x': ['LLFS', 'ILO'],
    '10.1016/j.envint.2026.110581': ['BiSC'],
    '10.1016/j.envint.2026.110430': ['FinnTwin12'],
    '10.1016/j.lanwpc.2026.101983': ['HEPCARE'],
    '10.1136/bmjopen-2026-122608': ['HELIX','多国多队列'],
    '10.1093/ehjdh/ztag159': ['西班牙 MBDS'],
    '10.1038/s41514-026-00384-8': ['GTEx','eQTLGen','BrainMeta','INTERVAL','1000 Genomes'],
    '10.1038/s41467-023-40908-4': ['GBD','CMIP6'],
    '10.1016/j.jacadv.2026.102665': ['PROMISE','CATHGEN'],
    '10.1016/j.jacadv.2026.103071': ['SWAN'],
    '10.59717/j.xinn-med.2025.100175': ['UK Biobank'],
    '10.1093/eurheartj/ehag563': ['UK Biobank'],
    '10.1038/s43587-026-01232-w': ['UK Biobank'],
    '10.1038/s41746-025-01771-3': ['UK Biobank'],
    'www.metabolismjournal.com/article/s0026-0495%2825%2900337-3/fulltext': ['UK Biobank'],
    '10.1093/ehjdh/ztag147': ['MIMIC-IV'],
    '10.1002/alz.71821': ['CHARLS','HRS','ELSA','多国多队列'],
    '10.1186/s12940-026-01327-2': ['上海出生队列'],
    'academic.oup.com/eurheartj/article/47/15/1799/8377304': ['UK Biobank'],
    'academic.oup.com/eurheartj/article/47/15/1861/8379858': ['UK Biobank'],
  };
  const datasetAliases = [
    ['多国多队列','mc','multicohort','multi cohort','cross national','多国队列','跨国多队列','多队列'],
    ['charls','china health and retirement longitudinal study','中国健康与养老追踪调查'],
    ['hrs','health and retirement study','美国健康与退休研究','美国健康与退休调查'],
    ['elsa','english longitudinal study of ageing','英国老龄化纵向研究'],
    ['share','survey of health ageing and retirement in europe','欧洲健康老龄化与退休调查'],
    ['nhanes','national health and nutrition examination survey','美国国家健康与营养调查'],
    ['mimic iv','mimiciv','mimic 4','mimic','重症监护数据库','重症监护医学信息数据库'],
    ['gbd','global burden of disease','全球疾病负担'],
    ['gtex','genotype tissue expression','基因型组织表达'],
    ['helix','human early life exposome','人类早期生命暴露组'],
    ['bisc','barcelona life study cohort','巴塞罗那出生队列'],
    ['llfs','long life family study','长寿家系研究'],
    ['ilo','integrative longevity omics study','长寿整合组学研究'],
    ['swan','study of women s health across the nation','美国女性健康研究'],
    ['mesa','multi ethnic study of atherosclerosis','多族裔动脉粥样硬化研究'],
    ['上海出生队列','shanghai birth cohort'],
    ['finntwin12','finntwin 12','芬兰双生子'],
    ['mbds','西班牙住院出院数据库'],
  ];
  const reviewedDates = {
    "www.the-innovation.org/article/id/66355e8352bf657b0f62aa78": "2024-06-25",
    "10.59717/j.xinn-med.2025.100175": "2025-11-19",
    "10.59717/j.xinn-med.2025.100164": "2025-10-31",
    "10.59717/j.xinn-med.2026.100238": "2026-07-15",
    "academic.oup.com/ehjdh/article/5/5/591/7730212": "2024-08-09",
    "10.1038/s43587-026-01232-w": "2026-10-06",
    "wwwnc.cdc.gov/eid/article/31/13/ac-3113_article": "2025-05",
    "wwwnc.cdc.gov/eid/article/32/6/ac-3206_article": "2026-06",
    "wwwnc.cdc.gov/eid/article/28/9/ac-2809_article": "2022-09",
    "fliphtml5.com/cvlqh/bh-1-1-cover-to-cover/": "2026-05",
    'academic.oup.com/eurheartj/article/47/15/1799/8377304': '2025-12-11',
    'academic.oup.com/eurheartj/article/47/15/1861/8379858': '2025-12-15',
    'www.bmj.com/content/368/bmj.m160': '2020-02-18',
    'www.metabolismjournal.com/article/s0026-0495%2825%2900337-3/fulltext': '2025-12-08',
    '10.1038/s41746-025-01771-3': '2025-07-26',
    'pmc.ncbi.nlm.nih.gov/articles/pmc12804104/': '2025-12-31',
    'pmc.ncbi.nlm.nih.gov/articles/pmc12490207/': '2025-08-25',
    '10.1038/s41591-026-04614-0': '2026-10-12',
    'jamanetwork.com/journals/jamanetworkopen/fullarticle/2847871': '2026-04-17',
    'jamanetwork.com/journals/jamanetworkopen/fullarticle/2847804': '2026-04-16',
    'academic.oup.com/eurjpc/article/32/1/77/7777149': '2024-09-26',
    'pmc.ncbi.nlm.nih.gov/articles/pmc11229557/': '2024-06-18',
    'pmc.ncbi.nlm.nih.gov/articles/pmc11734013/': '2024-12-26',
    'pmc.ncbi.nlm.nih.gov/articles/pmc13091349/': '2026-04-09',
    '10.1038/s43587-026-01085-3': '2026-02-26',
    '10.1038/s41467-023-40908-4': '2023-08-26',
    'pmc.ncbi.nlm.nih.gov/articles/pmc5672590/': '2017-12-14',
  };
  function articlePath(url) {
    return String(url ?? '').toLowerCase().replace(/^https?:\/\//,'').split(/[?#]/)[0];
  }
  function lookup(mapping, url, extra) {
    const path = articlePath(url);
    const directDoi = path.match(/(?:^|\/)(10\.\d{4,9}\/[^/]+)/)?.[1];
    const natureId = path.match(/^(?:www\.)?nature\.com\/articles\/(s\d{5}-[^/]+)/)?.[1];
    const doi = extra?.doi?.toLowerCase() ?? directDoi ?? (natureId && '10.1038/' + natureId);
    return mapping[doi] ?? mapping[path];
  }
  function formatDate(item) {
    const [kind, , year, , , , url, , , , extra] = item;
    const reviewed = lookup(reviewedDates, url, extra);
    const published = kind === 'cover' ? extra?.issueDate || reviewed : extra?.published || reviewed;
    const match = /^(\d{4})-(0[1-9]|1[0-2])(?:-\d{2})?$/.exec(published ?? '');
    return match ? match[1] + '年' + Number(match[2]) + '月' : String(year ?? '');
  }
  const facets = [
    ['主题', '全部主题', [
      ['环境健康', /环境|空气污染|细颗粒物|暴露组|气候|野火|pollution|climate|exposom|pm25|pfas|wildfire/u],
      ['生命历程', /生命历程|童年|孕期|围产|子代|早期暴露|life course|early life|childhood|prenatal|pregnan|offspring/u],
      ['心血管', /心血管|冠脉|冠心病|心脏|房颤|心力衰竭|cardiovascular|coronary|heart failure|atrial fibrillation|myocardial/u],
      ['老龄化', /老龄化|衰老|老年|衰弱|长寿|aging|ageing|frailty|longevity/u],
      ['组学', /组学|代谢组|蛋白组|遗传组|基因组|甲基化|表观遗传|omics|metabolom|proteom|genom|transcriptom|epigenet/u],
      ['代谢健康', /代谢|糖尿病|肥胖|血糖|胰岛素|metabolic|diabetes|obesity|glucose|insulin/u],
      ['神经与认知', /脑健康|神经|认知|痴呆|抑郁|dementia|alzheimer|cogniti|neurolog|depressi/u],
      ['肿瘤', /肿瘤|癌症|乳腺癌|oncolog|cancer|carcinoma/u],
      ['数字健康', /数字健康|可穿戴|人工智能|机器学习|digital health|wearable|machine learning|artificial intelligence/u],
      ['公共卫生', /公共卫生|卫生政策|卫生服务|全球负担|public health|health policy|health service|global burden/u],
    ]],
    ['研究设计', '全部设计', [
      ['队列研究', /队列|前瞻性随访|\bcohort\b|prospective study/u],
      ['随机试验', /随机对照|随机.{0,8}试验|\brct\b|randomi[sz]ed.{0,48}trial/u],
      ['病例对照', /病例对照|case control/u],
      ['病例交叉', /病例交叉|case crossover/u],
      ['横断面', /横断面|cross sectional/u],
      ['系统综述与荟萃分析', /系统综述|荟萃分析|systematic review|meta analysis/u],
      ['预测与验证', /风险预测|预测模型|外部验证|risk prediction|prediction model|external validation/u],
      ['定性研究', /定性研究|定性访谈|qualitative/u],
    ]],
    ['数据来源', '全部数据来源', [
      ['UK Biobank', /\bukb\b|\buk\s*biobank\b|英国生物样本库|英国生物银行|英国生物库/u],
      ['NHANES', /\bnhanes\b|national health and nutrition examination survey|美国国家健康与营养调查/u],
      ['FinnTwin12', /finntwin\s*12|芬兰双生子/u],
      ['MESA', /\bmesa\b|multi ethnic study of atherosclerosis/u],
      ['ARIC', /\baric\b|atherosclerosis risk in communities/u],
      ['CPRD', /\bcprd\b|clinical practice research datalink/u],
      ['Framingham', /framingham|弗雷明汉/u],
      ['CHARLS', /\bcharls\b|中国健康与养老追踪调查/u],
      ['MIMIC-IV', /\bmimic\s*(?:iv|4)\b/u],
      ['HRS', /\bhealth and retirement study\b|美国健康与退休(?:研究|调查)/u],
      ['ELSA', /\belsa\b|english longitudinal study of ageing|英国老龄化纵向研究/u],
      ['SHARE', /survey of health ageing and retirement in europe|欧洲健康老龄化与退休调查/u],
      ['HELIX', /\bhelix\b|human early life exposome/u],
      ['GBD', /\bgbd\b|global burden of disease|全球疾病负担/u],
      ['GTEx', /\bgtex\b|genotype tissue expression/u],
      ['SWAN', /\bswan\b|study of women s health across the nation/u],
      ['上海出生队列', /上海出生队列|shanghai birth cohort/u],
      ['MASALA', /\bmasala\b|mediators of atherosclerosis in south asians living in america/u],
      ['SHFS', /\bshfs\b|strong heart family study/u],
      ['SCCS', /\bsccs\b|southern community cohort study/u],
      ['HCHS/SOL', /\bhchs\s+sol\b|hispanic community health study/u],
      ['ECHO', /\becho cohort\b|environmental influences on child health outcomes/u],
      ['AlzEye', /\balzeye\b/u],
      ['MOSAAIC', /\bmosaaic\b|multi ethnic observational study in american asian and pacific islander communities/u],
    ]],
    ['作图方式', '全部作图方式', [
      ['研究流程图', /流程图|工作流|入组流程|筛选流程|建模流程|study workflow|flowchart/u],
      ['时间轴', /时间轴|时间线|时间窗口|诊断前时间窗|timeline/u],
      ['森林图与点区间图', /森林图|点区间图|forest plot|dot and whisker/u],
      ['桑基图与状态转移', /桑基图|流线|状态转移|sankey|alluvial/u],
      ['地理地图', /地图|空间分布|气旋路径|geographic map|choropleth/u],
      ['分类树与网络图', /分类图|树形图|网络图|关系网络|嵌套矩形|network map|treemap/u],
      ['概念与方法示意图', /概念图|概念框架|示意图|概念模型|conceptual framework|schematic/u],
      ['多面板组图', /组图|画成四列|三层分别|上下两层|多面板|分面|multipanel|multi panel/u],
      ['热图', /热图|热力图|heatmap|heat map/u],
      ['图标与插画', /图标|插画|视觉隐喻|icon|illustration/u],
    ]],
  ];
  const aliases = [
    ['ukb', 'uk biobank', 'ukbiobank', '英国生物样本库', '英国生物银行', '英国生物库'],
    ['mc', '多国多队列', 'multi country cohort', 'multi country cohorts', 'multicohort'],
    ['pm25', '细颗粒物', 'fine particulate matter'],
    ['老龄化', '老年', '衰老', 'aging', 'ageing'],
    ['队列', '队列研究', 'cohort'],
    ['暴露组', 'exposome', 'exposomics'],
    ['组学', 'omics', 'multiomics', 'multi omics'],
    ['代谢组', 'metabolomics', 'metabolomic'],
    ['蛋白组', 'proteomics', 'proteomic'],
    ['肿瘤', '癌症', 'cancer', 'oncology'],
    ['心血管', 'cardiovascular', 'cvd'],
    ['生命历程', 'lifecourse', 'life course'],
    ['桑基图', 'sankey', 'alluvial'],
    ['流程图', 'flowchart', 'workflow'],
    ['随机试验', '随机对照试验', 'rct', 'randomized controlled trial', 'randomised controlled trial'],
    ['新英格兰医学杂志', 'new england journal of medicine', 'nejm'],
    ['欧洲心脏杂志', 'european heart journal', 'ehj'],
    ['柳叶刀', 'lancet'],
    ['图片摘要', '图文摘要', 'graphical abstract', 'visual abstract', 'central illustration'],
  ];
  const kinds = {abstract:'图文摘要', figures:'正文组图', cover:'期刊封面'};
  function clean(value) {
    return String(value ?? '').normalize('NFKD').toLowerCase().replace(/\p{M}/gu, '')
      .replace(/\bpm\s*2(?:[.\s]+)?5\b/gu, 'pm25').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  }
  function hasTerm(text, term) {
    return /^[a-z0-9 ]+$/.test(term) ? (' ' + text + ' ').includes(' ' + term + ' ') : text.includes(term);
  }
  function describe(item) {
    const [type, journal, , title, keywords, note, url, , , , extra] = item;
    const translated = globalThis.GalleryLanguage?.searchText(item);
    const facts = clean([title, keywords, note, extra?.description, translated].filter(Boolean).join(' '));
    const graphic = clean([note, keywords, type === 'figures' ? '组图' : ''].filter(Boolean).join(' '));
    const keys = ['topic', 'design', 'dataset', 'layout'];
    const features = facets.map(([, ,rules], i) => {
      const matched = rules.filter(([,rule]) => rule.test(i===3 ? graphic : facts)).map(([key]) => key);
      const explicit = extra?.features?.[keys[i]];
      const verified = i === 2 ? lookup(articleDatasets, url, extra) ?? [] : [];
      return [...new Set([...matched, ...verified, ...(Array.isArray(explicit) ? explicit : [])])];
    });
    const base = clean([kinds[type], journal, formatDate(item), facts, ...features.flat()].join(' '));
    const text = [base, ...[...aliases, ...datasetAliases].filter(group => group.some(term => hasTerm(base,term))).flat()].join(' ');
    return {features, text, words:[...new Set(text.match(/[a-z][a-z0-9]{4,}/g) ?? [])]};
  }
  function near(term, word) {
    if (Math.abs(term.length-word.length) > 1) return false;
    const a = term.length <= word.length ? term : word;
    const b = term.length <= word.length ? word : term;
    let first = 0;
    while (first < a.length && a[first] === b[first]) first++;
    if (a.length !== b.length) return a.slice(first) === b.slice(first+1);
    return a.slice(first+1) === b.slice(first+1) ||
      (a[first] === b[first+1] && a[first+1] === b[first] && a.slice(first+2) === b.slice(first+2));
  }
  function matches(record, query) {
    return clean(query).split(' ').filter(Boolean).every(term => {
      if (/^[a-z0-9]{1,3}$/.test(term) && !(term === 'uk' || term === 'us')) {
        return hasTerm(record.text,term) || term.length === 1 && record.text.includes(term);
      }
      return record.text.includes(term) || /^[a-z][a-z0-9]{4,}$/.test(term) &&
        record.words.some(word => near(term,word));
    });
  }
  function setup(items, before, redraw) {
    const index = new Map(items.map(item => [item,describe(item)]));
    const group = document.createElement('div');
    group.className = 'extra-filters';
    const selects = facets.map(([label,all],i) => {
      const select = document.createElement('select');
      select.setAttribute('aria-label', label);
      const available = [...new Set([...index.values()].flatMap(item => item.features[i]))];
      available.sort((a,b) => a.localeCompare(b,'zh-CN'));
      select.add(new Option(all,''));
      for (const value of available) select.add(new Option(value,value));
      select.hidden = available.length === 0;
      select.addEventListener('change',redraw);
      group.append(select);
      return select;
    });
    before.parentElement.after(group);
    before.addEventListener('click', () => {for (const select of selects) select.value = '';});
    return (item,query) => {
      const record = index.get(item);
      return matches(record,query) && selects.every((select,i) => !select.value || record.features[i].includes(select.value));
    };
  }
  globalThis.GallerySearch = {describe,matches,setup,formatDate};
})();
