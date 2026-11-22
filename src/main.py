from pathlib import Path
import flet as ft

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

BETWEEN_LINKS = "}\\ \\ "
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

        bulletsPoints = list(getBulletPoints())
        yield [subCategoryName, bulletsPoints, subCategoryDate]

def getCategories():
    while True:
        categoryName = input("Any categories to add? (Leave blank if there are no more categories): ")
        if not categoryName:
            return

        subCategories = list(getSubCategories())
        yield [categoryName, subCategories]

def buildTexFile(name, linkedin="", github="", email="", phone="", otherWebsites=None, categories=None):
    otherWebsites = otherWebsites or []
    categories = categories or []
    
    resumeTex = BEFORE_NAME + name + '\n' + r"""\end{center}
"""
    if linkedin:
        resumeTex += BEFORE_LINK + linkedin + r"/}{\faLinkedin\ " + linkedin + BETWEEN_LINKS
    if github:
        resumeTex += BEFORE_LINK + github + r"/}{\faGithub\ " + github + BETWEEN_LINKS

    for website in otherWebsites:
        resumeTex += BEFORE_LINK + website + r"/}{\faGlobe\ " + website + BETWEEN_LINKS

    if email:
        resumeTex += BEFORE_EMAIL + email + r"}{\faEnvelope\ " + email + BETWEEN_LINKS
    if phone:
        resumeTex += BEFORE_PHONE + phone + r"}{\faPhone\ " + phone
    resumeTex += r"""} \\
        
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
    
    return resumeTex

async def get_downloads_dir() -> Path:
    storage_paths = ft.StoragePaths()
    downloads_str = None

    try:
        downloads_str = await storage_paths.get_downloads_directory()
    except Exception:
        downloads_str = None

    downloads_dir = Path(downloads_str) if downloads_str else (Path.home() / "Downloads")
    downloads_dir.mkdir(parents=True, exist_ok=True)
    return downloads_dir

def main(page: ft.Page):
    page.title = "ResumeBuilder"
    page.scroll = ft.ScrollMode.AUTO
    output_text = ft.Text()

    linkFields: list[ft.TextField] = []
    linkFieldColumn = ft.Column()
    categoryEntries: list[dict] = []
    categoryFieldColumn = ft.Column()
    
    def collect_categories():
        collected = []
        for cat in categoryEntries:
            cat_name = (cat["field"].value or "").strip()
            if not cat_name:
                continue

            sub_list = []
            for sub in cat["subcategories"]:
                sub_name = (sub["name_field"].value or "").strip()
                sub_date = (sub["date_field"].value or "").strip()
                bullets = [
                    (b.value or "").strip()
                    for b in sub["bullets"]
                    if (b.value or "").strip()
                ]

                if not sub_name and not sub_date and not bullets:
                    continue

                sub_list.append([sub_name, bullets, sub_date])

            collected.append([cat_name, sub_list])
        return collected

    def build_current_tex() -> str:
        if not nameField.value:
            output_text.value = "Please add a name."
            page.update()
            return ""

        return buildTexFile(
            nameField.value or "",
            linkedinField.value or "",
            githubField.value or "",
            emailField.value or "",
            phoneNumberField.value or "",
            [(f.value or "").strip() for f in linkFields if (f.value or "").strip()],
            collect_categories(),
        )

    #Functions
    def addLinkField(e):
        field = ft.TextField(label=f"Link {len(linkFields) + 1}")
        linkFields.append(field)
        linkFieldColumn.controls.append(field)
        page.update()

    def removeLinkField(e):
        if len(linkFields) <= 0:
            return
        lastField = len(linkFields) - 1
        linkFields.pop(lastField)
        linkFieldColumn.controls.pop(lastField)
        page.update()

    def addCategoryField(e):
        cat_idx = len(categoryEntries) + 1
        field = ft.TextField(label=f"Category {cat_idx}")
        subCategoryFieldsColumn = ft.Column(controls=[])

        cat_entry = {
            "field": field,
            "subcategories": [],
            "container": None,
        }

        def addSubCategoryField(e):
            sub_idx = len(cat_entry["subcategories"]) + 1
            subField = ft.TextField(label=f"Subcategory {sub_idx}")
            subDateField = ft.TextField(
                label=f"Timeframe {sub_idx} (Optional)",
                hint_text="Jan 2024 - Present",
            )
            bulletFields: list[ft.TextField] = []
            bulletFieldsColumn = ft.Column(controls=[])

            sub_entry = {
                "name_field": subField,
                "date_field": subDateField,
                "bullets": bulletFields,
                "container": None,
            }

            def addBulletField(e):
                bulletField = ft.TextField(label=f"Bullet {len(bulletFields) + 1}")
                bulletFields.append(bulletField)
                bulletFieldsColumn.controls.append(bulletField)
                page.update()

            def removeBulletField(e):
                if not bulletFields:
                    return
                bulletFields.pop()
                bulletFieldsColumn.controls.pop()
                page.update()

            subContainer = ft.Column(
                controls=[
                    subField,
                    subDateField,
                    ft.Row(
                        controls=[
                            ft.Text("      Add bullet"),
                            ft.Button(content="+", on_click=addBulletField),
                            ft.Button(content="-", on_click=removeBulletField),
                        ]
                    ),
                    bulletFieldsColumn,
                ]
            )
            sub_entry["container"] = subContainer

            cat_entry["subcategories"].append(sub_entry)
            subCategoryFieldsColumn.controls.append(subContainer)
            page.update()

        def removeSubCategoryField(e):
            if not cat_entry["subcategories"]:
                return
            cat_entry["subcategories"].pop()
            subCategoryFieldsColumn.controls.pop()
            page.update()

        subcategoryFieldColumn = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("   Add subcategory"),
                        ft.Button(content="+", on_click=addSubCategoryField),
                        ft.Button(content="-", on_click=removeSubCategoryField),
                    ]
                ),
                subCategoryFieldsColumn,
            ]
        )

        columnContainer = ft.Column(
            controls=[
                field,
                subcategoryFieldColumn,
            ]
        )
        cat_entry["container"] = columnContainer

        categoryEntries.append(cat_entry)
        categoryFieldColumn.controls.append(columnContainer)
        page.update()

    def removeCategoryField(e):
        if not categoryEntries:
            return
        categoryEntries.pop()
        categoryFieldColumn.controls.pop()
        page.update()

    async def handleBuild(e):
        resumeTex = build_current_tex()
        if not resumeTex:
            return

        save_path = await ft.FilePicker().save_file(file_name="resume.tex")
        if not save_path:
            output_text.value = "Save cancelled."
            page.update()
            return

        target_path = Path(save_path)
        if target_path.suffix.lower() != ".tex":
            target_path = target_path.with_suffix(".tex")

        target_path.write_text(resumeTex, encoding="utf-8")
        output_text.value = f"Saved to {target_path}"
        page.update()

    async def handleCopy(e):
        resumeTex = build_current_tex()
        if not resumeTex:
            return

        await ft.Clipboard().set(resumeTex)
        output_text.value = "Copied LaTeX to clipboard!"
        page.update()

    #Text Fields
    nameField = ft.TextField(label="Name", hint_text="Jane Doe")
    linkedinField = ft.TextField(label="LinkedIn (Optional)", hint_text="linkedin.com/in/barackobama")
    githubField = ft.TextField(label="Github (Optional)", hint_text="github.com/PirateSoftware")
    emailField = ft.TextField(label="Email (Optional)", hint_text="example@gmail.com")
    phoneNumberField = ft.TextField(label="Phone Number (Optional)", hint_text="0123456789")
    
    initialFieldColumn = ft.Column(
        controls=[
            nameField,
            linkedinField,
            githubField,
            emailField,
            phoneNumberField
        ]
    )

    #Additional text fields & labels
    linkButtonRow = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Text("Add/Remove link"),
            ft.Button(content="+", on_click=addLinkField),
            ft.Button(content="-", on_click=removeLinkField)
        ]
    )

    linkRow = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[linkFieldColumn]
    )

    categoryButtonRow = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Text("Add category"),
            ft.Button(content="+", on_click=addCategoryField),
            ft.Button(content="-", on_click=removeCategoryField)
        ]
    )

    categoryRow = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[categoryFieldColumn]
    )

    latexCompileRow = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Button(content="Create resume.tex", on_click=handleBuild),
            ft.Button(content="Copy resume.tex", on_click=handleCopy)
        ]
    )

    ROOT_DIR = Path(__file__).resolve().parents[1]
    IMAGE_PATH = ROOT_DIR / "assets" / "sample.png"
    img = ft.Image(
        src=str(IMAGE_PATH),
        width=700,
        height=250,
        fit="contain",
        border_radius=12,
    )

    right_image_container = ft.Container(
        content=img,
        alignment=ft.Alignment.TOP_RIGHT,
    )

    form_column = ft.Column(
        expand=True,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[initialFieldColumn],
            ),
            linkButtonRow,
            linkRow,
            categoryButtonRow,
            categoryRow,
            latexCompileRow,
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[output_text],
            ),
        ],
    )

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                form_column,
                right_image_container,
            ],
        )
    )

if __name__ == "__main__":
    ft.run(main)