import flet as ft

StateValue = str | int | float


class StateManager:
    def __init__(
        self,
        initial_value: StateValue,
        page_or_component: ft.Page | ft.Control,
        should_update_ui: bool = True,
    ):
        self.value = initial_value
        self.page_or_component = page_or_component
        self.should_update_ui = should_update_ui

    def setValue(self, new_value: StateValue):
        self.value = new_value
        if self.should_update_ui:
            self.page_or_component.update()

    def getValue(self):
        return self.value
