"""Maintain the gallery interface without reserializing embedded data."""
from pathlib import Path
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

page.write_text(document, encoding='utf-8')
