"""Maintain the gallery interface without reserializing embedded data."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parent.parent
page = root / 'index.html'
document = page.read_text(encoding='utf-8')


def replace_once(old, new):
    global document
    if document.count(old) != 1:
        raise ValueError(f'Expected one match for {old[:100]!r}')
    document = document.replace(old, new, 1)


if (root / 'assets' / 'gallery-style.css').is_file() and 'href="assets/gallery-style.css"' not in document:
    replace_once('</head>', '<link rel="stylesheet" href="assets/gallery-style.css">\n</head>')
    old_scope = '<p>关注人群和临床研究、长期与累积环境暴露，以及代谢组、蛋白组、遗传组和多组学整合。优先收录正式图文摘要，精选正文组图与封面。</p>'
    replace_once(old_scope, '<p>按学科浏览期刊。已收录的图片可在本页查看。</p>')
    replace_once(
        "    const count = registry.groups.reduce((total,group) => total + group.journals.length,0);",
        "    const tracked = registry.groups.flatMap(group => group.journals);\n"
        "    const count = tracked.length;\n"
        "    const covered = tracked.filter(journal => imagesPerJournal.has(journal.name)).length;"
    )
    replace_once(" + imagesPerJournal.size + ' 刊可预览';", " + covered + ' 刊可预览';")

if (root / 'assets' / 'gallery-search.js').is_file() and 'src="assets/gallery-search.js"' not in document:
    replace_once('<script>(function gallery() {',
                 '<script src="assets/gallery-search.js"></script>\n<script>(function gallery() {')
    replace_once('placeholder="搜索研究主题、期刊或作图方式"', 'placeholder="搜索，例如 UKB、组学或桑基图"')
    old_render = re.search(r'  function normalized\(text\).*?(?=    for \(const \[type, tab\] of tabs\))',
                           document, re.S)
    if old_render is None:
        raise ValueError('Previous search block missing')
    replace_once(old_render[0], """  const matchesFigure = GallerySearch.setup(items, document.querySelector('#reset'), render);
  function render() {
    const available = scope();
    if (category !== 'all' && !available.some(item => item[0] === category)) category = 'all';
    const results = available.filter(item => (category === 'all' || item[0] === category)
      && (!journal.value || journal.value === item[1]) && matchesFigure(item, search.value));
""")

# Journal names and NLM index abbreviations used for the 2026 extension.
JOURNAL_ADDITIONS = {
    '综合医学': [
        ('eClinicalMedicine', 'EClinicalMedicine'),
        ('BMJ Medicine', 'BMJ Med'),
        ('eBioMedicine', 'EBioMedicine'),
        ('The Lancet Regional Health – Europe', 'Lancet Reg Health Eur'),
        ('The Lancet Regional Health – Americas', 'Lancet Reg Health Am'),
    ],
    '心血管病学': [
        ('JACC: Asia', 'JACC Asia'),
        ('JACC: Cardiovascular Imaging', 'JACC Cardiovasc Imaging'),
        ('JACC: Clinical Electrophysiology', 'JACC Clin Electrophysiol'),
        ('European Journal of Heart Failure', 'Eur J Heart Fail'),
        ('Hypertension', 'Hypertension'),
        ('Circulation: Population Health and Outcomes', 'Circ Popul Health Outcomes'),
    ],
    '流行病学与公共卫生': [
        ('Journal of Clinical Epidemiology', 'J Clin Epidemiol'),
        ('JAMA Health Forum', 'JAMA Health Forum'),
        ('Nature Health', 'issn:3005-0693'),
    ],
    '环境健康': [('Environmental Science & Technology', 'Environ Sci Technol')],
    '老年医学与老龄化研究': [
        ('GeroScience', 'Geroscience'),
        ('Aging Cell', 'Aging Cell'),
        ('npj Aging', 'NPJ Aging'),
    ],
    '内分泌与代谢': [
        ('The Lancet Diabetes & Endocrinology', 'Lancet Diabetes Endocrinol'),
        ('Diabetes Care', 'Diabetes Care'),
    ],
    '神经病学与脑健康': [
        ('JAMA Neurology', 'JAMA Neurol'),
        ('The Lancet Neurology', 'Lancet Neurol'),
        ('Brain Health', 'issn:3142-9963'),
    ],
    '呼吸医学': [
        ('European Respiratory Journal', 'Eur Respir J'),
        ('American Journal of Respiratory and Critical Care Medicine', 'Am J Respir Crit Care Med'),
    ],
    '感染病学': [('Clinical Infectious Diseases', 'Clin Infect Dis')],
    '数字医学': [
        ('PLOS Digital Health', 'PLOS Digit Health'),
        ('Journal of Medical Internet Research', 'J Med Internet Res'),
    ],
}


# Only replace the registry payload so existing figures and reports stay intact.
registry_script = re.search(r'(<script id="journal-registry"[^>]*>)(.*?)(</script>)', document, re.S)
if not registry_script:
    raise ValueError('Journal registry missing')
registry = json.loads(registry_script[2])
legacy_group = next((group for group in registry['groups'] if group['title'] == '神经病学'), None)
if legacy_group is not None:
    legacy_group['title'] = '神经病学与脑健康'
by_group = {group['title']: group for group in registry['groups']}
existing = {journal['name'] for group in registry['groups'] for journal in group['journals']}
original_count = len(existing)
for group, additions in JOURNAL_ADDITIONS.items():
    for name, index in additions:
        if name in existing:
            continue
        journal = {'name': name, 'pubmed': index}
        if index.startswith('issn:'):
            journal.update(pubmed=None, issn=index.removeprefix('issn:'))
        by_group[group]['journals'].append(journal)
        existing.add(name)
exposome = next(journal for group in registry['groups'] for journal in group['journals']
                if journal['name'] == 'Exposome')
enable_exposome = exposome.get('track') is not True
if enable_exposome:
    exposome['track'] = True
if len(existing) != original_count or legacy_group is not None or enable_exposome:
    updated = '\n' + json.dumps(registry, ensure_ascii=False, indent=2) + '\n'
    document = document[:registry_script.start(2)] + updated + document[registry_script.end(2):]

pending_label = "        else entry.append(el('span','scope-badge','暂无预览'));"
if pending_label not in document:
    old_badge = "        if (previewCount) entry.append(el('span','scope-badge',previewCount + ' 张图'));"
    replace_once(old_badge, old_badge + '\n' + pending_label)
    anchor = "    const covered = tracked.filter(journal => imagesPerJournal.has(journal.name)).length;"
    replace_once(anchor, anchor + "\n" + """    const progress = JSON.parse(document.querySelector('#collection-report').textContent);
    const scanned = new Set((progress.history?.results ?? []).filter(entry => !entry.errors.length).map(entry => entry.name));
    const pending = tracked.filter(journal => !scanned.has(journal.name)).length;
    if (pending) document.querySelector('#coverage-status').append(' 另有 ' + pending + ' 刊待完成历史目录盘点。');""")

if 'GallerySearch.formatDate(item)' not in document:
    replace_once('[types[kind],name,year]', '[types[kind],name,GallerySearch.formatDate(item)]')
    replace_once('[types[kind], journalName, year]', '[types[kind], journalName, GallerySearch.formatDate(item)]')

# Complete the publication month on the archived DETECT-AHEAD figure.
detect_image = 'https://pmc-oa-opendata.s3.amazonaws.com/PMC11296689.1/nihms-2012174-f0002.jpg'
detect_metadata = json.dumps({'width': 1200, 'height': 806}, separators=(',', ':'))
detect_credit = json.dumps('Quer 等，Figure 2（美国国家医学图书馆收录的作者终稿）', ensure_ascii=False)
detect_fields = f'"{detect_image}",{detect_credit},"by-nc-nd",'
previous_detect = detect_fields + detect_metadata
if previous_detect in document:
    updated_detect = json.dumps(
        {'width': 1200, 'height': 806, 'published': '2024-07-24'}, separators=(',', ':')
    )
    replace_once(previous_detect, detect_fields + updated_detect)

page.write_text(document, encoding='utf-8')
