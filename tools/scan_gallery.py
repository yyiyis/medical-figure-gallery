#!/usr/bin/env python3
"""Find licensed article graphics and update the public gallery from a GitHub runner."""

import argparse
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
NCBI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
PMC = 'https://pmc-oa-opendata.s3.amazonaws.com/'
CROSSREF = 'https://api.crossref.org/'
XLINK = '{http://www.w3.org/1999/xlink}href'
LICENSES = {'CC BY': 'by', 'CC BY-NC': 'by-nc', 'CC BY-NC-ND': 'by-nc-nd'}
RETRY_STATUS = {429, 500, 502, 503, 504}
FIGURE_LABEL = re.compile(r'graphical.abstract|visual.abstract|central.illustration', re.I)
STUDY = re.compile(r'\b(cohort|biobank|participants|randomi[sz]ed|patients|registry|population.based|case.control|longitudinal|epidemiolog)\w*\b', re.I)
TOPICS = {
    '暴露组': r'\bexposom\w*|cumulative exposur|environmental exposur|early.life exposur|joint exposur|exposure mixtures|multiple exposures',
    '生命历程': r'life.course|lifecourse|childhood|early.life|prenatal|adolescen|intergenerational|longitudinal trajector',
    '环境健康': r'air pollution|particulate matter|PM2\.5|ambient heat|temperature|climate change|built environment|environmental justice|environmental epidemiology|traffic noise|greenness|wildfire smoke|lead exposure|PFAS|perfluoro|pesticides|drinking water',
    '组学': r'\b(?:multi.?)?omics\b|\b(?:proteom|metabolom|epigenom|transcriptom|genom)\w*\b',
    '老龄化': r'\b(?:aging|ageing|frailty|dementia|multimorbidity|healthspan|longevity)\b',
    '心血管': r'cardiovascular|heart failure|stroke|coronary|cardiometabolic|atherosclero',
    '人群研究': r'\bcohort\b|population.based|epidemiolog|risk prediction|disease trajectories',
}


def request(url, *, part=False, limit=None):
    headers = {'User-Agent': 'MedicalFigureGallery/1.0 https://github.com/yyiyis/medical-figure-gallery'}
    if part:
        headers['Range'] = 'bytes=0-131071'
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=16) as resp:
                return resp.read(limit)
        except urllib.error.HTTPError as error:
            if error.code not in RETRY_STATUS or attempt == 2:
                raise
            delay = error.headers.get('Retry-After', '')
            time.sleep(min(int(delay), 40) if delay.isdigit() else 2 ** (attempt + 1))
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 ** (attempt + 1))


def read_json(url):
    return json.loads(request(url))


def eutils(endpoint, **fields):
    time.sleep(.38)
    args = urllib.parse.urlencode({'db': 'pubmed', 'tool': 'medical_figure_gallery', **fields})
    return request(NCBI + endpoint + '.fcgi?' + args)


def json_section(document, name, fallback=None):
    pattern = r'<script id="' + re.escape(name) + r'"[^>]*>\s*(.*?)</script>'
    match = re.search(pattern, document, re.S)
    return json.loads(match[1]) if match else fallback


def set_section(document, name, value):
    safe = json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    block = '<script id="' + name + '" type="application/json">\n' + safe + '\n</script>'
    pattern = r'<script id="' + re.escape(name) + r'"[^>]*>.*?</script>'
    if re.search(pattern, document, re.S):
        return re.sub(pattern, lambda _: block, document, count=1, flags=re.S)
    return document.replace('<script id="catalog"', block + '\n<script id="catalog"', 1)


def text_of(node):
    return ' '.join(''.join(node.itertext()).split()) if node is not None else ''


def exact_date(parts):
    if len(parts) != 3 or not all(parts):
        return None
    try:
        return date(*map(int, parts))
    except ValueError:
        return None


def article_date(record):
    paths = (
        ".//ArticleDate[@DateType='Electronic']",
        ".//PubMedPubDate[@PubStatus='epublish']",
        ".//PubMedPubDate[@PubStatus='aheadofprint']",
    )
    online = [exact_date([node.findtext(k) for k in ('Year','Month','Day')])
              for path in paths for node in record.findall(path)]
    return min((value for value in online if value), default=None)


