from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from taggit.managers import TaggableManager
import logging
logger = logging.getLogger(__name__)

WING_CHOICES = [
    ('ARMY', _('Army')),
    ('NAVAL', _('Naval')),
    ('AIR_FORCE', _('Air Force'))
]

REASON_CHOICES = [
    ('SPAM', _('Spam')),
    ('INAPPROPRIATE', _('Inappropriate')),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, blank=True)
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/avatar.jpg')
    description = models.CharField(max_length=100, blank=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
    camps = TaggableManager(blank=True)
    wing = models.CharField(max_length=10, choices=WING_CHOICES, blank=True)

    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)
        
        # Check if there is an image and process it
        if self.image:
            try:
                # Open the image file
                img = Image.open(self.image)
                logger.debug(f"Opened image: {self.image.name}")
                
                # Check if the image dimensions are larger than the allowed size
                if img.height > 170 or img.width > 170:
                    output_size = (170, 170)
                    img.thumbnail(output_size)
                    
                    # Save the resized image to an in-memory file
                    in_mem_file = BytesIO()
                    img.save(in_mem_file, format='JPEG')
                    img_data = BytesIO(in_mem_file.getvalue())
                    
                    # Save the in-memory file to the image field
                    self.image.save(self.image.name, InMemoryUploadedFile(
                        img_data, None, self.image.name, 'image/jpeg', sys.getsizeof(img_data), None))
                    logger.debug(f"Resized and saved image: {self.image.name}")

            except Exception as e:
                logger.error(f"Error processing image for user {self.user.username}: {e}")
                # Handle the error appropriately (e.g., notify the user, use a default image, etc.)

    def __str__(self):
        return f"{self.user.username}'s Profile"
class UserReport(models.Model):
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    reason = models.CharField(max_length=13, choices=REASON_CHOICES)
    reporting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporting_user')
    date_reported = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.reported_user.username
