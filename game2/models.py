from django.db import models


class ImageForGame(models.Model):
    """
    Represents an image used in the game and the correct label associated with it.

    Fields:
    - title: The name of the image (max 255 characters), defaults to 'Untitled'.
    - image: The image file uploaded to the 'game_images/' folder.
    - correct_label: The correct label or class for this image (max 50 characters).
    """

    title = models.CharField(max_length=255, default="Untitled")
    image = models.ImageField(upload_to="game_images/")
    correct_label = models.CharField(max_length=50)

    def __str__(self):
        """
        Returns the title of the image when represented as a string.
        """
        return self.title
