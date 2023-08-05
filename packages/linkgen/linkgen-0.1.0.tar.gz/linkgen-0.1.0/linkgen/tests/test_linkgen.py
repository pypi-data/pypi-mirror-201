from textwrap import dedent

import pytest

import linkgen


def test_two_blocks():
    with pytest.raises(ValueError):
        linkgen.linkgen({"block": [{"link": False, "heading": False}]})


def test_unknown_block():
    with pytest.raises(ValueError):
        linkgen.linkgen({"block": [{"invalid": False}]})


def test_plaintext_block():
    assert linkgen.plain("Lorem ipsum") == "<p>Lorem ipsum</p>\n"


def test_heading_block():
    with pytest.raises(AssertionError):
        linkgen.heading(0, "Invalid number")
    with pytest.raises(ValueError):
        linkgen.heading("NaN", "Not a number")
    assert linkgen.heading(3, "Lorem ipsum") == "<h3>Lorem ipsum</h3>\n"


def test_image_block():
    assert linkgen.image("/example.png") == '<img src="/example.png">\n'
    assert linkgen.image("/example.png", "Example") == '<img alt="Example" src="/example.png">\n'


def test_link_block():
    expected = dedent(
    '''
        <a class="taplink" href="https://example.com" title="Example">
          <span class="taplink-text">Example</span>
        </a>
    ''').lstrip()
    assert linkgen.link("https://example.com", "Example") == expected


def test_card_block():
    expected = dedent(
    '''
        <div class="card">
          <p class="card-title">Test</p>
          <p class="card-subtitle">Test case</p>
        </div>
    ''').lstrip()
    assert linkgen.card("Test", "Test case") == expected
