from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from django.conf import settings

from crum import get_current_request

####################################################

class Users(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    number_address = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    phone_number = models.PositiveIntegerField(blank=True, null=True)
    dni = models.PositiveIntegerField(blank=True, null=True)
    image_user = models.ImageField(upload_to='user/', null=True, blank=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def get_image(self):
        if self.image:
            return "{}{}".format(settings.MEDIA_URL, self.image)
        return "{}{}".format(settings.STATIC_URL, "img/generic-user.png")

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        super().save(*args, **kwargs)
