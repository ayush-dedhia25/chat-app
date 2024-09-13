import flet as ft
from typing import Callable
import flet_route as fr

NavigateFn = Callable[[str], None]


def LoginPageView(page: ft.Page, params: fr.Params, basket: fr.Basket):
    navigate: NavigateFn = lambda route: page.go(route)

    usernameRef = ft.Ref[ft.TextField]()
    usernameErrorRef = ft.Ref[ft.Text]()

    passwordRef = ft.Ref[ft.TextField]()
    passwordErrorRef = ft.Ref[ft.Text]()

    def handleOnLogin(event: ft.ControlEvent):
        username = usernameRef.current.value
        password = passwordRef.current.value

        # Log the details
        print(f"Username: {username}, Password: {password}")

        # validate the details
        if username == "":
            usernameErrorRef.current.value = "Please enter a username or an email"
            usernameErrorRef.current.visible = True
        else:
            usernameErrorRef.current.visible = False

        if password == "":
            passwordErrorRef.current.visible = True
        else:
            passwordErrorRef.current.visible = False

        # Sync UI with the state
        usernameErrorRef.current.update()
        passwordErrorRef.current.update()

    def form_field(
        label: str = "",
        placeholder: str = "",
        errorText: str = "Invalid field",
        isPassword: bool = False,
        ref: ft.Ref | None = None,
        errorRef: ft.Ref | None = None,
    ):
        return ft.Container(
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(value=label),
                    ft.TextField(
                        ref=ref,
                        hint_text=placeholder,
                        hint_style=ft.TextStyle(weight=ft.FontWeight.W_400),
                        text_size=14,
                        border_color="white",
                        border_width=0.5,
                        border_radius=8,
                        password=isPassword,
                    ),
                    ft.Text(
                        value=errorText,
                        color=ft.colors.RED_300,
                        ref=errorRef,
                        visible=False,
                    ),
                ],
            )
        )

    return ft.View(
        route="/login",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=450,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        # Header
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        "Textify", size=24, weight=ft.FontWeight.W_600
                                    ),
                                    ft.Text(
                                        "Sign in to your account to continue using our chat app.",
                                        size=16,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                ],
                            ),
                        ),
                        ft.Divider(thickness=0.5),
                        # Input fields (username and password)
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=24),
                            content=ft.Column(
                                spacing=20,
                                controls=[
                                    form_field(
                                        ref=usernameRef,
                                        label="Username or Email",
                                        placeholder="Enter your username or email",
                                        errorText="Please enter your username or email",
                                        errorRef=usernameErrorRef,
                                    ),
                                    form_field(
                                        ref=passwordRef,
                                        label="Password",
                                        placeholder="Enter your password",
                                        errorText="Please fill out this field",
                                        errorRef=passwordErrorRef,
                                        isPassword=True,
                                    ),
                                ],
                            ),
                        ),
                        # Actions (forget password and login button)
                        ft.Container(
                            expand=True,
                            border=ft.border.all(1),
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        alignment=ft.alignment.center_right,
                                        content=ft.TextButton(
                                            text="Forget password?",
                                            style=ft.ButtonStyle(
                                                padding=0,
                                                overlay_color="transparent",
                                            ),
                                        ),
                                    ),
                                    ft.Container(
                                        expand=True,  # Ensure the parent container is expanded
                                        border=ft.border.all(1, "red"),
                                        content=ft.FilledButton(
                                            text="Login",
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=4
                                                ),
                                                padding=ft.padding.symmetric(
                                                    horizontal=20, vertical=16
                                                ),
                                                visual_density=ft.VisualDensity.COMPACT,
                                            ),
                                            on_click=handleOnLogin,
                                            expand=True,  # Ensure the button takes up the full width within the parent container
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
