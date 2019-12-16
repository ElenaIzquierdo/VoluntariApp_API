# voluntariapp/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'

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
        fields = ("id", "author","content","created_date", "forumtheme")

class ForumThemeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id","title","creator","description", "finished", "created_date", "group")

class ForumThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id","title","creator","description", "finished", "created_date", "group")

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rate
        fields = ("event", "comments", "snack_rate", "line_rate", "circle_rate", "respect_rate", "activity_rate")

class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventAttendee
        fields = ("id", "user", "event")

class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cours
        fields='__all__'

class QuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quarter
        fields = '__all__'

class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Week
        fields = '__all__'