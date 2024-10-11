from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError



# Create your models here.

class conferences(models.Model):
    
    titre=models.CharField(max_length=255)
    description=models.TextField()
    start_date=models.DateField(default=timezone.now().date())
    end_date=models.DateField()
    location=models.CharField(max_length=255)
    price=models.FloatField()

    capacite=models.IntegerField(validators=[MaxValueValidator(limit_value=200,message='capacity must be under 200')])
    update_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    program=models.FileField(upload_to='files/',validators=[FileExtensionValidator(allowed_extensions=['pdf','png','jpeg','jpg'],message='only pdf, png, jpeg, jpg')])
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="conferences")
    def clean(self):
        if self.end_date<= self.start_date:
            raise ValidationError('end_date must be greater than start_date')
    class Meta:
        verbose_name_plural="conferences"
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start_date__gte=timezone.now().date()
                    )
                ,name='the date must be greater or equal to today'
            )
        ]

