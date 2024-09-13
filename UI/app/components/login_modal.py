import flet as ft

from app.util import useState


class LoginModal(ft.AlertDialog):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page

        # UI States
        (self.email, setEmail) = useState("", self)
        (self.password, setPassword) = useState("", self)

        self.content_padding = ft.padding.symmetric(vertical=20, horizontal=24)
        self.shape = ft.RoundedRectangleBorder(radius=14)
        self.modal = True

        self.content = ft.Container(
            width=300,
            content=ft.Column(
                spacing=20,
                tight=True,
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "EMAIL", size=12, style=ft.TextStyle(letter_spacing=1.5)
                            ),
                            ft.TextField(
                                hint_text="E.g. johndoe@example.com",
                                border_color=ft.colors.WHITE24,
                                text_size=14,
                                hint_style=ft.TextStyle(weight=ft.FontWeight.W_400),
                                dense=True,
                                content_padding=ft.padding.symmetric(
                                    vertical=14, horizontal=12
                                ),
                                border_radius=8,
                                focused_border_color="#7C3AED",
                                on_change=lambda e: setEmail(e.control.value),
                            ),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "PASSWORD",
                                size=12,
                                style=ft.TextStyle(letter_spacing=1.5),
                            ),
                            ft.TextField(
                                hint_text="Enter your password",
                                border_color=ft.colors.WHITE24,
                                text_size=14,
                                hint_style=ft.TextStyle(weight=ft.FontWeight.W_400),
                                dense=True,
                                content_padding=ft.padding.symmetric(
                                    vertical=16, horizontal=14
                                ),
                                border_radius=8,
                                password=True,
                                can_reveal_password=True,
                                focused_border_color="#7C3AED",
                                on_change=lambda e: setPassword(e.control.value),
                            ),
                        ]
                    ),
                ],
            ),
        )

        self.actions = [
            ft.TextButton(
                text="Cancel",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.padding.symmetric(vertical=18, horizontal=30),
                ),
                on_click=self.close_modal,
            ),
            ft.TextButton(
                text="Login",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    bgcolor="#6366F1",
                    padding=ft.padding.symmetric(vertical=18, horizontal=30),
                    color=ft.colors.WHITE,
                ),
                on_click=self.close_modal,
            ),
        ]

    def close_modal(self, e):
        self.open = False
        print(f"Email: {self.email()}, Password: {self.password()}")
        self.page.update()

    def open_modal(self):
        if self not in self.page.overlay:
            self.page.overlay.append(self)
        self.open = True
        self.page.update()
