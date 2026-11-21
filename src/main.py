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

BEFORE_LINKEDIN = r"""\end{center}
\href{https://"""

BEFORE_GITHUB = r"""\href{https://"""

BEFORE_LINK = r"""\href{https://"""

BEFORE_EMAIL = r"""\\ \href{mailto:"""

BEFORE_PHONE = r"""\href{tel:+"""

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
        yield getBulletPoints

def getSubCategories():
    while True:
        otherSubCategories = input("Any subcategories to add? (Leave blank if there are no more subcategories): ")
        if not otherSubCategories:
            return
        
        # call bullet points
        otherSubCategories = list(getBulletPoints())
        yield otherSubCategories

def getCategories():
    while True:
        otherCategories = input("Any categories to add? (Leave blank if there are no more categories): ")
        if not otherCategories:
            return
        
        # call subcategories
        otherCategories = list(getSubCategories())
        yield otherCategories

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
    resumeTex += BEFORE_PHONE + phone + r"}{\faPhone\ +" + phone + "} \\"


    resumeTex = resumeTex + '\n' + r"\end{document}"
    print(resumeTex)

if __name__ == "__main__":
    name = input("What's your name?: ")
    linkedin = input("What's your LinkedIn link?: ")
    github = input("What's your Github link?: ")
    email = input("What's your Email?: ")
    phone = input("What's your Phone Number (Ex: 11234567890)?: ")
    print()

    otherWebsites = getWebsites()
    #categories = list(getCategories())

    buildTexFile(name, linkedin, github, email, phone, otherWebsites)