(() => {
  'use strict';
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
      ['上海社区队列', /上海.{0,10}队列|shanghai community cohort/u],
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
    const [type, journal, year, title, keywords, note, , , , , extra] = item;
    const facts = clean([title, keywords, note, extra?.description].filter(Boolean).join(' '));
    const graphic = clean([note, keywords, type === 'figures' ? '组图' : ''].filter(Boolean).join(' '));
    const keys = ['topic', 'design', 'dataset', 'layout'];
    const features = facets.map(([, ,rules], i) => {
      const matched = rules.filter(([,rule]) => rule.test(i===3 ? graphic : facts)).map(([key]) => key);
      const explicit = extra?.features?.[keys[i]];
      return [...new Set([...matched, ...(Array.isArray(explicit) ? explicit : [])])];
    });
    const base = clean([kinds[type], journal, year, facts, ...features.flat()].join(' '));
    const text = [base, ...aliases.filter(group => group.some(term => hasTerm(base,term))).flat()].join(' ');
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
        return hasTerm(record.text,term) || term.length < 3 && record.text.includes(term);
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
  globalThis.GallerySearch = {describe,matches,setup};
})();
