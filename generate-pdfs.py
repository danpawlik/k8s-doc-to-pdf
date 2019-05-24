#!/usr/local/env python3

import glob
import os

from PyPDF2 import PdfFileMerger
from weasyprint import HTML, CSS

cssStr = """
@page {
  size: Letter;
  margin: 0.8cm;
}

@font-size 10;

#pre-footer, footer, header, .feedback--prompt, .feedback--yes, .feedback--no,
#hero, #user-journeys-toc, #content .track,
.docssectionheaders:last-child, .docssectionheaders:last-of-type,
.sections, #editPageButton, #docsToc, #feedback, #feedback--prompt
{
    display: none !important;
}

.feedback
{
    display: none !important;
}

h1 {
    margin:0;
    font-size 10;
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


if __name__ == '__main__':
    sites = get_sites()
    section_order = generate_site(sites)
    pdf_files = get_pdf_files(section_order)
    merge_files(pdf_files)
