from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models, IntegrityError
from django.db.utils import DataError

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    middle_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, max_length=100, blank=True, validators=[validate_email])
    password = models.CharField(max_length=100, blank=True, null=False, default='password')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "'id': " + str(self.id) + ", " \
               "'first_name': '" + self.first_name + "', " \
               "'middle_name': '" + self.middle_name + "', " \
               "'last_name': '" + self.last_name + "', " \
               "'email': '" + self.email + "', " \
               "'created_at': " + str(int(self.created_at.timestamp())) + ", " \
               "'updated_at': " + str(int(self.updated_at.timestamp())) + ", " \
               "'role': " + str(self.role) + ", " \
               "'is_active': " + str(self.is_active)

    def __repr__(self):
        return ("CustomUser(id=" + str(self.id) + ")")

    @staticmethod
    def get_by_id(user_id):
        if CustomUser.objects.filter(id=user_id):
            return CustomUser.objects.get(id=user_id)
        else:
            return None

    @staticmethod
    def get_by_email(email):
        if CustomUser.objects.filter(email=email):
            return CustomUser.objects.get(email=email)
        else:
            return None

    @staticmethod
    def delete_by_id(user_id):
        if CustomUser.objects.filter(id=user_id):
            CustomUser.objects.filter(id=user_id).delete()
            return True
        else:
            return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        try:
            validate_email(email)
            if len(first_name) > 20 or len(middle_name) > 20 or len(last_name) > 20:
                raise DataError
            new_user = CustomUser.objects.create(first_name=first_name,
                                                 middle_name=middle_name,
                                                 last_name=last_name,
                                                 password=password,
                                                 email=email)
            return new_user
        except IntegrityError:
            return None
        except ValidationError:
            return None
        except DataError:
            return None
    """
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :return: a new user object which is also written into the DB
    """


    def to_dict(self):
        return { 'id': self.id,
                 'first_name': self.first_name,
                 'middle_name': self.middle_name,
                 'last_name': self.last_name,
                 'email': self.email,
                 'created_at': int(self.created_at.timestamp()),
                 'updated_at': int(self.updated_at.timestamp()),
                 'role': self.role,
                 'is_active': self.is_active}

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):

        if first_name != None:
            CustomUser.objects.filter(id=self.id).update(first_name=first_name)
        if last_name != None:
            CustomUser.objects.filter(id=self.id).update(last_name=last_name)
        if middle_name != None:
            CustomUser.objects.filter(id=self.id).update(middle_name=middle_name)
        if password != None:
            CustomUser.objects.filter(id=self.id).update(password=password)
        if role != None:
            CustomUser.objects.filter(id=self.id).update(role=role)
        if is_active != None:
            CustomUser.objects.filter(id=self.id).update(is_active=is_active)

    @staticmethod
    def get_all():
        return CustomUser.objects.all()
    """
        returns data for json request with QuerySet of all users
    """


    def get_role_name(self):
        return ROLE_CHOICES[self.role][1]
    """
        returns str role name
    """

