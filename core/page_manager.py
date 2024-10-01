import json
from flask import current_app
from typing import Dict, Any, List


class PageManager:
    def __init__(self):
        """
        Initialize the PageManager with the path to the JSON file from Flask's configuration.
        """
        self.json_file_path = current_app.config.get('PAGE_CONTENT_PATH', 'data/pages.json')
        self.pages = self.load_pages()

    def load_pages(self) -> Dict[str, Any]:
        """
        Load all pages from the JSON file.

        :return: Dictionary of pages where keys are page IDs and values are page data.
        """
        try:
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            current_app.logger.error(f"Page content file not found at {self.json_file_path}")
            return {}
        except json.JSONDecodeError:
            current_app.logger.error(f"Failed to decode JSON from {self.json_file_path}")
            return {}

    def save_pages(self):
        """
        Save the current state of pages to the JSON file.
        """
        with open(self.json_file_path, 'w') as file:
            json.dump(self.pages, file, indent=4)

    def add_content_to_page(self, page_id: str, content: str) -> bool:

        """

        Add content to an existing page.


        :param page_id: ID of the page to add content to.

        :param content: New content to add.

        :return: True if content was added, False otherwise.

        """

        if page_id in self.pages:
            self.pages[page_id]["content"] += content

            self.save_pages()

            return True

        return False

    def add_page(self, title: str, content: str) -> str:
        """
        Add a new page to the JSON file.

        :param title: Title of the page.
        :param content: Content of the page.
        :return: The ID of the newly created page.
        """
        new_id = self.generate_unique_id()
        self.pages[new_id] = {"title": title, "content": content}
        self.save_pages()
        return new_id

    def delete_page(self, page_id: str) -> bool:
        """
        Delete a page by its ID.

        :param page_id: ID of the page to delete.
        :return: True if the page was deleted, False if it didn't exist.
        """
        if page_id in self.pages:
            del self.pages[page_id]
            self.save_pages()
            return True
        return False

    def modify_page(self, page_id: str, title: str = None, content: str = None) -> bool:
        """
        Modify an existing page.

        :param page_id: ID of the page to modify.
        :param title: New title for the page, if changing.
        :param content: New content for the page, if changing.
        :return: True if the page was modified, False if it didn't exist.
        """
        if page_id in self.pages:
            if title:
                self.pages[page_id]["title"] = title
            if content:
                self.pages[page_id]["content"] = content
            self.save_pages()
            return True
        return False

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """
        Retrieve a page by its ID.

        :param page_id: ID of the page to retrieve.
        :return: Dictionary containing page data or None if not found.
        """
        return self.pages.get(page_id)

    def list_pages(self) -> List[Dict[str, Any]]:
        """
        List all pages.

        :return: List of dictionaries, each representing a page.
        """
        return list(self.pages.values())

    def generate_unique_id(self) -> str:
        """
        Generate a unique ID for a new page.

        :return: A unique string ID.
        """
        import uuid
        return str(uuid.uuid4())


# Utility functions (could be methods of PageManager or kept as standalone functions)
def get_page_title(page_data: Dict[str, Any]) -> str:
    """
    Extract the title from page data.

    :param page_data: Dictionary containing page data.
    :return: Title of the page, or a default title if not provided.
    """
    return page_data.get('title', 'Untitled Page')


def get_page_content(page_data: Dict[str, Any]) -> str:
    """
    Extract the content from page data.

    :param page_data: Dictionary containing page data.
    :return: Content of the page, or an empty string if not provided.
    """
    return page_data.get('content', '')

# Usage example:
# manager = PageManager()
# page_content = manager.get_page("some_id")
# title = get_page_title(page_content)
# content = get_page_content(page_content)
