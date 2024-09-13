import flet as ft

from app.components.chat_view import ChatView
from app.components.chat_list import ChatList


class HomePage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.content = ft.Row(
            spacing=0,
            controls=[ChatList(page), ChatView(page)],
        )
