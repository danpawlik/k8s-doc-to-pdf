#!/usr/local/env python3

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
.sections, #editPageButton, #docsToc, #feedback, #feedback--prompt, #what-s-next
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
    for site in sites:
        name = site.rsplit('/',2)[1]
        print(name)
        filename = "%s.pdf" % name
        HTML(url=site).write_pdf(filename, stylesheets=[CSS(string=cssStr)])


if __name__ == '__main__':
    sites = get_sites()
    generate_site(sites)
