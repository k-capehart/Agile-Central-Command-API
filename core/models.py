from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('username')._unique = False


class UsernameValidatorAllowSpace(UnicodeUsernameValidator):
   regex = r'^[\w.@+\- ]+$'


class TrackableDateModel(models.Model):
   '''
   Abstract model to Track the creation/updated date for a model.
   '''

   create_date = models.DateTimeField(auto_now_add=True)
   update_date = models.DateTimeField(auto_now=True)

   class Meta:
       abstract = True


class Session(models.Model):
   title = models.CharField(max_length=30)
   description = models.CharField(max_length=100, null=True, blank=True)
   TYPES = (
        ('R', 'Retro'),
        ('P', 'Poker'),
    )
   type = models.CharField(max_length=10, null=True, choices=TYPES)
   owner = models.ForeignKey(
       settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
   )

   @property
   def group_name(self):
       '''
       Returns the Channels Group name that sockets should subscribe to to get sent
       messages as they are generated.
       '''
       return "session-%s" % self.id


class RetroActionItems(TrackableDateModel):
   '''
   Store action items of Retro Board
   '''

   owner = models.ForeignKey(
       settings.AUTH_USER_MODEL, on_delete=models.PROTECT
   )
   session = models.ForeignKey(
       Session, on_delete=models.PROTECT
   )
   action_item_text = models.TextField(max_length=2000)


class SessionMember(TrackableDateModel):
   '''
   Store all users from a session
   '''

   session = models.ForeignKey(
       Session, on_delete=models.PROTECT
   )
   member = models.ForeignKey(
       settings.AUTH_USER_MODEL, on_delete=models.PROTECT
   )


class User(AbstractUser):
   username_validator = UsernameValidatorAllowSpace()
   username = models.CharField(
       _('username'),
       max_length=150,
       help_text=_(
           'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
       validators=[username_validator],
   )
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']

   def __str__(self):
       return self.username


class Story(models.Model):
   title = models.CharField(max_length=50)
   description = models.CharField(max_length=100, null=True, blank=True)
   story_points = models.IntegerField()
   session = models.ForeignKey(Session, on_delete=models.CASCADE)

   def __str__(self):
       return self.title