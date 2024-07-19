from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class QRUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    twofact = models.BooleanField(default=False)
    qr_id = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