def find_pmids(journal, start, end):
    name = journal['pubmed']
    term = f'"{name}"[jour] AND ({start:%Y/%m/%d}:{end:%Y/%m/%d}[epdat] OR {start:%Y/%m/%d}:{end:%Y/%m/%d}[dp])'
    result = json.loads(eutils('esearch', term=term, retmode='json', retmax=10000))['esearchresult']
    if result.get('errorlist'):
        raise ValueError(f'PubMed query: {result["errorlist"]}')
    count = int(result['count'])
    if count > 9999:
        if start == end:
            raise ValueError('PubMed result exceeds the daily retrieval limit')
        middle = start + (end-start)//2
        return sorted(set(find_pmids(journal, start, middle) + find_pmids(journal, middle + timedelta(days=1), end)))
    ids = result['idlist']
    if len(ids) != count:
        raise ValueError(f'PubMed returned {len(ids)} of {count} IDs')
    return ids


def fetch_records(ids):
    for offset in range(0, len(ids), 160):
        chunk = ids[offset:offset+160]
        records = ET.fromstring(eutils('efetch', id=','.join(chunk), retmode='xml'))
        for article in records.findall('PubmedArticle'):
            yield article


def study_topics(title, abstract):
    text = title + ' ' + abstract
    if not STUDY.search(text):
        return []
    return [name for name, pattern in TOPICS.items() if re.search(pattern, text, re.I)]


