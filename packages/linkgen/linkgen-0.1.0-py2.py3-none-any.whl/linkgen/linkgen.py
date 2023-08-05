# Copyright (c) 2022 Anna <cyber@sysrq.in>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import html
from typing import Optional

from linkgen.utils import open_tag, close_tag, indent

ClassList = Optional[list[str]]


def init_attrs(property: Optional[str] = None, classes: ClassList = None) -> dict[str, str]:
    attrs = {}
    if classes:
        attrs["class"] = " ".join(classes)
    if property:
        attrs["property"] = property
    return attrs


def plain(text: str, property: Optional[str] = None, classes: ClassList = None,
          **kwargs: dict) -> str:
    """ Plain text block """
    attrs = init_attrs(property, classes)

    result = open_tag("p", attrs)
    result += html.escape(text)
    result += close_tag("p")
    return result + "\n"


def heading(level: int, text: str, property: Optional[str] = None,
            classes: ClassList = None, **kwargs: dict) -> str:
    """ Heading block """
    level = int(level)
    assert 1 <= level <= 6

    attrs = init_attrs(property, classes)

    result = open_tag(f"h{level}", attrs)
    result += html.escape(text)
    result += close_tag(f"h{level}")
    return result + "\n"


def image(url: str, alt: Optional[str] = None, property: Optional[str] = None,
          classes: ClassList = None, **kwargs: dict) -> str:
    """ Image block """
    url = html.escape(url)

    attrs = init_attrs(property, classes)
    attrs["src"] = url
    if alt:
        attrs["alt"] = html.escape(alt)

    return open_tag("img", attrs) + "\n"


def svg_icon(css_class: str, path: str, alt: Optional[str] = None) -> str:
    result = ""
    assert path.endswith(".svg")

    attrs = {
        "xmlns": "http://www.w3.org/2000/svg",
        "height": "2em", "width": "2em",
        "class": css_class
    }
    if alt:
        attrs["role"] = "img"
        attrs["aria-label"] = html.escape(alt)
    else:
        attrs["role"] = "presentation"

    result += indent(1) + open_tag("svg", attrs) + "\n"
    for line in open(path):
        result += indent(2) + line
    result += indent(1) + close_tag("svg") + "\n"
    return result


def link(url: str, title: str, icon: Optional[dict] = None,
         property: Optional[str] = None, **kwargs: dict) -> str:
    """ Taplink block """

    def span(text: str) -> str:
        result = indent(1) + open_tag("span", {"class": "taplink-text"})
        result += html.escape(text)
        result += close_tag("span") + "\n"
        return result

    attrs = init_attrs(property, ["taplink"])
    attrs["href"] = html.escape(url)
    attrs["title"] = html.escape(title)

    result = open_tag("a", attrs) + "\n"
    if icon is not None:
        result += svg_icon("taplink-icon", icon["path"], icon.get("alt"))

    result += span(title)
    result += close_tag("a") + "\n"
    return result


def card(title: str, subtitle: str = "", icon: Optional[dict] = None,
         property: Optional[str] = None, **kwargs: dict) -> str:
    """ Simple card (icon + subtitle) block """

    def paragraph(css_class: str, text: str) -> str:
        result = indent(1) + open_tag("p", {"class": css_class})
        result += text
        result += close_tag("p") + "\n"
        return result

    title = html.escape(title)
    subtitle = html.escape(subtitle)

    attrs = init_attrs(property, ["card"])
    result = open_tag("div", attrs) + "\n"
    if icon is not None:
        result += svg_icon("card-icon", icon["path"], icon.get("alt", ""))

    result += paragraph("card-title", title)
    if subtitle:
        result += paragraph("card-subtitle", subtitle)

    result += close_tag("div") + "\n"
    return result


def block(kind: str, options: dict) -> str:
    if kind == "plain":
        return plain(**options)
    if kind == "heading":
        return heading(**options)
    if kind == "image":
        return image(**options)
    if kind == "link":
        return link(**options)
    if kind == "card":
        return card(**options)
    raise ValueError(f"Unknown block type: {kind}")


def linkgen(config: dict) -> str:
    """ Main function """
    result = ""

    general = config.get("general", {})
    htmlf = general.get("html", {})
    html_pre_file = htmlf.get("pre")
    html_post_file = htmlf.get("post")

    if html_pre_file is not None:
        result += open(html_pre_file).read()

    for blk in config.get("block", {}):
        if len(blk) == 0:
            continue
        if len(blk) > 1:
            keys = ", ".join(blk.keys())
            raise ValueError(f"Cannot mix block types: {keys}")
        kind, options = blk.popitem()
        result += block(kind, options)

    if html_post_file is not None:
        result += open(html_post_file).read()

    return result
