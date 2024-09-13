import flet as ft
import flet_route as fr

from app.components.sidebar import Sidebar
from app.views.home_page import HomePage
from app.views.not_found_view import NotFoundView


def MainPageView(page: ft.Page, params: fr.Params, basket: fr.Basket):
    # Create the main content container that will be updated based on the navigation
    main_content_area = ft.Container(padding=0, expand=True, content=HomePage(page))

    def handle_navigation(route: str):
        if route == "home:page":
            main_content_area.content = HomePage(page)
        else:
            main_content_area.content = NotFoundView(page)
        page.update()

    sidebar = Sidebar(page, on_navigate=handle_navigation)

    return ft.View(
        "/",
        controls=[
            ft.Row(controls=[sidebar, main_content_area], expand=True, spacing=0)
        ],
    )
