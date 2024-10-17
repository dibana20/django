from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import conferences
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone





def email_verif(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('email unvalid only @esprit.tn domain is allowed')


class participant(AbstractUser):
    only_numbers=RegexValidator('^[0-9]{8}$','only 8 numbers are allowed')
    #only_numbers=RegexValidator('^\d{8}$','only numbers are allowed')
    #{1,8} minimum 1 maximum 8 
    #{1,}minimum 1
    #{,8}
    cin=models.CharField(max_length=10,primary_key=True,validators=[only_numbers])
    email=models.CharField(unique=True,max_length=255,validators=[email_verif])
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    username=models.CharField(max_length=255,unique=True)
    USERNAME_FIELD='username'
    #si je fait l'authentification avec email (USERNAME_FIELD='email')
    CHOICES=(
        ('etudiant','etudiant'),
        #valeur recuperée et qui va etre stocker dans la base donner, la valeur qui va etre affichée dans l'interface
        ('chercheur','chercheur'),
        ('docteur','docteur'),
        ('enseignant','enseignant')
    )
    participant_category=models.CharField(max_length=255,choices=CHOICES)
    #choices va etre convertit a type select
    #reservations=models.ManyToManyField(conferences.through='reservations')
    reservations=models.ManyToManyField(conferences,through='reservation',related_name='reservations')
    update_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural="participants"
    def __str__(self):
        return f"User name = {self.username}"



class reservation(models.Model):
    conferences=models.ForeignKey(conferences,on_delete=models.CASCADE)
    participant=models.ForeignKey(participant,on_delete=models.CASCADE)
    confirmed=models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.conferences.start_date < timezone.now().date():
            raise ValidationError('you can only reserve for upcomming confrences')
        reservation_count=reservation.objects.filter(
            participant=self.participant,
            reservation_date=self.reservation_date
        )
        if reservation_count>=3:
            raise ValidationError('reservation_count >=3')
    class Meta :
        unique_together=('conferences','participant')
        #Un participant ne peut pas réserver plusieurs fois la même conférence
