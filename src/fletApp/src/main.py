import flet as ft


def main(page: ft.Page):
    page.title = "ResumeBuilder"
    linkFields: list[ft.TextField] = []
    linkFieldColumn = ft.Column()
    output_text = ft.Text()
    
    #Functions
    def addLinkField(e):
        field = ft.TextField(label=f"Link {len(linkFields) + 1}")
        linkFields.append(field)
        linkFieldColumn.controls.append(field)
        page.update()

    def removeLinkField(e):
        lastField = len(linkFields) - 1
        linkFields.pop(lastField)
        linkFieldColumn.controls.pop(lastField)
        page.update()

    def addCategory():
        TODO
    def addSubCategory():
        TODO
    
    def addBulletPoint():
        TODO

    #Text Fields
    nameField = ft.TextField(label="Name", hint_text="Jane Doe")
    linkedinField = ft.TextField(label="LinkedIn (Optional)")
    emailField = ft.TextField(label="Email (Optional)", hint_text="example@gmail.com")
    phoneNumberField = ft.TextField(label="Phone Number (Optional)", hint_text="0123456789")
    
    initialFieldColumn = ft.Column(
        controls=[
            nameField,
            linkedinField,
            emailField,
            phoneNumberField
        ]
        )

    #Additional text fields & labels
    linkRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                linkFieldColumn,
                ft.Text("Add/Remove link"),
                ft.Button(content="+", on_click=addLinkField),
                ft.Button(content="-", on_click=removeLinkField)
            ]
        )
    categoryRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Add category"),
                ft.Button(content="+", on_click=addCategory)
            ]
        )
    subcategoryRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Add category"),
                ft.Button(content="+", on_click=addSubCategory)
            ]
        )
    bulletPointRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Add category"),
                ft.Button(content="+", on_click=addBulletPoint)
            ]
        )


    latexCompileRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Button(content="Compile to LaTeX")
            ]
        )

    #page.floating_action_button = ft.FloatingActionButton(
    #    icon=ft.Icons.ADD, key="increment", on_click=increment_click
    #)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                initialFieldColumn,
                
            ]
        ),
        linkRow,
        categoryRow,
        latexCompileRow
    )


if __name__ == "__main__":
    ft.run(main)
