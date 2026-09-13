WINDOW_SIZE = (1480, 1200)
IMG_PER_ROW = 3

# Google frequently changes these CSS class names.
# If scraping returns 0 results, inspect google.com/search?tbm=isch in DevTools:
# - IMG_CLS_NAME: class on the large <img> in the preview panel (click any thumbnail)
# - SHOW_MORE_BTN_NAME: class on the "Show more results" button at the bottom
IMG_CLS_NAME = "sFlh5c"

XPATH_TEMPLATE = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'

PAGE_LOAD_TIME = 0.5
SHOW_MORE_BTN_NAME = "LZ4I"
MAX_RETRIES_PER_IMAGE = 3
SEARCH_URL = 'https://www.google.com/search?q='
MAIN_DIR = "scrapped_images"
