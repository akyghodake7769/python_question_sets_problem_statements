import re
import json

class UserDataProcessor:
    """
    User Data Processing System using Regular Expressions and JSON.
    Validates and processes user data with regex-based operations.
    """

    def __init__(self):
        """
        Initialize the UserDataProcessor.
        Create storage for processed user data.
        """
        self.metadata = {}

    def validate_email(self, email: str) -> bool:
        """
        Validate email format using regex.
        
        Parameters:
            email (str): Email address to validate
        
        Returns:
            bool: True if valid email format, False otherwise
        
        Pattern: ^[\\w\\.-]+@[\\w\\.-]+\\.[\\w]+$
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def validate_username(self, username: str) -> bool:
        """
        Validate username format using regex.
        Username must be 5-10 characters, alphanumeric only.
        
        Parameters:
            username (str): Username to validate
        
        Returns:
            bool: True if valid username format (5-10 alphanumeric), False otherwise
        
        Pattern: ^[a-zA-Z0-9]{5,10}$
        """
        pattern = r'^[a-zA-Z0-9]{5,10}$'
        return bool(re.match(pattern, username))

    def clean_phone(self, phone_str: str) -> str:
        """
        Extract all digits from phone string (remove non-digit characters).
        
        Parameters:
            phone_str (str): Phone string with possible formatting characters
        
        Returns:
            str: String containing only digits extracted from phone
        
        Uses: re.sub(r'\\D', '', phone_str) to remove all non-digit characters
        """
        return re.sub(r'\D', '', phone_str)

    def to_json(self, data: dict) -> str:
        """
        Convert dictionary to pretty-printed JSON string.
        
        Parameters:
            data (dict): Dictionary to convert to JSON
        
        Returns:
            str: JSON formatted string with 4-space indentation
        
        Uses: json.dumps() with indent=4
        """
        return json.dumps(data, indent=4)

    def from_json(self, json_str: str) -> dict:
        """
        Parse JSON string to dictionary.
        
        Parameters:
            json_str (str): JSON formatted string to parse
        
        Returns:
            dict: Dictionary parsed from JSON string
        
        Uses: json.loads()
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return {}
