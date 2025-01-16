from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class CommentData:
    """
    Represents a user's comment on a blog article.

    Attributes:
        content: The text content of the comment.
        author: The name of the comment's author.
        email: (Optional) The email address of the author.
    """
    content: str
    author: str
    email: Optional[str] = None

class ValidationError(Exception):
    """Custom exception raised when validation of a comment fails."""
    pass

class CommentValidator:
    """
    Validates a user's comment based on length, author presence, and email format.
    """
    def __init__(self):
        self.min_length = 5  # Minimum content length
        self.max_length = 1000  # Maximum content length
        self.allowed_email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def validate(self, comment: CommentData) -> bool:
        """
        Validates the given comment.

        Args:
            comment: The CommentData object to validate.

        Returns:
            True if the comment is valid.

        Raises:
            ValidationError: If the comment fails any validation check.
        """
        # Check content length
        if not (self.min_length <= len(comment.content) <= self.max_length):
            raise ValidationError("Comment length must be between 5 and 1000 characters")

        # Check if author is provided
        if not comment.author.strip():
            raise ValidationError("Author name is required")

        # Validate email format if provided
        if comment.email and not self.allowed_email_pattern.match(comment.email):
            raise ValidationError("Invalid email format")

        return True

class CommentSanitizer:
    """
    Sanitizes a user's comment by removing all dangerous or disallowed HTML tags
    along with their content. Only allowed tags like <b> and <i> are preserved.
    """
    def __init__(self):
        # List of allowed tags (e.g., bold and italic)
        self.allowed_tags = ['b', 'i']

        # Regex to match any opening or closing HTML tag
        self.any_tag_pattern = re.compile(r'<(/?[a-zA-Z0-9]+)[^>]*>')

        # Regex to match disallowed tags and their content
        self.disallowed_tag_pattern = re.compile(
            r'<(?!/?(?:b|i)\b)[a-zA-Z0-9]+[^>]*>.*?</[a-zA-Z0-9]+>', re.DOTALL
        )

    def sanitize(self, comment: CommentData) -> CommentData:
        """
        Sanitizes the comment's content by removing all disallowed tags and their content.

        Args:
            comment: The CommentData object to sanitize.

        Returns:
            A sanitized CommentData object with safe content.
        """
        # Step 1: Remove all disallowed tags and their content
        sanitized_content = self.disallowed_tag_pattern.sub('', comment.content)

        # Step 2: Remove any remaining disallowed tags (e.g., self-closing tags)
        def clean_html(match):
            tag = match.group(1).lower()  # Extract the tag name
            if tag.strip('/') in self.allowed_tags:  # Check if it is in the allowed list
                return match.group(0)  # Keep allowed tags as is
            return ''  # Remove disallowed tags

        sanitized_content = self.any_tag_pattern.sub(clean_html, sanitized_content)

        # Return a new CommentData object with sanitized content
        return CommentData(
            content=sanitized_content,
            author=comment.author.strip(),
            email=comment.email.strip() if comment.email else None
        )

class CommentProcessor:
    """
    Combines validation and sanitization of user comments.
    """
    def __init__(self):
        self.validator = CommentValidator()
        self.sanitizer = CommentSanitizer()

    def process_comment(self, comment: CommentData) -> CommentData:
        """
        Processes a comment by validating and sanitizing it.

        Args:
            comment: The CommentData object to process.

        Returns:
            A sanitized and validated CommentData object.

        Raises:
            ValidationError: If validation fails.
        """
        # Step 1: Validate the comment
        self.validator.validate(comment)

        # Step 2: Sanitize the comment
        return self.sanitizer.sanitize(comment)
    
###########################
# Example usage
try:
    comment = CommentData(
        content="<script>alert('hacked!');</script> Great article! <b>Thanks</b> for sharing. <div>Should not appear</div>",
        author="John Doe",
        email="john@example.com"
    )

    processor = CommentProcessor()
    safe_comment = processor.process_comment(comment)
    print(f"Original content: {comment.content}")
    print(f"Processed content: {safe_comment.content}")

except ValidationError as e:
    print(f"Validation failed: {str(e)}")