from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

#Falta mes info del user: grup del casal per exemple

class Cours(models.Model):
    name = models.TextField(blank=False, null=False, unique=True)
    year = models.IntegerField(blank=False, null=False, unique=True)

class Quarter(models.Model):
    name = models.TextField(blank=False, null=False, unique=True)
    season = models.TextChoices('Season', 'HIVERN TARDOR PRIMAVERA')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=False, blank=False)

#Gestionar tema dies i dates i tal
class Setmana(models.Model):
    name = models.TextField(blank=False, null=False)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, null=False, blank=False)
    rate_avg = models.IntegerField(blank=True, null=True)
    attendance_avg = models.IntegerField(blank=True, null=True)

class CentreInteres(models.Model):
    name = models.TextField(blank=False, null=False)

class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_creator',
                                null=True)
    title = models.CharField(blank=True, max_length=255)
    group = models.TextField(null=False)
    created_date = models.DateField(auto_now_add=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True,null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class EventAttendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventattendee_user',
                                null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'event']


class ForumTheme(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forumtheme_creator',
                                null=True)
    title = models.CharField(blank=True, max_length=255)
    created_date = models.DateTimeField(default=timezone.now)
    finished = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    group = models.TextField(null=False)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=400)
    forumtheme = models.ForeignKey(ForumTheme, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

class Rate(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, primary_key=True)
    circle_rate = models.IntegerField(blank=True,null=True)
    snack_rate = models.IntegerField(blank=True,null=True)
    respect_rate = models.IntegerField(blank=True,null=True)
    line_rate = models.IntegerField(blank=True,null=True)
    activity_rate = models.IntegerField(blank=True,null=True)
    comments = models.TextField(blank=True, null=True)


