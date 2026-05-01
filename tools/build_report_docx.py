from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import html
import struct


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "InsurancePremiumCalculatorReport.docx"

NS = (
    'xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'xmlns:o="urn:schemas-microsoft-com:office:office" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
    'xmlns:v="urn:schemas-microsoft-com:vml" '
    'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:w10="urn:schemas-microsoft-com:office:word" '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
    'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
    'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
    'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
    'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
    'mc:Ignorable="w14 wp14"'
)


def esc(text):
    return html.escape(str(text), quote=False)


def png_size(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", data[16:24])


def run(text, bold=False, italic=False, size=22):
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    props.append(f'<w:sz w:val="{size}"/>')
    return f"<w:r><w:rPr>{''.join(props)}</w:rPr><w:t>{esc(text)}</w:t></w:r>"


def para(text="", style=None, align=None, bold=False, size=22, spacing_after=140):
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    ppr.append(f'<w:spacing w:after="{spacing_after}" w:line="276" w:lineRule="auto"/>')
    return f"<w:p><w:pPr>{''.join(ppr)}</w:pPr>{run(text, bold=bold, size=size)}</w:p>"


def bullet(text):
    return para(f"- {text}", spacing_after=80)


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def table(headers, rows):
    xml = ['<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
           '<w:top w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>'
           '<w:left w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>'
           '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>'
           '<w:right w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>'
           '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
           '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
           '</w:tblBorders></w:tblPr>']
    all_rows = [headers] + rows
    for row_index, row in enumerate(all_rows):
        xml.append("<w:tr>")
        for cell in row:
            shade = '<w:shd w:fill="ECFDF5"/>' if row_index == 0 else ""
            xml.append(f'<w:tc><w:tcPr><w:tcW w:w="3000" w:type="dxa"/>{shade}</w:tcPr>')
            xml.append(para(cell, bold=row_index == 0, spacing_after=0))
            xml.append("</w:tc>")
        xml.append("</w:tr>")
    xml.append("</w:tbl>")
    return "".join(xml)


def image_paragraph(rid, name, width_px, height_px):
    max_width = 6.4
    max_height = 7.2
    width_in = max_width
    height_in = width_in * height_px / width_px
    if height_in > max_height:
        height_in = max_height
        width_in = height_in * width_px / height_px
    cx = int(width_in * 914400)
    cy = int(height_in * 914400)
    return f"""
<w:p>
  <w:pPr><w:jc w:val="center"/><w:spacing w:after="180"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{rid.replace('rId', '')}" name="{esc(name)}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr><pic:cNvPr id="0" name="{esc(name)}"/><pic:cNvPicPr/></pic:nvPicPr>
              <pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
              <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
"""


parts = []
parts.append(para("Insurance Premium Calculator Project Report", style="Title", align="center", bold=True, size=40, spacing_after=360))
parts.append(para("Prepared for academic project documentation", align="center", size=24, spacing_after=360))

sections = [
    ("Abstract", [
        "The Insurance Premium Calculator is a web-based application developed to estimate insurance premiums for health, vehicle, life, and travel insurance. The system provides a simple interface where users select an insurance type, enter relevant details, and receive calculated premium information.",
        "The application calculates the base premium, Goods and Services Tax (GST), total payable amount, and Equal Monthly Installment (EMI) options for 3, 6, 9, and 12 months. The project uses Spring Boot for the backend REST API and HTML, CSS, and JavaScript for the frontend."
    ]),
    ("Introduction", [
        "Insurance helps individuals manage financial risk by providing protection against uncertain events such as illness, accidents, loss of life, vehicle damage, and travel-related issues. Customers often need an estimated premium before choosing a policy.",
        "This project provides a lightweight digital tool for estimating premium amounts. It supports health, vehicle, life, and travel insurance, with each category using different input values and calculation rules."
    ]),
    ("Literature Review", [
        "Insurance premium calculation systems are widely used in financial technology and insurance services. Commercial systems usually rely on actuarial models, risk assessment, claim history, demographic data, and regulatory requirements.",
        "For academic and prototype systems, rule-based premium calculation is commonly used because it is simple to understand, implement, and test. REST APIs are suitable for this project because the frontend submits user details and receives structured JSON results from the backend.",
        "Spring Boot simplifies Java web application development by providing REST controller support, dependency management, and application configuration. HTML, CSS, and JavaScript provide a browser-compatible frontend for user interaction."
    ]),
    ("Objectives", []),
]

for title, paragraphs in sections:
    parts.append(para(title, style="Heading1", bold=True, size=30))
    for item in paragraphs:
        parts.append(para(item))

for item in [
    "Develop a web-based insurance premium calculator.",
    "Support premium estimation for health, vehicle, life, and travel insurance.",
    "Dynamically display input fields based on the selected insurance category.",
    "Calculate premium amount using predefined business rules.",
    "Calculate GST at 18 percent and the total payable amount.",
    "Provide EMI options for 3, 6, 9, and 12 months.",
    "Implement backend processing using a Spring Boot REST API.",
    "Demonstrate client-server communication using JavaScript Fetch API and JSON."
]:
    parts.append(bullet(item))

parts.append(para("Methodology", style="Heading1", bold=True, size=30))
parts.append(para("The project follows a client-server methodology. The frontend collects user input, sends data to the backend API, and displays the response received from the server. The backend applies business rules and returns the premium calculation details."))

parts.append(para("Graphical Diagrams", style="Heading1", bold=True, size=30))

images = [
    ("System Architecture Diagram", ROOT / "docs/diagrams/system-architecture.png"),
    ("Use Case Diagram", ROOT / "docs/diagrams/use-case.png"),
    ("Data Flow Diagram", ROOT / "docs/diagrams/data-flow.png"),
    ("Activity Diagram", ROOT / "docs/diagrams/activity.png"),
    ("Sequence Diagram", ROOT / "docs/diagrams/sequence.png"),
]

rels = []
for idx, (caption, image_path) in enumerate(images, start=1):
    if idx > 1:
        parts.append(page_break())
    parts.append(para(caption, style="Heading2", bold=True, size=26, align="center"))
    w, h = png_size(image_path)
    rid = f"rId{idx}"
    parts.append(image_paragraph(rid, image_path.name, w, h))
    rels.append((rid, image_path))

parts.append(page_break())
parts.append(para("Requirement Analysis", style="Heading1", bold=True, size=30))
parts.append(para("The application allows users to select an insurance type, enter required information, submit the form, and view premium amount, GST, total amount, and EMI options."))

parts.append(para("System Design", style="Heading1", bold=True, size=30))
parts.append(para("The application is divided into two major parts: a static frontend page developed using HTML, CSS, and JavaScript, and a Spring Boot REST API developed using Java."))
parts.append(para("Frontend file: src/main/resources/static/index.html"))
parts.append(para("Backend controller: src/main/java/com/calculate/insurance/insurancecalculator/controller/InsuranceController.java"))

parts.append(para("Frontend Development", style="Heading1", bold=True, size=30))
parts.append(para("The frontend provides cards for health, vehicle, life, and travel insurance. When an insurance type is selected, JavaScript dynamically generates the required form fields. The form is submitted using the Fetch API to POST /api/calculate-premium."))

parts.append(para("Backend Development", style="Heading1", bold=True, size=30))
parts.append(para("The backend accepts a PremiumRequest object and returns a PremiumResponse object. The response contains insurance type, premium amount, GST amount, total amount, and EMI options."))

parts.append(para("Premium Calculation Logic", style="Heading1", bold=True, size=30))
for item in [
    "Health: Premium = Coverage Amount * 0.02 + Number of Members * 1000. If age is greater than 45, 2000 is added.",
    "Vehicle: Car premium = Vehicle Value * 0.03. Bike premium = Vehicle Value * 0.02. Vehicle Age * 500 is added.",
    "Life: Premium = Coverage Amount * 0.015 + Policy Term * 300. If age is greater than 40, 1500 is added.",
    "Travel: Premium = Trip Cost * 0.01 + Travel Days * 50 + Travellers * 300.",
    "GST = Premium * 0.18.",
    "Total Amount = Premium + GST.",
    "EMI options are calculated by dividing the total amount by 3, 6, 9, and 12 months."
]:
    parts.append(bullet(item))

parts.append(para("Expected Result", style="Heading1", bold=True, size=30))
parts.append(para("The expected result is a working web application that allows users to estimate insurance premiums quickly and clearly. Users can select an insurance type, enter details, calculate premium, and view the base premium, GST, total amount, and EMI options."))
parts.append(para("The result should be treated as an academic estimate rather than an official commercial insurance quote."))

parts.append(para("Work Plan", style="Heading1", bold=True, size=30))
parts.append(table(
    ["Phase", "Task", "Description"],
    [
        ["Phase 1", "Requirement Study", "Identify insurance types, input fields, and expected outputs."],
        ["Phase 2", "System Design", "Plan frontend page, backend API, request model, and response model."],
        ["Phase 3", "Frontend Development", "Create insurance selection UI, dynamic forms, icons, and result table."],
        ["Phase 4", "Backend Development", "Implement Spring Boot controller and premium calculation logic."],
        ["Phase 5", "Integration", "Connect frontend submission with backend API using Fetch API."],
        ["Phase 6", "Testing", "Test form inputs, API response, calculations, and application startup."],
        ["Phase 7", "Documentation", "Prepare project report with methodology, diagrams, and references."],
        ["Phase 8", "Future Enhancement", "Add database storage, login, validation, and advanced pricing models."],
    ]
))

parts.append(para("References", style="Heading1", bold=True, size=30))
for ref in [
    "Spring Boot Documentation: https://docs.spring.io/spring-boot/documentation.html",
    "Oracle JDK 17 Documentation: https://docs.oracle.com/en/java/javase/17/",
    "MDN Web Docs Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API",
    "MDN Web Docs HTML: https://developer.mozilla.org/en-US/docs/Web/HTML",
    "MDN Web Docs CSS: https://developer.mozilla.org/en-US/docs/Web/CSS",
    "Project source code: InsuranceCalculator Spring Boot application."
]:
    parts.append(bullet(ref))


document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document {NS}>
  <w:body>
    {''.join(parts)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="864" w:right="864" w:bottom="864" w:left="864" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/><w:color w:val="0F766E"/><w:sz w:val="40"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/><w:color w:val="0F766E"/><w:sz w:val="30"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/><w:color w:val="134E4A"/><w:sz w:val="26"/></w:rPr></w:style>
</w:styles>'''

rels_xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
for rid, image_path in rels:
    rels_xml.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{image_path.name}"/>')
rels_xml.append("</Relationships>")

content_types = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
                 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
                 '<Default Extension="xml" ContentType="application/xml"/>',
                 '<Default Extension="png" ContentType="image/png"/>',
                 '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>',
                 '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>',
                 '</Types>']

package_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

with ZipFile(OUT, "w", ZIP_DEFLATED) as docx:
    docx.writestr("[Content_Types].xml", "\n".join(content_types))
    docx.writestr("_rels/.rels", package_rels)
    docx.writestr("word/document.xml", document_xml)
    docx.writestr("word/styles.xml", styles_xml)
    docx.writestr("word/_rels/document.xml.rels", "\n".join(rels_xml))
    for _, image_path in rels:
        docx.write(image_path, f"word/media/{image_path.name}")

print(OUT)
