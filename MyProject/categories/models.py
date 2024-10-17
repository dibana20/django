from django.db import models
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

# Create your models here.

def validate_letters_only(value):
    if not re.match(r'^[a-zA-Z\s]+$',value):
        raise ValidationError('Letters only')
    

class Category(models.Model):
    letters_only=RegexValidator('^[a-zA-Z\s]+$','only letters are allowed')
    #pass
    #title=models.CharField(max_length=255, validators=[letters_only])
    title=models.CharField(max_length=255, validators=[validate_letters_only])

    update_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    #auto now il va prendre date system automatiquement
    class Meta:
        verbose_name_plural="categories"
    def __str__(self):
            return f"categorie = {self.title}"

