"""Generate colours to the Urban Intelligence style guide.

This module aims to assist in creating figures to a single style across the organisation. The colour palletes are engrained in this module and the core function is to modify the pallete to fit the need of the users figure.
"""

__all__ = ["generate_colour_palette", "get_colour"]

import colour as _colour_module
from typing import Union

__ALLOWABLE_FORMATS = ['hex', 'rgb', 'hsl']

__COLOUR_PALETTES = {
    "planning": {
        "monochromatic": ["#5aa33b", "#48942e", "#358520", "#207611", "#006700"],
        "divergent": ["#5aa33b", "#76b05a", "#8fbd77", "#a8ca95", "#c0d7b3", "#d9e4d2", "#f1f1f1", "#f1d4d4", "#f0b8b8", "#ec9c9d", "#e67f83", "#de6069", "#d43d51"], 
    },
    "access": {
        "monochromatic": ["#246783", "#21779a", "#1b86b2", "#1396cb", "#09a7e5", "#00b7ff"],
        "divergent": ["#246783", "#307d91", "#44929d", "#5ca8a8", "#78beb1", "#97d3bb", "#93daa7", "#9fdd8c", "#b7de6a", "#d8dc44", "#ffd416"], 
    },
    "risk": {
        "monochromatic": ["#0b2948", "#344a69", "#596d8d", "#7f93b1", "#a7bad8", "#d1e3ff"],
        "divergent": ["#0b2948", "#3b4b67", "#657187", "#9198a8", "#bfc2ca", "#eeeeee", "#fad3c1", "#ffb896", "#ff9d6b", "#fe813f", "#f86302"], 
    }
}

__UI_COLOURS = {
    # Add new UI colours here!
    "dark blue": "#0b2948",
    "secondary blue": "#04497c",
    "orange": "#f86302",
    "red": "#e70e02",
    "pink": "#ff8fa3",
    "light blue": "#00b7ff",
    "dark green": "#006700",
    "light green": "#",
    "white": "#ffffff",
    "black": "#000000",
}

AVAILABLE_COLOURS = list(__UI_COLOURS.keys())

def generate_colour_palette(palette: str = "risk", scheme: str = "divergent", n: int = 5, format: str = "hex") -> list:
    """Generate a specific colour palette resembling a Urban Intelligence product.

    Return a list of colours that relate to an Urban Intelligence colour palette (planning, access or risk) for a given colour scheme (monochromatic or divergent). Colours are always returned in the order of positive to worst (in respect of what the palette is defining as a good and poor colour).

    Args:
        palette: The Urban Intelligence product to mimic the palette off.
        scheme: The colour scheme required ('divergent' or 'monochromatic').
        n: The number of unique colours required.
    
    Returns:
        A list of n colours relating to the requested palette and scheme.
    """

    if palette not in __COLOUR_PALETTES.keys():
        raise ValueError(f"The given pallete: {palette} is not acceptable. Please choose from: {list(__COLOUR_PALETTES.keys())}")
    if scheme not in __COLOUR_PALETTES[palette].keys():
        raise ValueError(f"The given scheme: {scheme} is not acceptable. Please choose from: {list(__COLOUR_PALETTES[palette].keys())}")
    assert n > 0 and type(n) == int, "The requested number of colours ('n') must be a positive integer."

    default_colours = __COLOUR_PALETTES[palette][scheme]
    if len(default_colours) == 0:
        raise NotImplementedError(f"Unfortunately, there is no colour scheme for the {palette} palette using a {scheme} scheme. Apologies for the inconvenience.")
    elif len(default_colours) == n:
        # A perfect match!
        return [_colour_module.Color(colour).__getattribute__(f"get_{format}")() for colour in default_colours]
    elif n == 1:
        # If requested only one colour, return the first one
        return [_colour_module.Color(default_colours[0]).__getattribute__(f"get_{format}")()]
    else:
        # Create a range of colours with n steps between the two ends
        return [color.__getattribute__(f"get_{format}")() for color in _colour_module.Color(default_colours[0]).range_to(_colour_module.Color(default_colours[-1]), steps=n)]


def get_colour(name: str = "dark blue", format: str = "hex") -> Union[str, tuple]:
    """Get one specific colour, by name.

    Return a colour that relates to an Urban Intelligence product, by name. See uintel.colours.AVAILABLE_COLOURS for a list of available colour names.

    Args:
        name: The name of the colour to return.
        format: The format the colour should be returned as
    
    Returns:
        The value of the requested colour in the requested format.
    """
    if name not in __UI_COLOURS:
        raise ValueError(f"The given name: {name} is not acceptable. Please choose from: {list(__UI_COLOURS.keys())}")
    if format not in __ALLOWABLE_FORMATS:
        raise ValueError(f"The given format: {format} is not acceptable. Please choose from: {__ALLOWABLE_FORMATS}")
    return _colour_module.Color(__UI_COLOURS[name]).__getattribute__(f"get_{format}")()
