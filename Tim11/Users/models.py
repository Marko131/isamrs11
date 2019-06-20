from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .validators import validate_phone
from django.dispatch import receiver
from django.db.models.signals import post_save
import threading
from django.core.mail import EmailMessage
from Tim11.settings import EMAIL_HOST_USER


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    city = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True, validators=[validate_phone])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.pk) + self.email

@receiver(post_save, sender=CustomUser)
def admin_change_password(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        send_html_mail("Account activation",
                       f"<a href=\"http://127.0.0.1:8000/change_password/{instance.id}\"> Click here to activate your account. </a>",
                       [instance.email])



class Request(models.Model):
    user_send = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_send')
    user_accept = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_accept')

    def __str__(self):
        return self.user_send.email + ' - ' + self.user_accept.email

class Friends(models.Model):
    class Meta:
        verbose_name_plural = 'Friends'

    current_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='current_user')
    friend_list = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.current_user.email
