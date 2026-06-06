from weasyprint import HTML

PDF_STYLE = """
<style>

@page {
    size: A4;
    margin: 2cm 2.2cm;
}

body {
    font-family: Arial, sans-serif;
    font-size: 13px;
    line-height: 1.7;
    color: #1f2937;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

h1 {
    font-size: 32px;
    font-weight: 700;
    color: #111827;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
    border-bottom: 3px solid #2563eb;
    padding-bottom: 10px;
    margin-bottom: 18px;
}

h2 {
    font-size: 15px;
    font-weight: 700;
    color: #1e40af;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 24px;
    margin-bottom: 8px;
    border-bottom: 1px solid #dbeafe;
    padding-bottom: 5px;
}

h3 {
    font-size: 14px;
    font-weight: 600;
    color: #111827;
    margin-top: 12px;
    margin-bottom: 4px;
}

p {
    font-size: 13px;
    margin-bottom: 10px;
    color: #374151;
}

ul {
    margin-left: 18px;
    margin-bottom: 10px;
    padding-left: 4px;
}

li {
    font-size: 13px;
    margin-bottom: 6px;
    color: #374151;
}

strong {
    font-weight: 700;
    color: #111827;
}

blockquote {
    border-left: 4px solid #2563eb;
    padding: 8px 14px;
    margin: 12px 0;
    color: #4b5563;
    background: #f0f6ff;
}

</style>
"""


def generate_pdf(html_content):
    html_content = html_content.replace("&nbsp;", " ")

    html = f"""
    <html>
    <head>
        {PDF_STYLE}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    return HTML(string=html).write_pdf()