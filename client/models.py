# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# handle error
# from django.core.exceptions import ObjectDoesNotExist

# Regex
# import re

# uuid
# import uuid

# import datetime

# Create your models here.


class UserManager(models.Manager):
    def _create_user(
        self,
        email,
        password,
        is_superuser,
        is_manager,
        is_staff,
        **extra_fields
    ):

        user = self.model(
            email=email,
            is_superuser=is_superuser,
            is_manager=is_manager,
            is_staff=is_staff,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_normal_user(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            False,          # is super user
            False,          # is manager
            True,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email'), max_length=254, unique=True,
        help_text=_(
            'Required ! 254 or fewer, Letter, digits and @/./-/_ only.'
        ))      # end of email setting

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(_('First name'), max_length=100, blank=True)
    last_name = models.CharField(_('Last name'), max_length=100, blank=True)
    sex = models.CharField(_('sex'), max_length=1, null=True, blank=True)
    register_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_(
            'Designates whether this user should be treated as '
            'active, Unselect this. instead of deleteing accounts.'
        )
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

    is_staff = models.BooleanField(
        _('staff status'), default=True,
        help_text=_(
            'All client role.'
        )
    )

    USERNAME_FIELD = 'email'

    objects = models.Manager()
    usercreate = UserManager()      # my models manager

    def get_email(self):
        """ Return the email back. """
        return unicode(self.email)

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


class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    sn = models.CharField(max_length=128, unique=True)
    bind_at = models.DateTimeField(_('bind at'), auto_now_add=True)
    
