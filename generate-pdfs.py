#!/usr/local/env python3

import glob
import os
import cssutils

from PyPDF2 import PdfFileMerger
from weasyprint import HTML, CSS

cssStr = """

#docsContent h1, #docsContent h2, #docsContent h3, #docsContent h4,
#docsContent h5, #docsContent h6 {
    line-height: 0.4 !important;
    font-weight: 500 !important;
    margin-bottom: 10px !important;
    padding-bottom: 0 !important;
}

#docsContent pre {
    margin-top: 0px !important;
    margin-bottom: 5px !important;
    padding: 10px !important;
}

@page {
  size: Letter !important;
  margin: 0.5cm !important;
}

#docsContent h1, #docsContent h2 {
    border-bottom-style: none !important;
}

#pre-footer, footer, header, .feedback--prompt, .feedback--yes, .feedback--no,
#hero, #user-journeys-toc, #content .track, .what-s-next,
.docssectionheaders:last-child, .docssectionheaders:last-of-type,
.sections, #editPageButton, #docsToc, #feedback, #feedback--prompt
{
    display: none !important;
}
#docsContent {
    float: none !important;
    width: 100% !important;
}
#encyclopedia {
    padding-bottom: 0 !important;
}
"""


def get_sites():
    sites = []
    with open('./k8s-sites', 'r') as f:
        for line in f:
            sites.append(line)
    return sites


def generate_site(sites):
    section_order = []
    for site in sites:
        name = site.rsplit('/', 2)[1]
        filename = "%s.pdf" % name
        print("Generating %s" % name)
        HTML(url=site).write_pdf(filename, stylesheets=[CSS(string=cssStr)])
        section_order.append(name)
    return section_order


def get_pdf_files(section_order):
    pdf_files = []
    for f in section_order:
        name = "%s.pdf" % f
        if glob.glob(name):
            pdf_files.append(name)
    return pdf_files


def merge_files(pdf_files):
    merger = PdfFileMerger()
    for pdf in pdf_files:
        merger.append(open(pdf, 'rb'))

    with open('k8s-book.pdf', 'wb') as fout:
        merger.write(fout)


def css_validation():
    parsed_css = cssutils.parseString(cssStr)
    return parsed_css.valid


if __name__ == '__main__':
    sites = get_sites()

    if not css_validation():
        print("Your CSS is not valid!")

    section_order = generate_site(sites)
    pdf_files = get_pdf_files(section_order)
    merge_files(pdf_files)
