import cv2
import numpy as np

from cat.ble import run_ble
from cat.cmds import PRINT_WIDTH, cmds_print_img

FONT_SIZE_MULTIPLIER = 0.5
FONT_FAMILY = cv2.FONT_HERSHEY_DUPLEX


class Text:
    size: int
    bold: bool
    underline: bool
    centered: bool
    content: str

    def __init__(
        self,
        content: str,
        size: int = 1,
        bold: bool = False,
        underline: bool = False,
        centered: bool = False,
    ):
        self.content = content
        self.size = size
        self.bold = bold
        self.underline = underline
        self.centered = centered

    def dimensions(self) -> tuple[int, int]:
        (width, height), baseline = cv2.getTextSize(
            self.content,
            FONT_FAMILY,
            FONT_SIZE_MULTIPLIER * self.size,
            self.thickness(),
        )
        return width, height + baseline

    def thickness(self) -> int:
        if self.bold:
            if self.size > 3:
                return 3
            else:
                return 2
        return 1


class CatPrinter:
    content: list[Text] = []

    def __receipt_height(self):
        minimum = sum([ht for _, ht in [frag.dimensions() for frag in self.content]])
        minimum += 10 * len(self.content)
        return (minimum + 7) & ~7  # Round up to multiple of 8

    def __image_from_text(self):
        img = np.zeros((self.__receipt_height(), PRINT_WIDTH), np.uint8)
        running_height = 0

        for fragment in self.content:
            width, height = fragment.dimensions()
            x = 10 if not fragment.centered else int((PRINT_WIDTH - width) / 2)
            _ = cv2.putText(
                img,
                fragment.content,
                (x, running_height + height),
                FONT_FAMILY,
                FONT_SIZE_MULTIPLIER * fragment.size,
                (255, 255, 255),
                fragment.thickness(),
                cv2.LINE_AA,
            )
            if fragment.underline:
                _ = cv2.line(
                    img,
                    (x, running_height + height),
                    (x + width, running_height + height),
                    (255, 255, 255),
                    2,
                )

            running_height += height + 10

        return img

    def textln(
        self,
        text: str,
        size: int = 1,
        bold: bool = False,
        underline: bool = False,
        centered: bool = False,
    ):
        self.content.extend(
            [Text(line, size, bold, underline, centered) for line in text.splitlines()]
        )

    async def cut(self):
        data = cmds_print_img(self.__image_from_text())
        await run_ble(data)
