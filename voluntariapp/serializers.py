# voluntariapp/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','name','surname','password','project')

class EventSerializer(serializers.ModelSerializer):
    attending = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()

    def get_attending(self, obj):
        attender = self.context.get('user')
        return models.EventAttendee.objects.filter(event=obj, user=attender).exists()

    def get_attendance(self, obj):
        return models.EventAttendee.objects.filter(event=obj).count()
    class Meta:
        model = models.Event
        fields = ('id','creator','title','group','start_date','end_date','description','attendance','attending')

#FALTA ATTENDING!
class EventGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields='__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("id", "content", "forumtheme",)

class ForumThemeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id","title","description","tasks","finished","created_date")

class ForumThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id","title","description","tasks")

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rate
        fields = ("id", "event", "rate","description")

class EventAttendeeSerializer(serializers.ModelSerializer):
    event_date = serializers.SerializerMethodField()

    def get_attending(self, obj):
        event = models.Event.objects.filter(event=obj.event)
        return event.start_date
    class Meta:
        model = models.EventAttendee
        fields = ("id", "user", "event","attending","event_date")