import flet as ft


class NotFoundView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.content = ft.Column(
            controls=[ft.Text("404 PAGE NOT FOUND")],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
