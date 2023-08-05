"""The Color class, and some related utilities."""

from __future__ import annotations

from colorsys import hls_to_rgb, rgb_to_hls
from dataclasses import dataclass, field
from functools import cached_property

from .color_info import COLOR_TABLE

__all__ = ["Color"]

OFF_WHITE = (245, 245, 245)
OFF_BLACK = (35, 35, 35)


def calculate_luminance(base: Color) -> float:
    """Calculates the given color's perceived luminance (brightness).

    Source: https://stackoverflow.com/a/596243.
    """

    def _linearize(color: float) -> float:
        """Converts sRGB color to linear value."""

        if color <= 0.04045:
            return color / 12.92

        return float(((color + 0.055) / 1.055) ** 2.4)

    red = _linearize(base.rgb[0] / 255)
    green = _linearize(base.rgb[1] / 255)
    blue = _linearize(base.rgb[2] / 255)

    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def calculate_contrast(
    base: Color,
    white: Color | None = None,
    black: Color | None = None,
) -> Color:
    """Calculates the given color's black/white contrast.

    Args:
        base: The color that's used for the calculation.
        white: The color returned for "dark" bases. Defaults to (245, 245, 245).
        black: The color returned for "light" bases. Defaults to (35, 35, 35).

    Returns:
        A color that satisfies W3C's contrast guidelines when painted on top of `base`.
    """

    if base.luminance > 0.179:
        return (black or DEFAULT_BLACK).as_background(base.is_background)

    return (white or DEFAULT_WHITE).as_background(base.is_background)


def calculate_triadic_group(base: Color) -> tuple[Color, Color, Color]:
    """Returns the triadic group this color is within."""

    return base, base.hue_shift(1 / 3), base.hue_shift(2 / 3)


def calculate_analogous_group(base: Color) -> tuple[Color, Color, Color]:
    """Returns the analogous group this color is within."""

    return base, base.hue_shift(1 / 12), base.hue_shift(2 / 12)


def calculate_tetradic_group(base: Color) -> tuple[Color, Color, Color, Color]:
    """Returns the triadic group this color is within."""

    return base, base.hue_shift(1 / 4), base.complement, base.hue_shift(3 / 4)


@dataclass(frozen=True)
class Color:
    """A class that represents an RGB value."""

    rgb: tuple[int, int, int]
    is_background: bool = False

    luminance: float = field(init=False)
    hls: tuple[float, float, float] = field(init=False)
    hex: str = field(init=False)

    def __post_init__(self) -> None:
        def _set_field(
            key: str, value: float | str | tuple[float, float, float]
        ) -> None:
            object.__setattr__(self, key, value)

        if any(not 0 <= val < 256 for val in self.rgb):
            raise ValueError(
                f"Invalid RGB value {self.rgb!r}, for color; must be between 0 and 256"
            )

        _set_field("luminance", calculate_luminance(self))
        _set_field("hls", rgb_to_hls(*(val / 256 for val in self.rgb)))
        _set_field("hex", "#" + "".join(f"{i:02X}" for i in self.rgb))

    @classmethod
    def from_ansi(cls, ansi: str) -> Color:
        """Creates a color instance from an ANSI sequence's body."""

        parts = ansi.split(";")
        if len(parts) > 3:
            is_background = parts[0].startswith("4")

            return Color(
                (int(parts[2]), int(parts[3]), int(parts[3])),
                is_background=is_background,
            )

        ansi = parts[-1]

        # TODO: Handle garbage

        index = int(ansi)
        is_background = False

        # Convert indices to 16-color
        if len(parts) == 1:
            if 30 <= index < 38:
                index -= 30

            elif 40 <= index < 48:
                index -= 40
                is_background = True

            if 90 <= index < 98:
                index -= 82

            elif 100 <= index < 108:
                index -= 92
                is_background = True

        return Color(COLOR_TABLE[index], is_background=is_background)

    @classmethod
    def from_hex(cls, hexstring: str) -> Color:
        """Generates a Color instance from a hex string."""

        hexstring = hexstring.lstrip("#")

        return cls(
            (
                int(hexstring[:2], base=16),
                int(hexstring[2:4], base=16),
                int(hexstring[4:], base=16),
            )
        )

    @classmethod
    def black(cls) -> Color:
        """Returns a 100% black."""

        return Color((0, 0, 0))

    @classmethod
    def white(cls) -> Color:
        """Returns a 100% white."""

        return Color((255, 255, 255))

    @cached_property
    def ansi(self) -> str:
        """Returns the ANSI code that represents this color."""

        return f"{38 + 10*self.is_background};2;{';'.join(map(str, self.rgb))}"

    @cached_property
    def contrast(self) -> Color:
        """Returns this given color's black/white contrast color."""

        return calculate_contrast(self)

    @cached_property
    def complement(self) -> Color:
        """Returns the complement of this color."""

        if self.hls[0] == 0.0:
            return Color((255, 255, 255)) if self.hls[1] == 0.0 else Color((0, 0, 0))

        return self.hue_shift(0.5)

    @cached_property
    def triadic_group(self) -> tuple[Color, Color, Color]:
        """Returns the triadic group this color is part of."""

        return calculate_triadic_group(self)

    @cached_property
    def analogous_group(self) -> tuple[Color, Color, Color]:
        """Returns the analogous group this color is part of."""

        return calculate_analogous_group(self)

    @cached_property
    def tetradic_group(self) -> tuple[Color, Color, Color, Color]:
        """Returns the tetradic group this color is part of."""

        return calculate_tetradic_group(self)

    def lighten(self, shade_count: int, step_size: float = 0.1) -> Color:
        """Returns a lighter version of this color.

        The calculation is done by blending white with an alpha of:

            `shade_count * step_size`
        """

        return self.blend(Color.white(), alpha=shade_count * step_size)

    def darken(self, shade_count: int, step_size: float = 0.1) -> Color:
        """Returns a darker version of this color.

        The calculation is done by blending black with an alpha of:

            `shade_count * step_size`
        """

        return self.blend(Color.black(), alpha=shade_count * step_size)

    def as_background(self, setting: bool = True) -> Color:
        """Returns this color, with the given background setting."""

        return Color(self.rgb, is_background=setting)

    def hue_shift(self, amount: float) -> Color:
        """Returns a color with a hue offset of the given amount.

        Args:
            amount: The difference in hue. Given as 0-1f.

        Returns:
            This color, with its hue shifted.
        """

        hue, lightness, saturation = self.hls
        rgb = hls_to_rgb((hue + amount) % 1, lightness, saturation)

        return Color(
            (int(255 * rgb[0]), int(255 * rgb[1]), int(255 * rgb[2])),
            is_background=self.is_background,
        )

    def blend(self, other: Color, alpha: float) -> Color:
        """Blends this color with other by a certain alpha.

        Args:
            other: The color to blend into.
            alpha: How closely we should blend to the given color. For example,
                0.9 would be 10% self, 90% other.

        Returns:
            The blended color.
        """

        red1, green1, blue1 = self.rgb
        red2, green2, blue2 = other.rgb

        return Color(
            (
                int(red1 + (red2 - red1) * alpha),
                int(green1 + (green2 - green1) * alpha),
                int(blue1 + (blue2 - blue1) * alpha),
            )
        )

    def blend_complement(self, alpha: float) -> Color:
        """Blends this color by its complement.

        See `blend` for more info.

        Args:
            alpha: How closely we should blend into the complement.
        """

        return self.blend(self.complement, alpha)


DEFAULT_WHITE = Color((245, 245, 245))
DEFAULT_BLACK = Color((35, 35, 35))
