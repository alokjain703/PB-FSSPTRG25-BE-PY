from typing import List, Optional
class BlogUtils:
    # convert list of strings to comma separated string
    @staticmethod
    def _convert_list_to_comma_separated_string( input_list: List[str]) -> str:
        return ", ".join(input_list)
    
    # convert comma separated string to list of strings
    @staticmethod
    def _convert_comma_separated_string_to_list(input_string: str) -> List[str]:
        return [item.strip() for item in input_string.split(",") if item.strip()]

    # Public method to convert tags list to comma-separated string for database storage
    @staticmethod
    def convert_tags_to_string(tags: List[str]) -> str:
        """Convert a list of tags to a comma-separated string for database storage."""
        if not tags:
            return ""
        return ", ".join(str(tag) for tag in tags)
    
    # Public method to convert comma-separated string to tags list for API responses
    @staticmethod
    def convert_tags_to_list(tags_str: str) -> List[str]:
        """Convert a comma-separated string to a list of tags for API responses."""
        if not tags_str or tags_str.strip() == "":
            return []
        return [tag.strip() for tag in tags_str.split(",") if tag.strip()]

  