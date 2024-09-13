import flet as ft


class ChatListItem(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.bgcolor = ft.colors.TRANSPARENT
        self.padding = ft.padding.all(10)
        self.border_radius = 6

        self.on_hover = self.on_hover_handler
        self.on_click = self.handle_click

        self.content = ft.Row(
            spacing=15,
            controls=[
                ft.CircleAvatar(
                    foreground_image_src="https://images.jdmagicbox.com/quickquotes/images_main/peacock-feather-wallpaper-511202-2217218618-cit6o7yv.jpg",
                    width=40,
                    height=40,
                ),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        spacing=2,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Ayush Dedhia"),
                                    ft.Text("15:20", size=12),
                                ],
                            ),
                            ft.Text("Hey, what do you doing?"),
                        ],
                    ),
                ),
            ],
        )

    def on_hover_handler(self, e: ft.ControlEvent):
        if e.data == "true":
            self.bgcolor = "#1E293B"
        else:
            self.bgcolor = ft.colors.TRANSPARENT
        self.update()

    def handle_click(self, e: ft.ControlEvent):
        print("Chat item clicked!")
