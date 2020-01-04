# voluntariapp/serializers.py
from django.utils import timezone
from rest_framework import serializers
from . import models
import pytz

utc = pytz.UTC


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('mobile_phone', 'days', 'group')


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


class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventAttendee
        fields = ("id", "event", "user")

    def create(self, validated_data):
        eventattendee = models.EventAttendee(**validated_data)
        eventattendee.save()
        return eventattendee


class AttendeesSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    class Meta:
        model = models.EventAttendee
        fields = ("id", "username")


class EventSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField()
    attending = serializers.SerializerMethodField()
    finished = serializers.SerializerMethodField()
    attenders = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    def get_attendance(self, obj):
        return models.EventAttendee.objects.filter(event=obj).count()

    def get_attenders(self, obj):
        attenders = models.EventAttendee.objects.filter(event=obj)
        return AttendeesSerializer(attenders, many=True).data

    def get_rate(self, obj):
        try:
            rate = models.Rate.objects.get(event=obj)
            return RateSerializer(rate).data

        except models.Rate.DoesNotExist:
            return None

    def get_attending(self, obj):
        return models.EventAttendee.objects.filter(event=obj, user=self.context['request'].user).exists()

    def get_finished(self, obj):
        return obj.start_date < timezone.now()

    class Meta:
        model = models.Event
        fields = ('id', 'title', 'group', 'start_date', 'end_date', 'description', 'attendance', 'week', 'attending',
                  'finished', 'attenders', 'rate')


# FALTA ATTENDING!
class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return (obj.author.first_name + ' ' + obj.author.last_name)

    class Meta:
        model = models.Comment
        fields = ("id", "user", "content", "created_date", "forumtheme")


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("id", "content", "created_date", "forumtheme", "author")


class ForumTopicGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTopic
        fields = ("id", "title", "creator", "description", "finished", "created_date", "group")


class ForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTopic
        fields = ("id", "title", "creator", "description", "finished", "created_date", "group")


class ForumCreateTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTopic
        fields = ("id", "title", "description", "finished", "group")


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rate
        fields = ("event", "comments", "snack_rate", "line_rate", "circle_rate", "respect_rate", "activity_rate")


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
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


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = '__all__'


class ScheduleGetFromCentreInteresSerializer(serializers.ModelSerializer):
    finished = serializers.SerializerMethodField()

    def get_finished(self, obj):
        if obj.date == None:
            return False
        else:
            now = timezone.now()
            return obj.date < now

    class Meta:
        model = models.Schedule
        fields = ('id', 'date', 'description', 'centreinteres', 'finished')
