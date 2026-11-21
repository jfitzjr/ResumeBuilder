# TeX uses curly braces so rip f strings
BEFORE_NAME = r"""\documentclass{article}
\usepackage{fontawesome5}
\usepackage[margin=1in]{geometry}
\usepackage[colorlinks=true, allcolors=black]{hyperref}
\usepackage{enumitem}
\pagestyle{empty}

\begin{document}

\vspace*{-3cm}
\begin{center}
    \Huge """

BETWEEN_LINKS = "}\ \ "
BEFORE_LINK = r"\href{https://"
BEFORE_EMAIL = r"\\ \href{mailto:"
BEFORE_PHONE = r"\href{tel:+"
BEFORE_CATEGORY_NAME = r"\noindent{\Large "
AFTER_CATEGORY_NAME = r"""}\\[-0.6em]
\vspace{2pt}
\noindent\rule{\textwidth}{1pt}"""


def getWebsites():
    while True:
        otherWebsite = input("Any other websites? (Leave blank if there are no more websites): ")
        if not otherWebsite:
            return
        yield otherWebsite

def getBulletPoints():
    while True:
        otherBulletPoints = input("Any bullet points to add? (Leave blank if there are no bullet points): ")
        if not otherBulletPoints:
            return
        yield otherBulletPoints

def getSubCategories():
    while True:
        subCategoryName = input("Any subcategories to add? (Leave blank if there are no more subcategories): ")
        if not subCategoryName:
            return
        
        subCategoryDate = input("What's the timeframe for this subcategory? (Leave blank if N/A): ")

        # call bullet points
        bulletsPoints = list(getBulletPoints())
        yield [subCategoryName, bulletsPoints, subCategoryDate]

def getCategories():
    while True:
        categoryName = input("Any categories to add? (Leave blank if there are no more categories): ")
        if not categoryName:
            return
        
        # call subcategories
        subCategories = list(getSubCategories())
        yield [categoryName, subCategories]

def buildTexFile(name, linkedin, github, email, phone, otherWebsites=[], categories=[]):
    global BEFORE_NAME
    global BEFORE_LINKEDIN
    
    resumeTex = BEFORE_NAME + name + '\n' + r"""\end{center}
"""
    resumeTex += BEFORE_LINK + linkedin + r"/}{\faLinkedin\ " + linkedin + BETWEEN_LINKS
    resumeTex += BEFORE_LINK + github + r"/}{\faGithub\ " + github + BETWEEN_LINKS

    for website in otherWebsites:
        resumeTex += BEFORE_LINK + website + r"/}{\faGlobe\ " + website + BETWEEN_LINKS

    resumeTex += BEFORE_EMAIL + email + r"}{\faEnvelope\ " + email + BETWEEN_LINKS
    resumeTex += BEFORE_PHONE + phone + r"}{\faPhone\ +" + phone + r"""} \\
        
"""

    for category in categories:
        resumeTex += BEFORE_CATEGORY_NAME + category[0] + AFTER_CATEGORY_NAME + '\n'

        for subCategory in category[1]:
            resumeTex += "\large " + subCategory[0]
            if subCategory[2]:
                resumeTex += " \hfill " + subCategory[2]

            if not subCategory[1]:
                resumeTex += " \\\\\n"
                continue
            
            resumeTex += "\n"
            resumeTex += r"\vspace{2pt}" + '\n' + r"\normalsize" + '\n' + r"\begin{itemize}[noitemsep, topsep=0pt, leftmargin=*]" + '\n'
            for bulletPoint in subCategory[1]:
                resumeTex += r"    \item " + bulletPoint + '\n'
            resumeTex += r"\end{itemize}" + '\n' + r"\vspace{2pt}"

        resumeTex += '\n\n' + r"\vspace{10pt}" + '\n'

    resumeTex = resumeTex + '\n' + r"\end{document}"
    print(resumeTex)

if __name__ == "__main__":
    name = input("What's your name?: ")
    linkedin = input("What's your LinkedIn link?: ")
    github = input("What's your Github link?: ")
    email = input("What's your Email?: ")
    phone = input("What's your Phone Number (Ex: 11234567890)?: ")

    otherWebsites = list(getWebsites())
    categories = list(getCategories())
    
    buildTexFile(name, linkedin, github, email, phone, otherWebsites, categories)