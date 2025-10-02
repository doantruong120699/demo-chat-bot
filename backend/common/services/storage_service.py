import os
import base64
import uuid
from django.conf import settings

class StorageService:
    @staticmethod
    def save_base64_image(base64_string, folder="images"):
        """
        Save a base64-encoded image to the media folder and return the relative file path.

        Args:
            base64_string (str): The base64-encoded image string (may include data:image/png;base64,...).
            folder (str): Subfolder in MEDIA_ROOT to save the image.

        Returns:
            str: Relative file path to the saved image (e.g., "images/uuid.png"), or None if failed.
        """
        # Remove header if present
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        try:
            # Try to decode base64
            image_data = base64.b64decode(base64_string)
        except Exception:
            return None

        # Generate unique filename
        filename = f"{uuid.uuid4().hex}.png"
        media_folder = os.path.join(settings.MEDIA_ROOT, folder)
        os.makedirs(media_folder, exist_ok=True)
        file_path = os.path.join(media_folder, filename)

        try:
            with open(file_path, "wb") as f:
                f.write(image_data)
        except Exception:
            return None

        # Return relative path for use in URLs
        return os.path.join(folder, filename)
