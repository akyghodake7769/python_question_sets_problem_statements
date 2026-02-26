import re

class UserDataProcessor:
    """
    User Data Processing System using Regular Expressions.
    Validates and processes user data with regex-based operations.
    """

    def __init__(self):
        """
        Initialize the UserDataProcessor.
        Create storage for processed user data.
        """
        self.users = []

    def validate_email(self, email: str) -> bool:
        """
        Validate email format using regex.
        
        Parameters:
            email (str): Email address to validate
        
        Returns:
            bool: True if valid email format, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_phone(self, phone: str) -> bool:
        """
        Validate phone number format using regex.
        
        Parameters:
            phone (str): Phone number to validate (format: +1-234-567-8900 or similar)
        
        Returns:
            bool: True if valid phone format, False otherwise
        """
        pattern = r'^(\+\d{1,3})?[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}$'
        return bool(re.match(pattern, phone))

    def extract_usernames(self, text: str) -> list:
        """
        Extract usernames from text (format: @username).
        
        Parameters:
            text (str): Text to search for usernames
        
        Returns:
            list: List of usernames found (without @ symbol)
        """
        pattern = r'@([a-zA-Z0-9_]+)'
        matches = re.findall(pattern, text)
        return matches

    def mask_sensitive_data(self, text: str, pattern_type: str = 'email') -> str:
        """
        Mask sensitive data in text (email or phone).
        
        Parameters:
            text (str): Text containing sensitive data
            pattern_type (str): Type of data to mask ('email' or 'phone')
        
        Returns:
            str: Text with masked sensitive data
        """
        if pattern_type == 'email':
            pattern = r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            replacement = r'***@***'
        elif pattern_type == 'phone':
            pattern = r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
            replacement = '***-***-****'
        else:
            return text
        
        return re.sub(pattern, replacement, text)

    def get_statistics(self) -> dict:
        """
        Get statistics about processed data.
        
        Returns:
            dict: Contains 'total_validations', 'patterns_found', 'data_masked'
                  Returns zeros if no data processed
        """
        return {
            'total_validations': 0,
            'patterns_found': 0,
            'data_masked': 0
        }
