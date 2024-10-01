import json
from flask import current_app


def load_page_content(page_name):
    """
    Load content for a specific page from JSON file.

    :param page_name: Name of the page to load content for.
    :return: Dictionary containing page content, or None if not found.
    """
    # Get the path to the JSON file from Flask's configuration
    json_path = current_app.config.get('PAGE_CONTENT_PATH', 'data/pages.json')

    try:
        with open(json_path, 'r') as file:
            pages = json.load(file)
        return pages.get(page_name)
    except FileNotFoundError:
        current_app.logger.error(f"Page content file not found at {json_path}")
        return None
    except json.JSONDecodeError:
        current_app.logger.error(f"Failed to decode JSON from {json_path}")
        return None


def get_page_title(page_data):
    """
    Extract the title from page data.

    :param page_data: Dictionary containing page data.
    :return: Title of the page, or a default title if not provided.
    """
    return page_data.get('title', 'Untitled Page')


def get_page_content(page_data):
    """
    Extract the content from page data.

    :param page_data: Dictionary containing page data.
    :return: Content of the page, or an empty string if not provided.
    """
    return page_data.get('content', '')