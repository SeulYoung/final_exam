from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Password must not be empty')

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=100, primary_key=True)
    username = models.CharField(verbose_name='username', max_length=100, unique=True, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class WeiboData(models.Model):
    num = models.AutoField(primary_key=True)
    author = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    likes = models.IntegerField(default=0)
    postData = models.DateTimeField(auto_now_add=True)


class WeiboLike(models.Model):
    num = models.IntegerField()
    liker = models.CharField(max_length=100)


class Follow(models.Model):
    author = models.CharField(max_length=100)
    follower = models.CharField(max_length=100)
