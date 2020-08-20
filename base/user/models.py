import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Username address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'

    objects = UserAccountManager()
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff', default=False)

    email = models.EmailField('email', unique=True, blank=False)
    username = models.CharField('username',  unique=True, blank=True, null=True, max_length=400)

    comments_admin = models.TextField('Комментарий администратора', blank=True)
    is_verify = models.BooleanField('Подтвержденный', default=False)
    black_list = models.BooleanField('Черный список', default=False)
    def __unicode__(self):
        return self.email


class Employer(User):
    company = models.CharField('Название компании', blank=True, null=True, max_length=256)
    category = models.CharField('Род деятельности', blank=True, null=True, max_length=256)
    address = models.CharField('Адресс', blank=True, null=True, max_length=1024)
    fio = models.CharField('ФИО', blank=True, null=True, max_length=1024)
    phone = models.CharField('Телефон', blank=True, null=True, max_length=1024)
    url = models.CharField('Ссылка на сайт компании', blank=True, null=True, max_length=1024)

    chat_id = models.IntegerField('ID чата в телеграме', blank=True)

class Candidate(User):
    name = models.CharField('Имя', blank=True, null=True, max_length=256)
    secondname = models.CharField('Фамилия', blank=True, null=True, max_length=256)
    age = models.IntegerField('Возраст', blank=True)
    address = models.CharField('Адресс', blank=True, null=True, max_length=1024)
    phone = models.CharField('Телефон', blank=True, null=True, max_length=1024)
    url = models.CharField('Ссылка на соц.сети', blank=True, null=True, max_length=1024)

    chat_id = models.IntegerField('ID чата в телеграме', blank=True)
