from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')  # Link to User
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded by {self.user.username}"


class ImageEdit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_images')  # Link to User
    original_image = models.ImageField(upload_to='originals/')
    edited_image = models.ImageField(upload_to='edited/', blank=True, null=True)
    effect_applied = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image ID: {self.id}, Effect: {self.effect_applied or 'None'}"
