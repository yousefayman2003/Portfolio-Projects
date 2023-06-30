from typing import Any
from django.db import models, connection
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils import timezone

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, date_of_birth, gender, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have an first name')
        if not last_name:
            raise ValueError('Users must have an last name')
        if not date_of_birth:
            raise ValueError('Users must have an date of birth')
        if not gender:
            raise ValueError('Users must have an gender')
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, date_of_birth, gender, phone, password):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone=phone
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(
        max_length=20, verbose_name='first name', default=None)
    last_name = models.CharField(
        max_length=20, verbose_name='last name', default=None)
    date_of_birth = models.DateField(
        verbose_name='date of birth', default=None)
    gender = models.CharField(
        max_length=6, verbose_name='gender', default=None, db_column='gender')
    phone = models.CharField(max_length=11, unique=True,
                             db_column='phone_number', verbose_name='phone number')
    about = models.TextField(max_length=1000)
    image = models.ImageField(default='default.png', upload_to='profile', validators=[
                              FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    # some required fields for django
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'date_of_birth', 'gender', 'phone']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'user'


class PageModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='created_by', db_column='created_by')
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='date_created')
    company_email = models.CharField(max_length=255)
    likes_number = models.IntegerField(
        verbose_name='likes_number', db_column='likes_number', default=0)

    class Meta:
        db_table = 'page'


class PostModel(models.Model):
    title = models.CharField(
        max_length=100, verbose_name='title', default=None)
    content = models.TextField(
        max_length=10000, verbose_name='content', default=None)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='created_by', db_column='created_by')
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='date_created')
    likes_number = models.IntegerField(
        verbose_name='likes_number', db_column='likes_number', default=0)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comment_set.all().count()

    def comments(self):
        return self.comment_set.all()

    class Meta:
        db_table = 'post'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comment'


class Shared(models.Model):
    # Field name made lowercase.
    sharing = models.IntegerField(db_column='Sharing')
    # Field name made lowercase.
    time_of_sharing = models.DateTimeField(db_column='Time_Of_Sharing')
    # Field name made lowercase. The composite primary key (Post_ID, User_ID) found, that is not supported. The first column is selected.
    post = models.OneToOneField(
        PostModel, models.CASCADE, db_column='Post_ID', primary_key=True)
    # Field name made lowercase.
    user = models.ForeignKey(User, models.CASCADE, db_column='User_ID')

    class Meta:
        db_table = 'shared'
        unique_together = (('post', 'user'),)


class Chat(models.Model):
    chat_id = models.IntegerField(primary_key=True)
    user1 = models.CharField(max_length=255)
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    user2 = models.CharField(max_length=255)

    class Meta:
        db_table = 'chat'


class Receiver(models.Model):
    id = models.OneToOneField(
        User, models.CASCADE, db_column='receiver_id', primary_key=True)

    class Meta:
        db_table = 'receiver'


class Sender(models.Model):
    id = models.OneToOneField(
        User, models.CASCADE, db_column='sender_id', primary_key=True)

    class Meta:
        db_table = 'sender'


class Friend(models.Model):
    # The composite primary key (id_1, friendsid_2) found, that is not supported. The first column is selected.
    id = models.AutoField(primary_key=True)
    id_1 = models.OneToOneField(
        User, models.CASCADE, db_column='id_1', unique=False)
    id_2 = models.ForeignKey(
        User, models.CASCADE, db_column='id_2', related_name='id_2', unique=False)

    def __str__(self):
        return self.id_2.first_name

    class Meta:
        db_table = 'friend'
        unique_together = (('id_1', 'id_2'),)


class Messages(models.Model):
    chat_fk = models.ForeignKey(
        Chat, on_delete=models.CASCADE, db_column='chat_id')
    sender_fk = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='sender_id', related_name='sender_fk')
    receiver_fk = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='receiver_id')
    content = models.CharField(max_length=255)
    time_field = models.DateTimeField(db_column='time_', auto_now_add=True)
    message_id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'messages'


def make_query(model, query):

    return model.objects.raw(query)
