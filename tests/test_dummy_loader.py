"""Tests for easy_scrape.dummy_loader"""
import pytest
from easy_scrape.dummy_loader import scan_page


EXTS = (".jpg", ".jpeg", ".png")


def _html(*urls):
    """Wrap URLs in minimal quoted HTML so scan_page can find them."""
    parts = " ".join(f'"{u}"' for u in urls)
    return f"<html>{parts}</html>"


def test_returns_matching_urls():
    html = _html("https://example.com/a.jpg", "https://example.com/b.png")
    result = scan_page(html, EXTS, n_max=10)
    assert result == ["https://example.com/a.jpg", "https://example.com/b.png"]


def test_respects_n_max():
    html = _html(
        "https://example.com/1.jpg",
        "https://example.com/2.jpg",
        "https://example.com/3.jpg",
    )
    result = scan_page(html, EXTS, n_max=2)
    assert len(result) == 2


def test_skips_non_matching_extensions():
    html = _html(
        "https://example.com/a.gif",
        "https://example.com/b.jpg",
        "https://example.com/c.mp4",
    )
    result = scan_page(html, EXTS, n_max=10)
    assert result == ["https://example.com/b.jpg"]


def test_raises_on_empty_html():
    with pytest.raises(ValueError, match="non-empty"):
        scan_page("", EXTS, n_max=5)


def test_raises_when_no_https_urls():
    with pytest.raises(ValueError, match="JS-rendered"):
        scan_page("<html>no urls here</html>", EXTS, n_max=5)


def test_raises_when_no_extension_match():
    html = _html("https://example.com/a.gif", "https://example.com/b.svg")
    with pytest.raises(ValueError, match="none matched"):
        scan_page(html, EXTS, n_max=5)


def test_deduplication_not_enforced():
    """scan_page itself doesn't deduplicate; the caller does if needed."""
    html = _html("https://example.com/a.jpg", "https://example.com/a.jpg")
    result = scan_page(html, EXTS, n_max=10)
    assert result.count("https://example.com/a.jpg") == 2
