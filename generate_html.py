#!/usr/bin/env python3
"""
Générateur HTML pour le cours de révision Anthropic Architect Pro.
Convertit les fichiers markdown du dossier cours/ en HTML avec design system intégré.
Usage : python3 generate_html.py
"""

import os
import re
import glob

PALETTE = {
    "blue": "#4f8ef7",
    "aqua": "#2dd4a0",
    "violet": "#a78bfa",
    "yellow": "#fbbf24",
    "red": "#f87171",
    "ink": "#c4bede",
    "bg": "#13151f",
    "surface": "#1c1f2e",
    "surface2": "#252840",
    "border": "#2e3250",
    "text": "#ddd8f0",
    "muted": "#7874a0",
}

HTML_HEADER = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anthropic Architect Pro — Cours de révision</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad: false, theme: 'dark', flowchart: {{ curve: 'basis' }} }});</script>
<style>
  :root {{
    --blue: {blue};
    --aqua: {aqua};
    --violet: {violet};
    --yellow: {yellow};
    --red: {red};
    --ink: {ink};
    --bg: {bg};
    --surface: {surface};
    --surface2: {surface2};
    --border: {border};
    --text: {text};
    --muted: {muted};
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-size: 15px;
    line-height: 1.7;
  }}
  a {{ color: var(--blue); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}

  /* Layout */
  .wrapper {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}

  /* TOC compact + dépliable */
  nav.toc {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.5rem;
    margin-bottom: 2.5rem;
  }}
  nav.toc > summary {{
    cursor: pointer; font-size: 0.75rem; text-transform: uppercase;
    letter-spacing: 0.12em; font-weight: 700; color: var(--muted);
    list-style: none; display: flex; align-items: center; gap: 0.5rem;
  }}
  nav.toc > summary::before {{ content: '▸'; transition: transform 0.2s; }}
  nav.toc[open] > summary::before {{ content: '▾'; }}
  nav.toc ol {{ padding-left: 1.1rem; margin-top: 0.8rem; }}
  nav.toc > ol > li {{ margin: 0.5rem 0; }}
  nav.toc details {{ margin: 0.2rem 0; }}
  nav.toc details summary {{
    cursor: pointer; color: var(--blue); font-size: 0.9rem; font-weight: 500;
    list-style: none; display: flex; align-items: center; gap: 0.4rem;
  }}
  nav.toc details summary::before {{ content: '▸'; font-size: 0.7rem; color: var(--muted); }}
  nav.toc details[open] summary::before {{ content: '▾'; }}
  nav.toc ul {{ list-style: none; padding-left: 1.2rem; margin-top: 0.3rem; }}
  nav.toc ul li {{ margin: 0.2rem 0; }}
  nav.toc ul li a {{ color: var(--muted); font-size: 0.84rem; }}
  nav.toc ul li a:hover {{ color: var(--blue); }}

  /* Sections dépliables */
  .section-wrap {{ margin: 2rem 0; }}
  .section-wrap > summary {{
    cursor: pointer; list-style: none;
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
  }}
  .section-wrap > summary h2 {{
    margin: 0; border: none; padding: 0; font-size: 1.25rem;
    font-weight: 700; color: var(--ink);
  }}
  .section-wrap > summary::before {{
    content: '▸'; color: var(--muted); font-size: 0.8rem; flex-shrink: 0;
    transition: transform 0.2s;
  }}
  .section-wrap[open] > summary::before {{ content: '▾'; }}
  .section-wrap > summary::-webkit-details-marker {{ display: none; }}
  .section-content {{ padding-top: 0.5rem; }}

  /* Headings */
  h1 {{ font-size: 1.8rem; font-weight: 700; color: var(--blue); margin-bottom: 0.3rem; }}
  h2 {{
    font-size: 1.25rem; font-weight: 700; color: var(--ink);
    margin: 2.5rem 0 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
  }}
  h3 {{ font-size: 1rem; font-weight: 600; color: var(--violet); margin: 1.6rem 0 0.6rem; }}

  /* Prose */
  p {{ margin-bottom: 0.8rem; color: var(--text); }}
  strong {{ color: var(--ink); font-weight: 700; }}
  em {{ color: var(--muted); font-style: italic; }}
  code {{
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px; padding: 0.1em 0.4em;
    font-family: 'Fira Code', 'Menlo', monospace; font-size: 0.86em;
    color: var(--violet);
  }}
  pre {{
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 1rem; overflow-x: auto; margin: 1rem 0;
  }}
  pre code {{ background: none; border: none; padding: 0; font-size: 0.86em; color: var(--text); }}

  /* Tables — compactes */
  table {{
    width: 100%; border-collapse: collapse; margin: 1rem 0;
    font-size: 0.88em;
  }}
  th {{
    background: var(--surface2); color: var(--ink);
    padding: 0.5rem 0.8rem; text-align: left; font-weight: 600;
    border-bottom: 1px solid var(--border);
  }}
  td {{ padding: 0.45rem 0.8rem; border-bottom: 1px solid var(--border); background: var(--surface); }}
  tr:last-child td {{ border-bottom: none; }}

  /* Callouts */
  .callout {{
    border-left: 3px solid var(--blue);
    background: rgba(79,142,247,0.08);
    border-radius: 0 6px 6px 0;
    padding: 0.75rem 1rem;
    margin: 1rem 0;
  }}
  .callout.insight {{ border-color: var(--aqua); background: rgba(45,212,160,0.08); }}
  .callout.warning {{ border-color: var(--yellow); background: rgba(251,191,36,0.08); }}
  .callout.rule {{ border-color: var(--violet); background: rgba(167,139,250,0.08); }}
  .callout.limit {{ border-color: var(--red); background: rgba(248,113,113,0.08); }}
  .callout.situation {{ border-color: var(--blue); background: rgba(79,142,247,0.05); }}
  .callout .callout-label {{
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em;
    font-weight: 700; margin-bottom: 0.35rem; color: var(--muted);
  }}
  .callout p {{ margin-bottom: 0.4rem; }}
  .callout p:last-child {{ margin-bottom: 0; }}

  /* Mermaid */
  .mermaid {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1.2rem 0;
    text-align: center;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }}
  .mermaid svg {{
    min-width: 480px;
  }}

  /* SVG */
  .diagram-wrap {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
    margin: 1.2rem 0;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }}
  .diagram-wrap svg {{
    display: block;
    min-width: 600px;
    height: auto;
  }}

  /* Flashcards — flip au clic */
  .flashcards-wrap {{
    display: flex; gap: 0.8rem; overflow-x: auto;
    padding-bottom: 0.6rem; margin: 1rem 0;
    scrollbar-width: thin;
  }}
  .flashcard {{
    min-width: 210px; max-width: 250px; flex-shrink: 0;
    height: 140px;
    perspective: 800px; cursor: pointer;
  }}
  .flashcard-inner {{
    position: relative; width: 100%; height: 100%;
    transition: transform 0.45s cubic-bezier(.4,0,.2,1);
    transform-style: preserve-3d;
  }}
  .flashcard.flipped .flashcard-inner {{ transform: rotateY(180deg); }}
  .flashcard-front, .flashcard-back {{
    position: absolute; inset: 0;
    backface-visibility: hidden;
    border-radius: 8px; padding: 0.9rem 1rem;
    border: 1px solid var(--border);
    display: flex; flex-direction: column; justify-content: center;
  }}
  .flashcard-front {{
    background: var(--surface);
    border-top: 2px solid var(--blue);
  }}
  .flashcard-back {{
    background: var(--surface2);
    border-top: 2px solid var(--aqua);
    transform: rotateY(180deg);
  }}
  .flashcard .fc-hint {{
    font-size: 0.65rem; color: var(--muted); margin-bottom: 0.4rem;
    text-transform: uppercase; letter-spacing: 0.08em;
  }}
  .flashcard .fc-q {{
    font-size: 0.84rem; color: var(--text); line-height: 1.4; font-weight: 500;
  }}
  .flashcard .fc-r {{
    font-size: 0.88rem; color: var(--text); line-height: 1.5;
  }}

  /* QCM */
  .qcm {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 1rem; margin: 1rem 0;
  }}
  .qcm .qcm-q {{ font-weight: 600; margin-bottom: 0.6rem; }}
  .qcm ol {{ padding-left: 1.2rem; }}
  .qcm li {{ margin: 0.3rem 0; }}
  details.qcm-answer {{ margin-top: 0.6rem; font-size: 0.88rem; }}
  details.qcm-answer summary {{ cursor: pointer; color: var(--muted); }}

  /* Lists */
  .callout ul, .callout ol {{ padding-left: 1.3rem; margin: 0.4rem 0; }}
  .callout li {{ margin: 0.25rem 0; }}
  ul {{ padding-left: 1.4rem; margin: 0.6rem 0; }}
  ol {{ padding-left: 1.4rem; margin: 0.6rem 0; }}
  li {{ margin: 0.3rem 0; }}

  blockquote {{
    border-left: 2px solid var(--border);
    padding: 0.2rem 0.9rem;
    color: var(--muted);
    margin: 0.7rem 0;
    font-style: italic;
  }}
  /* Navigation sections */
  .section {{ display: none; }}
  .section.active {{ display: block; }}

  .section-nav {{
    display: flex; align-items: center; justify-content: space-between;
    margin-top: 2rem; padding-top: 1.2rem;
    border-top: 1px solid var(--border);
    gap: 1rem;
  }}
  .nav-btn {{
    background: var(--surface2); color: var(--text);
    border: 1px solid var(--border); border-radius: 6px;
    padding: 0.5rem 1.1rem; cursor: pointer; font-size: 0.88rem;
    transition: background 0.15s, border-color 0.15s;
    font-family: inherit;
  }}
  .nav-btn:hover {{ background: var(--border); border-color: var(--blue); }}
  .nav-btn:disabled {{ opacity: 0.3; cursor: default; }}
  .nav-progress {{
    font-size: 0.78rem; color: var(--muted); text-align: center; flex: 1;
  }}
