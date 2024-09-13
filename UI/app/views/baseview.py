import flet as ft


class BaseView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
