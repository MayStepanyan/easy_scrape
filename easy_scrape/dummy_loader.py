"""
Utils for parsing html string and its substrings via requests library
"""

import requests


def scan_page(html, extensions, n_max):
    """
    Scan html for urls that contain any of given extensions

    Parameters
    ----------
    html : str
        html to scan
    extensions : iter
        extensions to search for
    n_max : int
        maximal number of urls to return

    Returns
    -------
    out : list
        urls that contain any of given extensions
    """
    end = -1
    image_links = []
    if not html:
        raise ValueError("Please provide a non-empty html to parse")
    # Google Images is JS-rendered; if there are no quoted https:// URLs at all,
    # the response is a JS shell — fall back to Selenium.
    if '"https://' not in html:
        raise ValueError("No image URLs found in raw HTML — page may be JS-rendered.")
    while len(image_links) < n_max:
        raw_start = html.find('"https://', end + 1)
        if raw_start == -1:
            break
        start = raw_start + 1  # The link starts with " and ends with it too
        end = html.find('"', start)
        candidate_link = html[start:end]
        if any(candidate_link.endswith(extension) for extension in extensions):
            image_links.append(candidate_link)
    if not image_links:
        raise ValueError("HTML contained https:// URLs but none matched the requested extensions.")
    return image_links


def download_page(url):
    """Get and return a raw html page"""
    headers = {
        'User-Agent': (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=30)
    return response.content.decode()
