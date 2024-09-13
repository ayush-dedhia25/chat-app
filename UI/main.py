import flet as ft
import flet_route as fr

from app.views.login_page import LoginPageView
from app.views.main_view import MainPageView


def main(page: ft.Page):
    page.padding = 0

    app_routes = [
        fr.path("/", clear=True, view=MainPageView),
        fr.path("/login", clear=True, view=LoginPageView),
    ]

    fr.Routing(page=page, app_routes=app_routes)

    page.go("/login")
    # page.add(ft.Row(controls=[sidebar, main_content_area], expand=True, spacing=0))


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
