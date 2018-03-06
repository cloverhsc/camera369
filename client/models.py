# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from authtools.models import AbstractEmailUser
from django.core import validators

# handle error
from django.core.exceptions import ObjectDoesNotExist

# Regex
import re

# uuid
# import uuid

# import datetime

# Create your models here.


class DomainManager(models.Manager):
    def create_domain(self, domain_name):
        """
        Save domain name
        """
        if not re.match(
            r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$",
            domain_name
        ):
            raise ObjectDoesNotExist
        else:
            domain = self.model(name=domain_name)
            domain.save()
            return domain


class Domain(models.Model):
    name = models.CharField(max_length=254)

    objects = DomainManager()

    def __str__(self):
        return self.name

    def show_domain(self):
        return self.name

    class Meta:
        db_table = 'Domain'


class User(AbstractEmailUser):
    first_name = models.CharField(_('First name'), max_length=100, blank=True)
    last_name = models.CharField(_('Last name'), max_length=100, blank=True)
    sex = models.CharField(_('sex'), max_length=1, null=True, blank=True)
    register_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=False,
        blank=True,
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                _('Enter a valid username. '
                'This value may contain only letters, numbers '
                'and @/./+/-/_ characters.'), 'invalid'),
        ],
    )

    friends = models.ManyToManyField(
        "self", through='CameraFriend', symmetrical=False
    )

    '''
        is_superuser: inheritance from PermissionMixin
    '''

    is_manager = models.BooleanField(
        _('manager user'), default=False,
        help_text=_(
            'No manager role.'
        )
    )

    USERNAME_FIELD = 'email'

    def get_email(self):
        """ Return the email back. """
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (
            self.last_name, self.first_name
        )
        return unicode(full_name)

    class Meta:
        db_table = 'User'


class CarManager(models.Manager):
    def create_car(self, **extra_fields):
        car = self.model(
            **extra_fields
        )
        car.save()
        return car


class Cars(models.Model):
    license_plate = models.CharField(
        _('license plate'), max_length=10, blank=True, null=True,
        help_text=_('license plate'))
    color = models.CharField(
        _('color of car'), max_length=30, blank=True, null=True,
        help_text=_('color of car')
    )
    brand = models.CharField(
        _('brand of car'), max_length=128, blank=True, null=True,
        help_text=_('brand of car')
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="the car's owner"
    )

    USERNAME_FIELD = 'license_plate'

    objects = models.Manager()
    carcreate = CarManager()

    def get_license_plate(self):
        return unicode(self.license_plate)

    def get_color(self):
        return unicode(self.color)

    def get_brand(self):
        return unicode(self.brand)

    def __str__(self):
        return "license plate:%s\ncolor:%s\nbrand:%s" % (
            self.license_plate, self.color, self.brand)

    class Meta:
        db_table = 'Cars'


# class DeviceManager(models.Manager):
#     def create_camera(self, )


class Camera(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="the camera's owner"
    )
    sn = models.CharField(max_length=128, unique=True)
    bind_at = models.DateTimeField(_('bind at'), auto_now_add=True)
    fob_num = models.CharField(max_length=64, unique=True)
    name = models.CharField(
        _('camera name or tag'), max_length=128, blank=True, null=True
    )
    domain = models.ForeignKey(Domain)

    # objects = DeviceManager()
    USERNAME_FIELD = id

    def __str__(self):
        return 'Camera table'

    def get_owner(self):
        return self.user.email

    def get_fob(self):
        return self.fob_num

    def get_camera_name(self):
        return self.name

    def get_sn(self):
        return self.sn

    class Meta:
        db_table = 'Camera'


class CameraFriend(models.Model):
    camera = models.ManyToManyField(Camera, related_name='camera_id')
    friend = models.ForeignKey(User, related_name='friend_id')
    is_active = models.BooleanField(
        _('can get alert and stream'),
        default=False,
        help_text=_(
            'if true this friend can get alert and streaming'
        )
    )

    def __str__(self):
        return self.friend

    class Meta:
        db_table = 'CameraFriend'


class ProductSerial(models.Model):
    sn = models.CharField(max_length=128, unique=True)
    be_used = models.BooleanField(
        _('be used'),
        default=False,
        help_text=_(
            'if be used or binded. set true'
        )
    )

    def __str__(self):
        return self.sn

    class Meta:
        db_table = 'ProductSerial'