</style>
<script>
var _renderedSections = {{}};

function showSection(idx) {{
  const sections = document.querySelectorAll('.section');
  const total = sections.length;
  if (idx < 0 || idx >= total) return;

  sections.forEach((s, i) => s.classList.toggle('active', i === idx));
  document.querySelectorAll('.toc-link').forEach((l, i) => l.classList.toggle('toc-active', i === idx));

  // Update nav buttons in current section
  const activeSection = sections[idx];
  const btnPrev = activeSection.querySelector('.btn-prev');
  const btnNext = activeSection.querySelector('.btn-next');
  const prog = activeSection.querySelector('.nav-progress');
  if (btnPrev) btnPrev.disabled = idx === 0;
  if (btnNext) btnNext.disabled = idx === total - 1;
  if (prog) prog.textContent = (idx + 1) + ' / ' + total;

  window.currentSection = idx;
  localStorage.setItem('currentSection', idx);

  // Render mermaid only once per section, only when visible
  if (!_renderedSections[idx]) {{
    _renderedSections[idx] = true;
    const nodes = activeSection.querySelectorAll('.mermaid');
    if (nodes.length > 0) {{
      setTimeout(function() {{
        mermaid.run({{ nodes: nodes }});
      }}, 50);
    }}
  }}
  window.scrollTo(0, 0);
}}

