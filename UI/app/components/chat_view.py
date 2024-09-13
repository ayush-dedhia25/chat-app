import flet as ft

from app.ui.icon_button import MyIconButton


class ChatView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.expand = True
        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                self.render_header(),
                self.render_chats_section(),
                self.render_footer(),
            ],
        )

    def render_header(self):
        return ft.Container(
            bgcolor="#1F2937",  # gray-800
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            content=ft.Row(
                spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Row(
                            spacing=12,
                            controls=[
                                ft.CircleAvatar(
                                    foreground_image_src="https://images.jdmagicbox.com/quickquotes/images_main/peacock-feather-wallpaper-511202-2217218618-cit6o7yv.jpg",
                                    width=40,
                                    height=40,
                                ),
                                ft.Column(
                                    spacing=1,
                                    controls=[
                                        ft.Text(
                                            "Ayush Dedhia",
                                            color="white",
                                            weight=ft.FontWeight.W_600,
                                        ),
                                        ft.Text(
                                            "Last seen today at 8:25",
                                            color="white",
                                            size=12,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        bgcolor="#111827",  # gray-800
                        border_radius=6,
                        content=ft.Row(
                            spacing=0,
                            controls=[
                                ft.IconButton(
                                    content=ft.Image(
                                        src="assets/icons/video.svg",
                                        color="#CBD5E1",
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.all(10),
                                        shape=ft.RoundedRectangleBorder(radius=6),
                                    ),
                                    width=40,
                                    height=40,
                                ),
                                ft.IconButton(
                                    content=ft.Image(
                                        src="assets/icons/phone.svg",
                                        color="#CBD5E1",
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.all(12),
                                        shape=ft.RoundedRectangleBorder(radius=6),
                                    ),
                                    width=40,
                                    height=40,
                                ),
                            ],
                        ),
                    ),
                    ft.IconButton(
                        content=ft.Image(
                            src="assets/icons/search.svg",
                            color="#CBD5E1",
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        style=ft.ButtonStyle(
                            padding=ft.padding.all(12),
                            shape=ft.RoundedRectangleBorder(radius=6),
                        ),
                        width=40,
                        height=40,
                    ),
                ],
            ),
        )

    def render_chat_bubble(self, message: str, time: str, is_sender: bool = False):
        return ft.Row(
            alignment=(
                ft.MainAxisAlignment.END if is_sender else ft.MainAxisAlignment.START
            ),
            controls=[
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=8, vertical=6),
                    bgcolor=(
                        ft.colors.LIGHT_BLUE_ACCENT if is_sender else ft.colors.WHITE12
                    ),
                    border_radius=ft.border_radius.only(
                        top_left=5 if is_sender else 0,
                        top_right=0 if is_sender else 5,
                        bottom_left=5,
                        bottom_right=5,
                    ),
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                message,
                                color=(
                                    ft.colors.WHITE
                                    if is_sender
                                    else ft.colors.LIGHT_BLUE_ACCENT
                                ),
                            ),
                            ft.Container(
                                content=ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text(
                                            time,
                                            color=ft.colors.WHITE,
                                            size=12,
                                        ),
                                        ft.Image(
                                            src="assets/icons/check-check.svg",
                                            width=15,
                                            color=ft.colors.WHITE,
                                            visible=is_sender,
                                        ),
                                    ],
                                )
                            ),
                        ]
                    ),
                )
            ],
        )

    def render_chats_section(self):
        return ft.Container(
            expand=True,
            padding=ft.padding.symmetric(vertical=10, horizontal=10),
            content=ft.Column(
                spacing=4,
                expand=True,
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    self.render_chat_bubble("What are you guys doing?", "12:34"),
                    self.render_chat_bubble(
                        "Have you came back from the event?", "12:36", True
                    ),
                ],
            ),
        )

    def render_footer(self):
        self.text_message = ""
        footer = None

        def handle_text_change(e: ft.ControlEvent) -> None:
            self.text_message = e.control.value.strip()
            send_button.visible = bool(self.text_message)
            if footer is not None:
                footer.update()

        message_field = ft.TextField(
            expand=True,
            hint_text="Type a message",
            border_color="transparent",
            text_size=14,
            cursor_color="#CBD5E1",  # slate-300
            hint_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_400),
            content_padding=0,
            height=38,
            color="#CBD5E1",  # slate-300
            on_change=handle_text_change,
        )

        send_button = MyIconButton(
            url="icons/send-horizontal.svg",
            size=36,
            color="#CBD5E1",
            visible=False,
        )

        footer = ft.Container(
            bgcolor="#1F2937",
            padding=ft.padding.symmetric(vertical=6, horizontal=10),
            content=ft.Row(
                controls=[
                    MyIconButton(url="icons/smile-plus.svg", size=36, color="#CBD5E1"),
                    message_field,
                    send_button,
                ]
            ),
        )

        return footer
