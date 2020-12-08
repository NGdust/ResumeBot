from django.db import models

# Create your models here.
class FAQ(models.Model):
    type = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.type