def image_size(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 24:
        return int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
    if not data.startswith(b'\xff\xd8'):
        return None
    offset = 2
    frame_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while offset + 9 <= len(data) and data[offset] == 255:
        marker = data[offset+1]
        if marker == 255:
            offset += 1
            continue
        if marker in frame_markers:
            return int.from_bytes(data[offset+7:offset+9], 'big'), int.from_bytes(data[offset+5:offset+7], 'big')
        if marker in {0xDA, 0xD9}:
            return None
        size = int.from_bytes(data[offset+2:offset+4], 'big')
        if size < 2:
            return None
        offset += size + 2
    return None


def inspect_image(url):
    return image_size(request(url, part=True, limit=131072))


def pmc_version(pmcid):
    args = urllib.parse.urlencode({'list-type': 2, 'prefix': pmcid + '.'})
    tree = ET.fromstring(request(PMC + '?' + args))
    objects = {o.findtext('{*}Key'): o.findtext('{*}ETag') for o in tree.findall('{*}Contents')}
    if tree.findtext('{*}IsTruncated') == 'true':
        raise ValueError('Incomplete PMC object listing')
    versions = [k for k in objects if re.fullmatch(re.escape(pmcid) + r'\.\d+/' + re.escape(pmcid) + r'\.\d+\.json', k)]
    if not versions:
        return None, {}
    version = max(versions, key=lambda key: int(key.split('/')[0].rsplit('.', 1)[1]))
    prefix = version.split('/')[0] + '/'
    return version, {k: v for k, v in objects.items() if k.startswith(prefix)}


def named_graphics(xml):
    for node in xml.iter():
        if node.tag not in {'abstract', 'fig', 'sec'}:
            continue
        name = ' '.join([node.get('abstract-type', ''), node.get('sec-type', ''), text_of(node.find('label')), text_of(node.find('title'))])
        is_graphical_abstract = node.tag == 'abstract' and node.get('abstract-type','').casefold() == 'graphical'
        if not is_graphical_abstract and not FIGURE_LABEL.search(name):
            continue
        if node.find('.//permissions') is not None:
            continue
        for graphic in node.iter('graphic'):
            file = graphic.get(XLINK, '')
            if file:
                yield name.strip(), file


def licensed_graphic(article):
    version, files = pmc_version(article['pmcid'])
    if not version:
        return None, 'missing_pmc_version'
    metadata = read_json(PMC + version)
    licence = LICENSES.get(metadata.get('license_code'))
    if not licence:
        return None, 'licence_unconfirmed'
    xml = ET.fromstring(request(PMC + version.removesuffix('.json') + '.xml'))
    permissions = xml.find('./front/article-meta/permissions')
    evidence = ET.tostring(permissions, encoding='unicode') if permissions is not None else ''
    license_links = set(re.findall(r'https?://creativecommons\.org/licenses/([a-z-]+)/(\d\.\d)', evidence, re.I))
    if license_links != {(licence, '4.0')}:
        return None, 'licence_unconfirmed'
    possibilities = list(named_graphics(xml))
    if not possibilities:
        return None, 'no_label_in_pmc'
    seen = set()
    for label, file in possibilities:
        leaf = file.rsplit('/', 1)[-1]
        keys = [k for k in files if k.rsplit('/', 1)[-1] in {leaf, leaf + '.jpg', leaf + '.png', leaf + '.jpeg'}]
        for key in keys:
            if not re.search(r'\.(?:jpe?g|png)$', key, re.I):
                continue
            fingerprint = files[key] or key
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            preview = PMC + urllib.parse.quote(key, safe='/')
            try:
                before = inspect_image(preview)
            except (urllib.error.URLError, TimeoutError):
                continue
            if not before:
                continue
            size = before
            original = None
            pii = re.sub(r'[^A-Za-z0-9]', '', article.get('pii', ''))
            name = key.rsplit('/', 1)[-1].rsplit('.', 1)[0]
            if re.fullmatch(r'S[A-Za-z0-9]{10,24}',pii) and re.fullmatch(r'ga\d+|gr\d+|fx\d+',name):
                direct = f'https://ars.els-cdn.com/content/image/1-s2.0-{pii}-{name}_lrg.jpg'
                try:
                    high = inspect_image(direct)
                    if high and high[0] > before[0] and abs(high[0]/high[1] - before[0]/before[1]) < .02:
                        size, original = high, direct
                except (urllib.error.URLError, TimeoutError):
                    pass
            if size[0] < 1200:
                continue
            row = make_row(article, preview, licence, size, 'PubMed Central 收录版', original)
            return row, 'candidate'
    return None, 'image_unavailable_or_small'


def make_row(article, image, licence, size, attribution, original=None):
    figure = {'width': size[0], 'height': size[1], 'doi': article['doi'], 'published': article['published'].isoformat()}
    if original:
        figure['url'] = original
    return ['abstract', article['journal'], article['published'].year, article['title'], '|'.join(article['topics']),
            '', 'https://doi.org/' + article['doi'], image, article['author'] + ' · ' + attribution, licence, figure]


def article_info(record, journal, start, end):
    article = record.find('./MedlineCitation/Article')
    if article is None:
        return None, 'no_article_metadata'
    excluded = {'Editorial', 'News', 'Published Erratum', 'Letter', 'Comment', 'Retracted Publication', 'Retraction of Publication'}
    if excluded.intersection(text_of(pt) for pt in article.findall('.//PublicationType')):
        return None, 'article_type_excluded'
    title = text_of(article.find('ArticleTitle'))
    topics = study_topics(title, text_of(article.find('Abstract')))
    if not topics:
        return None, 'outside_topic_filter'
    online = article_date(record)
    if not online:
        return None, 'date_needs_confirmation'
    if not start <= online <= end:
        return None, 'outside_online_date'
    ids = {k.get('IdType'): k.text or '' for k in record.findall('./PubmedData/ArticleIdList/ArticleId')}
    if not ids.get('doi'):
        return None, 'doi_missing'
    author = article.findtext('.//AuthorList/Author/LastName') or article.findtext('.//AuthorList/Author/CollectiveName') or journal
    return {'title': title, 'topics': topics, 'published': online, 'doi': ids['doi'].lower(), 'journal': journal,
            'author': author + ' 等', 'pmcid': ids.get('pmc'), 'pii': ids.get('pii') or ''}, None


def publisher_date(items):
    values = [exact_date(parts) for f in ('published-online',) for parts in items.get(f,{}).get('date-parts',[])]
    return min((value for value in values if value), default=None)


def publisher_index(journal, start, end):
    query = {'filter': f'from-pub-date:{start},until-pub-date:{end}', 'cursor': '*', 'rows': 100}
    seen = set()
    while True:
        url = CROSSREF + 'journals/' + journal['issn'] + '/works?' + urllib.parse.urlencode(query)
        results = read_json(url)['message']
        if not results['items']:
            break
        for item in results['items']:
            doi = item.get('DOI','').lower()
            if doi and doi not in seen:
                seen.add(doi)
                yield item
        if len(results['items']) < query['rows'] or results.get('next-cursor') == query['cursor']:
            break
        query['cursor'] = results['next-cursor']


def tag_content(page, name):
    for tag in re.findall(r'<meta\b[^>]+>',page,re.I):
        attrs = dict(re.findall(r'([\w-]+)\s*=\s*["\']([^"\']*)["\']',tag))
        if attrs.get('name','').lower() == name:
            return html.unescape(attrs.get('content',''))
    return ''


def innovation_article(item, journal, start, end):
    doi = item['DOI'].lower()
    official = 'https://www.the-innovation.org/article/doi/' + urllib.parse.quote(doi,safe='/')
    page = request(official).decode('utf-8',errors='replace')
    if tag_content(page,'citation_doi').lower() != doi:
        return None, 'publisher_identity_unconfirmed'
    title = tag_content(page,'citation_title') or (item.get('title') or [''])[0]
    abstract = tag_content(page,'description') or item.get('abstract','')
    topics = study_topics(title,abstract)
    if not topics:
        return None, 'outside_topic_filter'
    online = publisher_date(item)
    if not online:
        for name in ('citation_online_date','citation_publication_date'):
            value = tag_content(page,name)
            if re.fullmatch(r'\d{4}[-/]\d{2}[-/]\d{2}',value):
                online = exact_date(re.split('[-/]',value))
                if online:
                    break
    if not online:
        return None, 'date_needs_confirmation'
    if not start <= online <= end:
        return None, 'outside_online_date'
    if not re.search(r'<a\b[^>]*href="https://creativecommons\.org/licenses/by/4\.0/"[^>]*class="cc-link"',page):
        return None, 'licence_unconfirmed'
    match = re.search(r'<img\b[^>]*src\s*=\s*["\'](https://data\.the-innovation\.org/[^"\']*/PIC/[^"\']*Abstract[^"\']*)["\'][^>]*class="figure_img"',page,re.I)
    if not match:
        return None, 'no_publisher_graphical_abstract'
    media = html.unescape(match[1])
    size = inspect_image(media)
    if not size or size[0] < 1200:
        return None, 'image_unavailable_or_small'
    author = tag_content(page,'citation_author') or journal['name']
    article = {'doi':doi, 'journal':journal['name'], 'title':title, 'published':online, 'author':author+' 等', 'topics':topics}
    return make_row(article,media,'by',size,'期刊图文摘要'), 'candidate'


def safe_graphic(article):
    try:
        return licensed_graphic(article)
    except (OSError, ET.ParseError, ValueError, KeyError) as error:
        print(f"[figure] {article['doi']}: {type(error).__name__} {error}",flush=True)
        return None, 'figure_check_failed'


def scan_journal(journal, start, end):
    from collections import Counter
    counts = Counter()
    candidates = []
    errors = []
    def add(row, reason):
        counts[reason] += 1
        if row:
            candidates.append(row)
    try:
        if journal['pubmed']:
            ids = find_pmids(journal,start,end)
            counts['indexed'] = len(ids)
            todo = []
            for record in fetch_records(ids):
                counts['metadata_read'] += 1
                article, reason = article_info(record,journal['name'],start,end)
                if not article:
                    counts[reason] += 1
                elif not article['pmcid']:
                    counts['publisher_review'] += 1
                else:
                    todo.append(article)
            if counts['metadata_read'] != counts['indexed']:
                raise ValueError('PubMed metadata count differs from the count of retrieved IDs')
            with ThreadPoolExecutor(max_workers=5) as pool:
                for row, reason in pool.map(safe_graphic,todo):
                    add(row,reason)
        else:
            articles = list(publisher_index(journal,start,end))
            counts['indexed'] = len(articles)
            for article in articles:
                counts['metadata_read'] += 1
                if journal['name'] != 'The Innovation Medicine':
                    counts['publisher_review'] += 1
                    continue
                try:
                    add(*innovation_article(article,journal,start,end))
                except (OSError, ET.ParseError, ValueError, KeyError) as error:
                    counts['figure_check_failed'] += 1
                    errors.append(f"{article.get('DOI','')}: {type(error).__name__}")
    except (OSError, ET.ParseError, ValueError, KeyError) as error:
        errors.append(f'{type(error).__name__}: {error}')
    result = {'name':journal['name'],'counts':dict(counts),'errors':errors}
    print(json.dumps(result,ensure_ascii=False),flush=True)
    return candidates,result


def normalize_value(text):
    return re.sub(r'\W+','',text.casefold())


def extend_catalog(current, candidates):
    titles = {normalize_value(r[3]) for r in current}
    links = {x for r in current for x in (r[6], r[7] if len(r)>7 else None, r[10].get('doi') if len(r)>10 else None) if x}
    added = []
    for row in sorted(candidates,key=lambda r:r[10]['published'],reverse=True):
        title = normalize_value(row[3])
        if title in titles or any(url in links for url in (row[6],row[7],row[10]['doi'])):
            continue
        if row[10].get('url') in links:
            continue
        titles.add(title)
        links.update({row[6],row[7],row[10]['doi']})
        added.append(row)
    return added + current, added


def update_stamp(document, history, latest):
    note = f'计划盘点 {history["start"]} 至 {history["end"]} 首次线上发表的文章。'
    if history.get('results'):
        indexed = sum(r['counts'].get('metadata_read',0) for r in history['results'])
        completed = sum(not r['errors'] for r in history['results'])
        note += f' 历史目录已扫描 {completed}/{len(history["results"])} 刊，共读取 {indexed:,} 条记录。'
    if latest:
        note += ' 最近发布 ' + latest['stamp'] + '（北京时间）。本次扫描 ' + latest['start'] + ' 至 ' + latest['end'] + '，新增 ' + str(latest.get('candidates',0)) + ' 张图文摘要。'
    pattern = r'(<p id="coverage-status">).*?(</p>)'
    return re.sub(pattern,lambda m:m[1]+html.escape(note)+m[2],document,count=1,flags=re.S)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('pilot','backfill','weekly'),required=True)
    parser.add_argument('--journal',default='')
    parser.add_argument('--start')
    parser.add_argument('--end')
    parser.add_argument('--publish',action='store_true')
    parser.add_argument('--report',type=Path,default=Path('scan-result.json'))
    options = parser.parse_args()
    document = INDEX.read_text(encoding='utf-8')
    registry = json_section(document,'journal-registry')
    all_journals = [journal for group in registry['groups'] for journal in group['journals']]
    lookup = {journal['name']:journal for journal in all_journals}
    selected = [name.strip() for name in options.journal.split(',') if name.strip()]
    if options.mode == 'pilot' and not selected:
        selected = ['JACC: Advances','The Innovation Medicine']
    invalid = sorted(set(selected).difference(lookup))
    if invalid:
        raise SystemExit(f'Unknown journals: {invalid}')
    journals = [lookup[name] for name in selected] if selected else all_journals
    now = datetime.now(ZoneInfo('Asia/Shanghai'))
    stop = date.fromisoformat(options.end or (now.date().isoformat() if options.mode == 'weekly' else registry['end']))
    begin = date.fromisoformat(options.start or ((stop-timedelta(days=27)).isoformat() if options.mode == 'weekly' else registry['start']))
    if stop < begin:
        raise SystemExit('End must not be earlier than start')
    entries = []
    checks = []
    for journal in journals:
        if options.mode == 'weekly' and journal.get('archive') and not journal.get('track'):
            continue
        candidates, result = scan_journal(journal,begin,stop)
        entries.extend(candidates)
        checks.append(result)
    run = {'mode':options.mode, 'start':str(begin), 'end':str(stop), 'stamp':now.strftime('%Y-%m-%d %H:%M'), 'results':checks}
    catalog, added = extend_catalog(json_section(document,'catalog'),entries)
    run['candidates'] = len(added)
    options.report.write_text(json.dumps({**run,'items':added},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Processed {len(checks)} journals and identified {len(added)} new graphical abstract candidates.',flush=True)
    for row in added:
        print(json.dumps({'doi':row[10]['doi'],'journal':row[1],'title':row[3],'size':[row[10]['width'],row[10]['height']], 'published':row[10]['published'],'image':row[10].get('url',row[7]),'licence':row[9]},ensure_ascii=False),flush=True)
    if not checks or all(r['errors'] for r in checks):
        raise SystemExit('No journal was scanned successfully')
    if options.publish:
        if options.mode == 'pilot':
            raise SystemExit('A pilot run does not publish')
        progress = json_section(document,'collection-report',{})
        if options.mode == 'backfill':
            progress['history'] = run
        progress['latest'] = run
        plan = progress.get('history',{'start':registry['start'],'end':registry['end']})
        changed = set_section(set_section(document,'catalog',catalog),'collection-report',progress)
        INDEX.write_text(update_stamp(changed,plan,run),encoding='utf-8')


if __name__ == '__main__':
    main()

