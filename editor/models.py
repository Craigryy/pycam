from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')  # Link to User
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded by {self.user.username}"