document.addEventListener('DOMContentLoaded', function() {{
  const saved = parseInt(localStorage.getItem('currentSection') || '0');
  window.currentSection = 0;
  showSection(isNaN(saved) ? 0 : saved);
}});
</script>
</head>
<body>
<div class="wrapper">
<h1>Anthropic Certified Architect Pro<br><small style="font-size:0.5em;color:var(--muted);font-weight:400;">Cours de révision</small></h1>
""".format(**PALETTE)

HTML_FOOTER = """
</div>
</body>
</html>
"""


def parse_callout(block_type, content):
    labels = {
        "situation": "Situation réelle",
        "problem": "Problème",
        "rule": "Règle",
        "callout-insight": "A retenir",
        "warning": "Attention",
        "limit": "Limite",
    }
    css_class = block_type.replace("callout-", "")
    label = labels.get(block_type, block_type.upper())
    return (
        f'<div class="callout {css_class}">'
        f'<div class="callout-label">{label}</div>'
        f'{md_to_html_inline(content.strip())}'
        f'</div>'
    )


def parse_flashcards(content):
    cards = []
    current_q = None
    for line in content.strip().splitlines():
        line = line.strip()
        if line.startswith("Q:"):
            current_q = line[2:].strip()
        elif line.startswith("R:") and current_q:
            r = line[2:].strip()
            cards.append((current_q, r))
            current_q = None
    if not cards:
        return ""
    items = ""
    for q, r in cards:
        items += (
            f'<div class="flashcard" onclick="this.classList.toggle(\'flipped\')">'
            f'<div class="flashcard-inner">'
            f'<div class="flashcard-front">'
            f'<div class="fc-hint">cliquer pour répondre</div>'
            f'<div class="fc-q">{q}</div>'
            f'</div>'
            f'<div class="flashcard-back">'
            f'<div class="fc-hint">réponse</div>'
            f'<div class="fc-r">{md_to_html_inline(r)}</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
    return f'<div class="flashcards-wrap">{items}</div>'


def md_to_html_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text


def md_to_html(md):
    lines = md.splitlines()
    html = []
    i = 0
    in_table = False
    in_pre = False
    in_ul = False
    in_ol = False
    table_lines = []

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith("```"):
            if not in_pre:
                lang = line.strip()[3:].strip()
                html.append(f'<pre><code class="language-{lang}">')
                in_pre = True
            else:
                html.append('</code></pre>')
                in_pre = False
            i += 1
            continue

        if in_pre:
            html.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
            continue

        # Custom callouts :::type ... :::
        m = re.match(r'^:::([\w-]+)\s*(.*)', line)
        if m:
            block_type = m.group(1)
            first_line = m.group(2)
            # Check for SVG mindmap (inline)
            if block_type == "mindmap":
                svg_lines = [first_line]
                i += 1
                while i < len(lines) and lines[i].strip() != ":::":
                    svg_lines.append(lines[i])
                    i += 1
                html.append(f'<div class="diagram-wrap">{"".join(svg_lines)}</div>')
            elif block_type == "mermaid":
                mmd_lines = [first_line]
                i += 1
                while i < len(lines) and lines[i].strip() != ":::":
                    mmd_lines.append(lines[i])
                    i += 1
                mmd_content = '\n'.join(mmd_lines)
                html.append(f'<div class="mermaid">{mmd_content}\n</div>')
            elif block_type == "flashcards":
                fc_lines = [first_line]
                i += 1
                while i < len(lines) and lines[i].strip() != ":::":
                    fc_lines.append(lines[i])
                    i += 1
                html.append(parse_flashcards('\n'.join(fc_lines)))
            else:
                block_lines = [first_line]
                i += 1
                while i < len(lines) and lines[i].strip() != ":::":
                    block_lines.append(lines[i])
                    i += 1
                html.append(parse_callout(block_type, '\n'.join(block_lines)))
            i += 1
            continue

        # Headings
        if line.startswith("#### "):
            html.append(f'<h4>{md_to_html_inline(line[5:])}</h4>')
            i += 1
            continue
        if line.startswith("### "):
            slug = re.sub(r'[^a-z0-9]+', '-', line[4:].lower()).strip('-')
            html.append(f'<h3 id="{slug}">{md_to_html_inline(line[4:])}</h3>')
            i += 1
            continue
        if line.startswith("## "):
            slug = re.sub(r'[^a-z0-9]+', '-', line[3:].lower()).strip('-')
            html.append(f'<h2 id="{slug}">{md_to_html_inline(line[3:])}</h2>')
            i += 1
            continue
        if line.startswith("# "):
            slug = re.sub(r'[^a-z0-9]+', '-', line[2:].lower()).strip('-')
            html.append(f'<h1 id="{slug}">{md_to_html_inline(line[2:])}</h1>')
            i += 1
            continue

        # Tables
        if line.strip().startswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            # Peek ahead
            if i >= len(lines) or not lines[i].strip().startswith("|"):
                # Render table
                rows = [r for r in table_lines if not re.match(r'^\s*\|[-| :]+\|\s*$', r)]
                t = '<table>'
                for ri, row in enumerate(rows):
                    cells = [c.strip() for c in row.strip().strip('|').split('|')]
                    tag = 'th' if ri == 0 else 'td'
                    t += '<tr>' + ''.join(f'<{tag}>{md_to_html_inline(c)}</{tag}>' for c in cells) + '</tr>'
                t += '</table>'
                html.append(t)
                in_table = False
                table_lines = []
            continue

        # Horizontal rule
        if re.match(r'^---+$', line.strip()):
            html.append('<hr style="border:none;border-top:1px solid var(--border);margin:2rem 0;">')
            i += 1
            continue

        # Unordered list
        if line.startswith("- ") or line.startswith("* "):
            if not in_ul:
                html.append('<ul style="padding-left:1.5rem;margin:0.8rem 0;">')
                in_ul = True
            html.append(f'<li>{md_to_html_inline(line[2:])}</li>')
            i += 1
            if i >= len(lines) or (not lines[i].startswith("- ") and not lines[i].startswith("* ")):
                html.append('</ul>')
                in_ul = False
            continue

        # Ordered list
        m = re.match(r'^(\d+)\. (.*)', line)
        if m:
            if not in_ol:
                html.append('<ol style="padding-left:1.5rem;margin:0.8rem 0;">')
                in_ol = True
            html.append(f'<li>{md_to_html_inline(m.group(2))}</li>')
            i += 1
            if i >= len(lines) or not re.match(r'^\d+\. ', lines[i]):
                html.append('</ol>')
                in_ol = False
            continue

        # Blank line
        if line.strip() == "":
            i += 1
            continue

        # Paragraph
        html.append(f'<p>{md_to_html_inline(line)}</p>')
        i += 1

    return '\n'.join(html)


def build_toc(md):
    toc = []
    for line in md.splitlines():
        if line.startswith("## "):
            title = line[3:]
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            toc.append((2, title, slug))
        elif line.startswith("### "):
            title = line[4:]
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            toc.append((3, title, slug))
    if not toc:
        return ""
    html = ['<details class="toc"><summary>Sommaire</summary><ol>']
    i = 0
    while i < len(toc):
        level, title, slug = toc[i]
        if level == 2:
            # Collect subsections
            subs = []
            j = i + 1
            while j < len(toc) and toc[j][0] == 3:
                subs.append(toc[j])
                j += 1
            if subs:
                html.append(f'<li><details><summary><a href="#{slug}">{title}</a></summary><ul>')
                for _, st, ss in subs:
                    html.append(f'<li><a href="#{ss}">{st}</a></li>')
                html.append('</ul></details></li>')
            else:
                html.append(f'<li><a href="#{slug}">{title}</a></li>')
            i = j
        else:
            i += 1
    html.append('</ol></details>')
    return '\n'.join(html)


def split_into_sections(html_body):
    """Split HTML body into sections at each <h2> tag."""
    parts = re.split(r'(?=<h2 )', html_body)
    sections = []
    intro = parts[0] if parts else ""
    for part in parts[1:]:
        sections.append(part)
    return intro, sections


def build_toc_with_links(md, section_index):
    """Build TOC with JS onclick navigation."""
    toc_items = []
    sec_i = 0
    for line in md.splitlines():
        if line.startswith("## "):
            title = line[3:]
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            toc_items.append((sec_i, title, slug, []))
            sec_i += 1
        elif line.startswith("### ") and toc_items:
            title = line[4:]
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            toc_items[-1][3].append((title, slug))

    html = ['<details class="toc"><summary>Sommaire</summary><ol>']
    for idx, title, slug, subs in toc_items:
        active = 'toc-active' if idx == 0 else ''
        if subs:
            html.append(f'<li><a class="toc-link {active}" href="#" onclick="showSection({idx});return false;">{title}</a><ul>')
            for st, ss in subs:
                html.append(f'<li><a href="#{ss}" onclick="showSection({idx});return false;">{st}</a></li>')
            html.append('</ul></li>')
        else:
            html.append(f'<li><a class="toc-link {active}" href="#" onclick="showSection({idx});return false;">{title}</a></li>')
    html.append('</ol></details>')
    return '\n'.join(html)


def wrap_sections(intro, sections):
    """Wrap each section in a .section div with prev/next navigation."""
    total = len(sections)
    html = [intro]
    for i, sec in enumerate(sections):
        prev_dis = 'disabled' if i == 0 else ''
        next_dis = 'disabled' if i == total - 1 else ''
        prev_btn = f'<button class="nav-btn btn-prev" onclick="showSection({i-1})" {prev_dis}>← Précédent</button>'
        next_btn = f'<button class="nav-btn btn-next" onclick="showSection({i+1})" {next_dis}>Suivant →</button>'
        progress = f'<span class="nav-progress">{i+1} / {total}</span>'
        nav = f'<div class="section-nav">{prev_btn}{progress}{next_btn}</div>'
        active = 'active' if i == 0 else ''
        html.append(f'<div class="section {active}" data-index="{i}">{sec}{nav}</div>')
    return '\n'.join(html)


def main():
    md_files = sorted(glob.glob("cours/*.md"))
    if not md_files:
        print("Aucun fichier markdown trouvé dans cours/")
        return

    full_md = ""
    for f in md_files:
        with open(f, encoding="utf-8") as fh:
            full_md += fh.read() + "\n\n"

    toc = build_toc_with_links(full_md, 0)
    body = md_to_html(full_md)
    intro, sections = split_into_sections(body)
    wrapped = wrap_sections(intro, sections)

    # Add toc-active style
    toc_style = '<style>.toc-active { font-weight: 700; color: var(--aqua) !important; }</style>'

    output = HTML_HEADER + toc_style + toc + wrapped + HTML_FOOTER
    with open("index.html", "w", encoding="utf-8") as fh:
        fh.write(output)
    print(f"index.html généré ({len(output)} caractères, {len(md_files)} fichier(s) source)")


if __name__ == "__main__":
    main()
