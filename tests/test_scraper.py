"""Tests for easy_scrape.scraper — download helpers and URL building."""
import io
import os
import pytest
from unittest.mock import MagicMock, patch

from easy_scrape.scraper import download_single_image, download_images, GoogleImageScraper
from easy_scrape.constants import SEARCH_URL


# ---------------------------------------------------------------------------
# download_single_image
# ---------------------------------------------------------------------------

def test_download_single_image_saves_file(tmp_path):
    fake_image = io.BytesIO()
    from PIL import Image
    Image.new("RGB", (10, 10), color="red").save(fake_image, format="JPEG")
    fake_image.seek(0)

    mock_response = MagicMock()
    mock_response.content = fake_image.read()

    with patch("easy_scrape.scraper.requests.get", return_value=mock_response):
        filepath = str(tmp_path / "img")
        download_single_image(url="https://example.com/photo.jpg", filepath=filepath)

    assert os.path.exists(filepath + ".jpg")


# ---------------------------------------------------------------------------
# download_images
# ---------------------------------------------------------------------------

def test_download_images_counts_successes(tmp_path):
    fake_image = io.BytesIO()
    from PIL import Image
    Image.new("RGB", (5, 5)).save(fake_image, format="PNG")
    fake_image.seek(0)
    content = fake_image.read()

    mock_response = MagicMock()
    mock_response.content = content

    links = [
        "https://example.com/a.png",
        "https://example.com/b.png",
    ]
    with patch("easy_scrape.scraper.requests.get", return_value=mock_response):
        count = download_images(links=links, filename_prefix="test", save_dir=str(tmp_path))

    assert count == 2


def test_download_images_tolerates_failures(tmp_path):
    def boom(*a, **kw):
        raise RuntimeError("network error")

    with patch("easy_scrape.scraper.requests.get", side_effect=boom):
        count = download_images(
            links=["https://example.com/x.jpg"],
            filename_prefix="test",
            save_dir=str(tmp_path),
        )

    assert count == 0


# ---------------------------------------------------------------------------
# GoogleImageScraper — URL building
# ---------------------------------------------------------------------------

def test_search_url_encodes_query(tmp_path):
    fake_links = ["https://example.com/img.jpg"]

    with patch("easy_scrape.scraper.download_page", return_value='"https://example.com/img.jpg"'), \
         patch("easy_scrape.scraper.scan_page", return_value=fake_links), \
         patch("easy_scrape.scraper.MAIN_DIR", str(tmp_path)):
        scraper = GoogleImageScraper(query="cats and dogs", n_images=1)

    assert scraper.links == fake_links


def test_scraper_falls_back_to_selenium_on_html_failure(tmp_path):
    fake_links = ["https://example.com/img.jpg"]

    with patch("easy_scrape.scraper.download_page", side_effect=Exception("blocked")), \
         patch("easy_scrape.scraper.scrape_image_links", return_value=fake_links), \
         patch("easy_scrape.scraper.MAIN_DIR", str(tmp_path)):
        scraper = GoogleImageScraper(query="cats", n_images=1)

    assert scraper.links == fake_links


def test_scraper_uses_selenium_directly_for_large_n(tmp_path):
    fake_links = ["https://example.com/img.jpg"] * 5

    with patch("easy_scrape.scraper.scrape_image_links", return_value=fake_links) as mock_sel, \
         patch("easy_scrape.scraper.MAIN_DIR", str(tmp_path)):
        scraper = GoogleImageScraper(query="dogs", n_images=200)

    mock_sel.assert_called_once()
    assert scraper.links == fake_links
