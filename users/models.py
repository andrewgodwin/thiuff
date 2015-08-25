from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, validators
from django_pgjson.fields import JsonBField


class UserManager(BaseUserManager):
    """
    Manager for users providing helpful methods. That's what managers do.
    """

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Main user model. Username is for display purposes, but still unique.
    Emails and other backends are how logins work, and it's possible to have
    any number of those (see UserAuth), though there's still a single password
    which is stored on this model.
    """

    username = models.CharField(
        max_length=40,
        unique=True,
        help_text='40 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                'Enter a valid username. This value may contain only letters, numbers ' 'and @/./+/-/_ characters.'
            ),
        ],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    name = models.CharField(max_length=255, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.name

    @classmethod
    def by_username(cls, username):
        return cls.objects.filter(username__iexact=username).first()

    @classmethod
    def by_identifier(cls, id_type, identifier):
        auth = UserAuth.by_identifier(id_type, identifier)
        if auth is None:
            return None
        else:
            return auth.user


class UserAuth(models.Model):
    """
    A way of authenticating a user. Generally either a third-party verifiable
    identity using OAuth or similar, or an identity token the user can provide
    themselves like an email address that will be combined with the password
    field on User.

    Each identity backend should have a single "identifier" field that can be
    looked up via an indexed equality query, and then all other relevant data
    in a "data" JSON blob.
    """

    TYPE_CHOICES = [
        ("email", "Email"),
        ("twitter", "Twitter"),
        ("facebook", "Facebook"),
        ("google", "Google"),
    ]

    user = models.ForeignKey(User, related_name="auths")
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    identifier = models.TextField(db_index=True)
    data = JsonBField(blank=True, null=True)

    @classmethod
    def by_identifier(cls, id_type, identifier):
        # Check identifier type is valid
        if id_type not in [x for x, y in cls.TYPE_CHOICES]:
            raise ValueError("Invalid identifier type %s" % id_type)
        # Normalise identifier
        identifier = cls.normalise_identifier(id_type, identifier)
        # Get the right object
        try:
            return UserAuth.objects.get(type=type, identifier=identifier)
        except UserAuth.DoesNotExist:
            return None

    @classmethod
    def normalise_identifier(cls, id_type, identifier):
        """
        Normalises identifiers to avoid comparison errors.
        """
        if id_type == "email":
            return identifier.lower()
        elif id_type == "twitter":
            return identifier.lower()
        else:
            return identifier
