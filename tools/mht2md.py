"""
mht2md.py - Convert OneNote pages exported as .mht into Markdown + compressed image files.

Usage:
  python mht2md.py <in_dir_with_mht> <out_md_dir> <out_img_root> <img_rel_prefix>

Every "NN - Title.mht" becomes <out_md_dir>/NN-title.md and its images go to
<out_img_root>/NN-title/imgK.png, referenced as <img_rel_prefix>/NN-title/imgK.png
"""
import sys, os, re, email, io
from email import policy
from bs4 import BeautifulSoup, NavigableString
from markdownify import MarkdownConverter
from PIL import Image

MAX_W = 1400
DATE_RE = re.compile(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?( [A-Z][a-z]+ \d{1,2}, \d{4})?$')
DATE2_RE = re.compile(r'^[A-Z][a-z]+ \d{1,2}, \d{4}$')
TIME_RE = re.compile(r'^\d{1,2}:\d{2}( [AP]M)?$')
ITEM_RE = re.compile(r'^(\d+)\. (.*)$')


def slugify(title):
    t = title.lower()
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t[:50].rstrip('-')


class Conv(MarkdownConverter):
    def convert_img(self, el, text, parent_tags):
        return '\n\n![sawir](' + el.get('src', '') + ')\n\n'


def compress(data, path):
    im = Image.open(io.BytesIO(data))
    if im.mode not in ('RGB', 'RGBA', 'P', 'L'):
        im = im.convert('RGB')
    if im.width > MAX_W:
        im = im.resize((MAX_W, int(im.height * MAX_W / im.width)), Image.LANCZOS)
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        im = bg
    if im.mode != 'P':
        im = im.convert('RGB').quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    im.save(path, 'PNG', optimize=True)


def clean_markdown(md, title):
    lines = md.split('\n')
    # drop OneNote header: title line + weekday/date/time lines at the very top
    i = 0
    while i < len(lines) and i < 12:
        s = lines[i].strip()
        if (not s or s == title.strip() or DATE_RE.match(s) or DATE2_RE.match(s)
                or TIME_RE.match(s) or s in ('AM', 'PM')):
            i += 1
        else:
            break
    lines = lines[i:]
    # OneNote exports every numbered item as its own <ol>, so items come out as "1." repeatedly.
    # Renumber runs of top-level items; a run is broken by a heading or a line of plain prose.
    out, run = [], []          # run = indexes (in out) of the items of the current list
    for ln in lines:
        m = ITEM_RE.match(ln)
        stripped = ln.strip()
        if ln.startswith('#'):
            run = []
        elif m:
            n = int(m.group(1))
            if n == 1:
                run.append(len(out))
                ln = f'{len(run)}. {m.group(2)}'
            else:
                # explicit number: the previous n-1 items of the run belong to this list
                keep = run[-(n - 1):] if 0 < n - 1 <= len(run) else []
                if len(keep) == n - 1:
                    for j, idx in enumerate(keep, 1):
                        out[idx] = re.sub(r'^\d+\. ', f'{j}. ', out[idx])
                    run = keep
                else:
                    run = []
                run.append(len(out))
                ln = f'{n}. {m.group(2)}'
        elif stripped and not ln.startswith((' ', '\t', '-', '!', '`', '|', '>')):
            run = []
        out.append(ln)
    md = '\n'.join(out)
    md = re.sub(r'\n{3,}', '\n\n', md).strip() + '\n'
    return f'# {title.strip()}\n\n' + md


def convert(mht_path, md_path, img_dir, img_rel, title):
    with open(mht_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    html_part, images = None, {}
    for part in msg.walk():
        ct = part.get_content_type()
        loc = part.get('Content-Location', '') or ''
        if ct == 'text/html' and html_part is None:
            html_part = part.get_content()
        elif ct.startswith('image/'):
            images[loc] = (ct, part.get_payload(decode=True))
    if html_part is None:
        raise RuntimeError('no html part in ' + mht_path)
    soup = BeautifulSoup(html_part, 'html.parser')
    for t in soup(['style', 'script', 'meta', 'link', 'title']):
        t.decompose()
    # OneNote hard-wraps text inside paragraphs: collapse whitespace in text nodes
    for node in soup.find_all(string=True):
        if isinstance(node, NavigableString) and node.parent.name not in ('pre', 'code'):
            node.replace_with(re.sub(r'\s+', ' ', str(node)))
    os.makedirs(img_dir, exist_ok=True)
    k = 0
    for img in soup.find_all('img'):
        src = img.get('src', '')
        key = src if src in images else None
        if key is None:
            base = os.path.basename(src)
            cand = [l for l in images if l.endswith(base)]
            key = cand[0] if cand else None
        if key is None:
            img.decompose()
            continue
        ct, data = images[key]
        k += 1
        name = f'img{k:02d}.png'
        compress(data, os.path.join(img_dir, name))
        img.attrs = {'src': f'{img_rel}/{name}', 'alt': 'sawir'}
    md = Conv(heading_style='ATX', bullets='-', strip=['span', 'font']).convert(str(soup))
    md = md.replace('\xa0', ' ')
    md = re.sub(r'[ \t]+\n', '\n', md)
    md = clean_markdown(md, title)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    return k, len(md)


if __name__ == '__main__':
    in_dir, out_md, out_img, rel = sys.argv[1:5]
    os.makedirs(out_md, exist_ok=True)
    for fn in sorted(os.listdir(in_dir)):
        if not fn.lower().endswith('.mht'):
            continue
        m = re.match(r'(\d+) - (.*)\.mht$', fn)
        num, title = m.group(1), m.group(2)
        slug = f'{num}-{slugify(title)}'
        k, n = convert(os.path.join(in_dir, fn), os.path.join(out_md, slug + '.md'),
                       os.path.join(out_img, slug), f'{rel}/{slug}', title)
        print(f'{slug}: {k} images, {n} chars')
