from flet import (
    IconButton,
    Image,
    ImageFit,
    RoundedRectangleBorder,
    padding as pad,
    ButtonStyle,
    OptionalEventCallable,
)


class MyIconButton(IconButton):
    def __init__(
        self,
        url: str,
        size: int = 32,
        padding: int = 8,
        corner_radius: int = 6,
        color: str = "white",
        visible: bool = True,
        on_click: OptionalEventCallable = None,
    ):
        super().__init__()

        self.content = Image(
            src=f"assets/{url}",
            color=color,
            fit=ImageFit.CONTAIN,
        )
        self.style = ButtonStyle(
            padding=pad.all(padding),
            shape=RoundedRectangleBorder(radius=corner_radius),
        )
        self.width = size
        self.height = size
        self.on_click = on_click
        self.visible = visible
