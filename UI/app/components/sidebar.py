from typing import Callable
import flet as ft


class Sidebar(ft.Container):
    def __init__(self, page: ft.Page, on_navigate: Callable[[str], None]):
        super().__init__()
        self.page = page
        self.on_navigate = on_navigate

        self.bgcolor = "#1E293B"  # slate-800
        self.padding = ft.padding.all(8)
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.create_nav_button("menu", "home:page"),
                self.create_nav_button("phone", "calls:page"),
                self.create_nav_button("circle-equal", "status:page"),
                self.create_nav_button("bot-message-square", "ask_AI:page"),
                self.create_nav_button("star", "starredMessages:page"),
                self.create_nav_button("archive", "archiveChats:page"),
                self.create_nav_button("settings", "settings:page"),
                self.create_nav_button("user-pen", "profile:page"),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.bottom_center,
                    content=ft.CircleAvatar(
                        foreground_image_src="https://images.jdmagicbox.com/quickquotes/images_main/peacock-feather-wallpaper-511202-2217218618-cit6o7yv.jpg",
                        width=26,
                        height=26,
                    ),
                ),
            ],
        )

    def create_nav_button(self, icon: str, route: str):
        return ft.IconButton(
            content=ft.Image(
                src=f"assets/icons/{icon}.svg",
                color="#CBD5E1",
                fit=ft.ImageFit.CONTAIN,
            ),
            style=ft.ButtonStyle(
                padding=ft.padding.all(8),
                shape=ft.RoundedRectangleBorder(radius=6),
            ),
            width=34,
            height=34,
            on_click=lambda e, route=route: self.on_navigate(route),
        )
