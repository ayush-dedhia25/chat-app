import flet as ft

from app.util.state import StateManager

StateValue = str | int | float
PageOrComponent = ft.Page | ft.Control


def useState(initial_value: StateValue, page_or_component: PageOrComponent):
    state = StateManager(initial_value, page_or_component, True)
    return (state.getValue, state.setValue)


def useRef(initial_value: StateValue, page_or_component: PageOrComponent):
    state = StateManager(initial_value, page_or_component, False)
    return (state.getValue, state.setValue)
