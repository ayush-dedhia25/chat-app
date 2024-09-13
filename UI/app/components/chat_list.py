from turtle import width
from app.components.chat_list_item import ChatListItem
import flet as ft


class ChatList(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        super().__init__()

        header = ft.Row(
            controls=[
                ft.Text(value="Chats", weight=ft.FontWeight.BOLD, size=20, expand=True),
                ft.IconButton(
                    content=ft.Image(
                        src="assets/icons/square-pen.svg",
                        color="#CBD5E1",
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(8),
                        shape=ft.RoundedRectangleBorder(radius=6),
                    ),
                    width=34,
                    height=34,
                ),
                ft.IconButton(
                    content=ft.Image(
                        src="assets/icons/list-filter.svg",
                        color="#CBD5E1",
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(8),
                        shape=ft.RoundedRectangleBorder(radius=6),
                    ),
                    width=34,
                    height=34,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        )

        search_bar = ft.Container(
            bgcolor="#475569",
            padding=ft.padding.symmetric(horizontal=12),
            border_radius=6,
            border=ft.Border(bottom=ft.BorderSide(1, "white")),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        src="assets/icons/search.svg",
                        color="#CBD5E1",
                        fit=ft.ImageFit.CONTAIN,
                        width=16,
                    ),
                    ft.TextField(
                        text_size=14,
                        hint_text="Search",
                        cursor_color="white",
                        border_color="transparent",
                        content_padding=ft.padding.symmetric(vertical=12),
                        dense=True,
                        max_lines=1,
                        expand=True,
                    ),
                ],
            ),
        )

        chat_list = ft.ListView(
            expand=True,
            spacing=4,
            controls=[
                ChatListItem(page),
                ChatListItem(page),
                ChatListItem(page),
                ChatListItem(page),
            ],
        )

        self.content = ft.Container(
            width=350,
            bgcolor="#334155",  # slate-700
            content=ft.Column(
                spacing=20,
                controls=[
                    header,  # Chat List header
                    search_bar,  # Search bar
                    chat_list,  # All the Chats
                ],
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=14),
        )
