"""Publish individually reviewed figures from the 2025 archive."""
from datetime import date
import json
from pathlib import Path

from preview_gallery import archive_image
from scan_gallery import json_section, set_section

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/reviews/2025-figures.json'
CATALOGUE = ROOT / 'index.html'


def publish(document, review, root):
    catalogue = json_section(document, 'catalog')
    registry = json_section(document, 'journal-registry')
    registered = {journal['name'] for group in registry['groups'] for journal in group['journals']}
    by_link = {row[6]: row for row in catalogue}
    for item in review['dateCorrections']:
        existing = by_link[item['source']]
        value = date.fromisoformat(item['published'])
        existing[2] = value.year
        if len(existing) == 10:
            existing.append({})
        existing[10].update(doi=item['doi'], published=value.isoformat())

    known = {identifier for row in catalogue for identifier in (
        row[6], row[10].get('doi', '').casefold() if len(row) > 10 else ''
    ) if identifier}
    added = []
    (root / 'assets/reference').mkdir(parents=True, exist_ok=True)
    for row in review['figures']:
        kind, journal, year, title, tags, note, source, image, credit, licence, meta = row
        published = date.fromisoformat(meta['issueDate'] if kind == 'cover' else meta['published'])
        identity = meta['doi'].casefold()
        if (kind not in {'abstract', 'figures', 'cover'} or year != 2025 or published.year != year
                or journal not in registered or not all((title, tags, note, credit, meta['titleEn'], meta['noteEn']))
                or licence not in {'by', 'by-nc', 'by-nc-nd', 'pd'} or not source.startswith('https://')
                or not image.startswith('https://') or not identity or min(meta['width'], meta['height']) < 650):
            raise ValueError(f'Invalid reviewed entry: {source}')
        if source in known or identity in known:
            continue
        result = archive_image(row, root)
        if result is row or (result[10]['width'], result[10]['height']) != (meta['width'], meta['height']):
            raise ValueError(f'Missing or changed publisher original: {source}')
        known.update((source, identity))
        added.append(result)

    if added:
        existing_2025 = next((i for i, row in enumerate(catalogue) if row[2] == 2025), len(catalogue))
        catalogue[existing_2025:existing_2025] = sorted(
            added, key=lambda row: row[10].get('published', row[10].get('issueDate', '')), reverse=True
        )
    print(f'Added {len(added)} individually reviewed 2025 figures.', flush=True)
    return set_section(document, 'catalog', catalogue)


def main():
    if MANIFEST.exists():
        document = CATALOGUE.read_text(encoding='utf-8')
        updated = publish(document, json.loads(MANIFEST.read_text(encoding='utf-8')), ROOT)
        if updated != document:
            CATALOGUE.write_text(updated, encoding='utf-8')


if __name__ == '__main__':
    main()
