"""Serve previously published open-license figures from the gallery site."""

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit
import http.client

from scan_gallery import image_size, json_section, request, set_section

IMAGE_HOSTS = {
    'ars.els-cdn.com',
    'cdn.ncbi.nlm.nih.gov',
    'data.the-innovation.org',
    'media.springernature.com',
    'oup.silverchair-cdn.com',
    'pmc-oa-opendata.s3.amazonaws.com',
    'wwwnc.cdc.gov',
}
LICENSES = {'by', 'by-nc', 'by-nc-nd', 'pd'}
MAX_BYTES = 8_000_000


def archive_image(row, root):
    if len(row) < 11 or row[9] not in LICENSES or not row[7].startswith('https://'):
        return row
    image = row[7]
    quality = dict(row[10])
    urls = dict.fromkeys((quality.get('url') or image, image))
    for url in urls:
        parts = urlsplit(url)
        if parts.scheme != 'https' or parts.hostname not in IMAGE_HOSTS:
            continue
        if parts.hostname == 'data.the-innovation.org':
            url = url.replace('.org//', '.org/')
        try:
            payload = request(url, limit=MAX_BYTES + 1)
            dimensions = image_size(payload)
            if len(payload) > MAX_BYTES or not dimensions or min(dimensions) <= 0:
                continue
        except (OSError, http.client.HTTPException, ValueError) as error:
            print(f'Figure source unavailable for {row[3]}: {type(error).__name__}', flush=True)
            continue
        extension = '.webp' if payload.startswith(b'RIFF') else '.png' if payload.startswith(b'\x89PNG') else '.jpg'
        reference = Path('assets/reference') / (sha256(payload).hexdigest()[:24] + extension)
        dest = root / reference
        if not dest.exists():
            dest.write_bytes(payload)
        quality['backupUrl'] = url
        if url == quality.get('url'):
            quality.pop('url')
        quality.update(width=dimensions[0], height=dimensions[1])
        archived = list(row)
        archived[7] = reference.as_posix()
        archived[10] = quality
        return archived
    return row


IMAGE_LOADER = """  function loadImage(img, image, quality, onFailure, onReady) {
    const sources = image.startsWith('assets/reference/') ? [image, quality.url] : [quality.url, image];
    const urls = [...new Set([...sources, quality.backupUrl].filter(Boolean))];
    let next = 0;
    img.onload = onReady;
    img.onerror = () => {
      if (next < urls.length) img.src = urls[next++];
      else onFailure();
    };
    img.src = urls[next++];
  }
"""

CARD_IMAGE = """      const pending = el('span','preview-pending','图片加载中…');
      pending.setAttribute('aria-hidden', 'true');
      const failed = el('div','image-error');
      const retry = el('button','plain','重试');
      retry.type = 'button';
      failed.append('图片加载失败。 ', retry);
      const start = () => {
        failed.remove();
        preview.prepend(pending);
        preview.setAttribute('aria-busy','true');
        loadImage(img,image,quality,() => {
          preview.remove();
          box.prepend(failed);
        },() => {
          pending.remove();
          preview.removeAttribute('aria-busy');
        });
      };
      retry.addEventListener('click', () => {
        box.prepend(preview);
        start();
      });
      preview.append(img);
      preview.addEventListener('click', () => openImage(item));
      box.append(preview);
      start();
"""

STYLES = """
  .preview {position:relative}
  .preview[aria-busy] img {visibility:hidden}
  .preview-pending {position:absolute; inset:0; display:grid; place-items:center;
    padding:16px; color:var(--muted); background:var(--paper); font:inherit}
  .image-error .plain {margin-inline-start:4px}
"""


def improve_previews(document, root):
    if 'preview-pending' not in document:
        document = replace_block(document, '  function loadImage(', '  function setActualSize(', IMAGE_LOADER)
        document = replace_block(document, '      loadImage(img,image,quality,() => {',
                                 '    }\n    const content = el(', CARD_IMAGE)
        document = document.replace('</style>', STYLES + '</style>', 1)
        document = document.replace(
            '    viewerError.hidden = true;\n    viewerImage.hidden = false;',
            "    viewerError.textContent = '原图加载中…';\n    viewerError.hidden = false;\n    viewerImage.hidden = true;", 1)
        document = document.replace(
            '      viewerImage.hidden = true;\n      viewerError.hidden = false;\n      actualSize.disabled = true;\n    });',
            "      viewerError.textContent = '图片加载失败，可关闭后重试或打开原始出处。';\n"
            "      actualSize.disabled = true;\n    },() => {\n      viewerImage.hidden = false;\n      viewerError.hidden = true;\n    });", 1)

    rows = json_section(document, 'catalog')
    (root / 'assets/reference').mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        updated = list(pool.map(lambda row: archive_image(row, root), rows))
    new_count = sum(before is not after for before, after in zip(rows, updated))
    print(f'Archived {new_count} existing figure sources for on-site preview.', flush=True)
    return set_section(document, 'catalog', updated) if new_count else document


def replace_block(document, first, after, replacement):
    begin = document.index(first)
    end = document.index(after, begin + len(first))
    return document[:begin] + replacement + document[end:]
