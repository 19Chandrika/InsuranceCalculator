from html import escape
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PROJECT_REPORT.md"
OUTPUT = ROOT / "PROJECT_REPORT.html"


def inline(text):
    text = escape(text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def flush_paragraph(parts, out):
    if parts:
        out.append(f"<p>{inline(' '.join(parts))}</p>")
        parts.clear()


def flush_list(items, out):
    if items:
        out.append("<ul>")
        for item in items:
            out.append(f"<li>{inline(item)}</li>")
        out.append("</ul>")
        items.clear()


def flush_table(rows, out):
    if not rows:
        return

    out.append("<table>")
    header = rows[0]
    out.append("<thead><tr>")
    for cell in header:
        out.append(f"<th>{inline(cell)}</th>")
    out.append("</tr></thead>")

    out.append("<tbody>")
    for row in rows[1:]:
        out.append("<tr>")
        for cell in row:
            out.append(f"<td>{inline(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    rows.clear()


def markdown_to_html(markdown):
    out = []
    paragraph = []
    list_items = []
    table_rows = []
    in_code = False

    for raw in markdown.splitlines():
        line = raw.rstrip()

        if line.startswith("```"):
            flush_paragraph(paragraph, out)
            flush_list(list_items, out)
            flush_table(table_rows, out)
            in_code = not in_code
            continue

        if in_code:
            continue

        if not line:
            flush_paragraph(paragraph, out)
            flush_list(list_items, out)
            flush_table(table_rows, out)
            continue

        image_match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if image_match:
            flush_paragraph(paragraph, out)
            flush_list(list_items, out)
            flush_table(table_rows, out)
            alt, src = image_match.groups()
            png_src = src.replace(".svg", ".svg.png")
            out.append(f'<figure><img src="{escape(png_src)}" alt="{escape(alt)}"><figcaption>{escape(alt)}</figcaption></figure>')
            continue

        if line.startswith("#"):
            flush_paragraph(paragraph, out)
            flush_list(list_items, out)
            flush_table(table_rows, out)
            level = len(line) - len(line.lstrip("#"))
            text = line[level:].strip()
            out.append(f"<h{level}>{inline(text)}</h{level}>")
            continue

        if line.startswith("- "):
            flush_paragraph(paragraph, out)
            flush_table(table_rows, out)
            list_items.append(line[2:].strip())
            continue

        if line.startswith("|") and line.endswith("|"):
            flush_paragraph(paragraph, out)
            flush_list(list_items, out)
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if all(set(cell) <= {"-", " "} for cell in cells):
                continue
            table_rows.append(cells)
            continue

        flush_list(list_items, out)
        flush_table(table_rows, out)
        paragraph.append(line.strip())

    flush_paragraph(paragraph, out)
    flush_list(list_items, out)
    flush_table(table_rows, out)
    return "\n".join(out)


body = markdown_to_html(SOURCE.read_text(encoding="utf-8"))

html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Insurance Premium Calculator Project Report</title>
  <style>
    @page {{ margin: 0.65in; }}
    body {{
      color: #0f172a;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 11.5pt;
      line-height: 1.55;
      margin: 0;
    }}
    h1 {{
      color: #0f766e;
      font-size: 26pt;
      margin: 0 0 18px;
      text-align: center;
    }}
    h2 {{
      border-bottom: 2px solid #99f6e4;
      color: #0f766e;
      font-size: 18pt;
      margin: 28px 0 10px;
      padding-bottom: 4px;
    }}
    h3 {{
      color: #134e4a;
      font-size: 14pt;
      margin: 18px 0 8px;
    }}
    p {{ margin: 8px 0; }}
    ul {{ margin: 7px 0 12px 22px; padding: 0; }}
    li {{ margin: 4px 0; }}
    code {{
      background: #f1f5f9;
      border-radius: 4px;
      color: #0f172a;
      font-family: Menlo, Consolas, monospace;
      font-size: 10pt;
      padding: 1px 4px;
    }}
    table {{
      border-collapse: collapse;
      margin: 12px 0;
      width: 100%;
    }}
    th, td {{
      border: 1px solid #cbd5e1;
      padding: 7px;
      text-align: left;
      vertical-align: top;
    }}
    th {{ background: #ecfdf5; color: #134e4a; }}
    figure {{
      break-inside: avoid;
      margin: 14px 0 24px;
      text-align: center;
    }}
    img {{
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      max-height: 8.8in;
      max-width: 100%;
    }}
    figcaption {{
      color: #475569;
      font-size: 10pt;
      margin-top: 6px;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""

OUTPUT.write_text(html, encoding="utf-8")
print(OUTPUT)
