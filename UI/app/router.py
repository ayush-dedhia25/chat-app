import flet as ft

from app.views.not_found_view import NotFoundView


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {}
        self.page.on_route_change = self.on_route_change

    def add_route(self, route: str, view):
        self.routes[route] = view

    def on_route_change(self, route):
        self.page.views.clear()
        new_view = self.routes.get(self.page.route)
        if new_view:
            self.page.views.append(new_view(self.page))
        else:
            self.page.views.append(NotFoundView(self.page))
        self.page.update()

    def navigate(self, route: str):
        self.page.go(route)
