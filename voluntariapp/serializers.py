# voluntariapp/serializers.py
from django.utils import timezone
from rest_framework import serializers
from . import models
import pytz

utc = pytz.UTC


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('mobile_phone','days','group')


class UserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source='username')
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'password', 'profile', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = models.User(**validated_data)
        user.set_password(password)
        user.save()
        models.UserProfile.objects.create(user=user, **profile_data)
        return user

    #def update(self, instance, validated_data):
        #profile_data = validated_data.pop('profile')
        #profile = instance.profile

        #instance.email = validated_data.get('email', instance.email)
        #instance.save()

        #profile.title = profile_data.get('mobile_phone', profile.mobile_phone)
        #profile.dob = profile_data.get('days', profile.days)
        #profile.address = profile_data.get('group', profile.group)
        #profile.save()

        #return instance

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
        fields = ('id', 'creator', 'title', 'group', 'start_date', 'end_date', 'description', 'attendance', 'attending', 'week')


# FALTA ATTENDING!
class EventGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("id", "author", "content", "created_date", "forumtheme")


class ForumThemeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id", "title", "creator", "description", "finished", "created_date", "group")


class ForumThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id", "title", "creator", "description", "finished", "created_date", "group")


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
        fields = '__all__'


class QuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quarter
        fields = '__all__'


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Week
        fields = '__all__'


class CentreInteresSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CentreInteres
        fields = '__all__'


class ObjectiuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Objectiu
        fields = '__all__'


class ExplicacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Explicacio
        fields = '__all__'


class ExplicacioGetFromCentreInteresSerializer(serializers.ModelSerializer):
    finished = serializers.SerializerMethodField()

    def get_finished(self, obj):
        if obj.date == None:
            return False
        else:
            now = timezone.now()
            return obj.date < now

    class Meta:
        model = models.Explicacio
        fields = ('id', 'date', 'description', 'centreinteres', 'finished')
