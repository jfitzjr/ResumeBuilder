import flet as ft


def main(page: ft.Page):
    page.title = "ResumeBuilder"
    linkFields: list[ft.TextField] = []
    linkFieldColumn = ft.Column()
    #output_text = ft.Text()
    
    categoryFields: list[ft.TextField] = []
    categoryFieldColumn = ft.Column()

    
    

    #Functions
    def addLinkField(e):
        field = ft.TextField(label=f"Link {len(linkFields) + 1}", hint_text=f"example{len(linkFields) + 1}.com")
        linkFields.append(field)
        linkFieldColumn.controls.append(field)
        page.update()

    def removeLinkField(e):
        lastField = len(linkFields) - 1
        if lastField >= 0:
            linkFields.pop(lastField)
            linkFieldColumn.controls.pop(lastField)
        page.update()

    def addCategoryField(e):
        field = ft.TextField(label=f"Category {len(categoryFields) + 1}")

        #Make a separate list with the field container and the list of the subcontainer
        fieldContainer:list[ft.TextField] = []
        fieldContainer.append(field)

        columnContainer = ft.Column()
        columnContainer.controls.append(field)

        #Makes subcategory fields first
        subcategoryFields: list[ft.TextField] = []
        fieldContainer.append(subcategoryFields)

        subcategoryFieldColumn = ft.Column(controls=[
            ft.Row(subcategoryFields),
            ft.Row(
                controls=[
                    ft.Text("Add subcategory"),
                    ft.Button(content="+", on_click=addSubCategoryField),
                    ft.Button(content="-", on_click=removeCategoryField)
                ]
            )
        ])

        # Then append it to the column container
        columnContainer.controls.append(subcategoryFieldColumn)
        categoryFields.append(fieldContainer)
        categoryFieldColumn.controls.append(columnContainer)

        page.update()
    
    def addSubCategoryField(e):
        TODO
        
    def removeCategoryField(e):
        TODO

    def removeSubCategoryField(e):
        TODO

    def addBulletPointField(e):
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
    addLinkRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Add/Remove link"),
                ft.Button(content="+", on_click=addLinkField),
                ft.Button(content="-", on_click=removeLinkField)
            ]
        )
    addCategoryRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Add category"),
                ft.Button(content="+", on_click=addCategoryField),
                ft.Button(content="-", on_click=removeCategoryField)
            ]
        )
    
    addBulletPointRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Add category"),
                ft.Button(content="+", on_click=addBulletPointField)
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
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                linkFieldColumn
            ]
        ),

        addLinkRow,

        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                categoryFieldColumn
            ]
        ),

        addCategoryRow,
        latexCompileRow
    )


if __name__ == "__main__":
    ft.run(main)
