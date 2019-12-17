# voluntariapp/urls.py
from django.urls import path
from voluntariapp.views_directory import user_views, event_views, forum_views, comment_views, rate_views, \
                                        eventattendee_views, cours_views, quarter_views, week_views, \
                                        centreinteres_views, objectius_view
from voluntariapp.views_directory.user_views import login

urlpatterns = [
    path('login',login),

    path('users', user_views.UserListView.as_view()),

    path('event', event_views.EventListView.as_view()),
    path('event/<id_event>', event_views.EventDetailView.as_view(), name="event-details"),

    path('forum', forum_views.ForumThemeListView.as_view(), name="forum"),
    path('forum/<id_forumtheme>', forum_views.ForumThemeDetailView.as_view(), name="forumtheme-detail"),

    path('comment', comment_views.ListCommentView.as_view(), name="comments-all"),
    path('comment/<id_comment>', comment_views.CommentDetailView.as_view(), name="comments-detail"),
    path('comment/forum/<id_forumtheme>', comment_views.CommentFromThemeView.as_view(), name="comments-from-theme"),

    path('rate', rate_views.ListRateView.as_view(), name="rate-all"),
    path('rate/<id_rate>', rate_views.RateDetailView.as_view(), name="rate-detail"),
    path('rate/event/<id_event>', rate_views.RateFromEventView.as_view(), name="rate-from-event"),

    path('eventattendee', eventattendee_views.ListEventAttendeeView.as_view(), name="eventattendee-all"),
    path('event/<id_event>/attendee', eventattendee_views.AttendeeView.as_view(), name="eventattendee-detail"),

    path('cours', cours_views.ListCoursView.as_view(), name="cours-all"),
    path('cours/<id_cours>', cours_views.CoursDetailView.as_view(), name="cours-detail"),

    path('quarter', quarter_views.ListQuarterView.as_view(), name="quarter-all"),
    path('quarter/<id_quarter>', quarter_views.QuarterDetailView.as_view(), name="quarter-detail"),
    path('quarter/cours/<id_cours>', quarter_views.QuarterFromCoursView.as_view(), name="quarter-from-cours"),

    path('week', week_views.ListWeekView.as_view(), name="week-all"),
    path('week/<id_week>', week_views.WeekDetailView.as_view(), name="week-detail"),
    path('week/quarter/<id_quarter>', week_views.WeekFromQuarterView.as_view(), name="week-from-quarter"),

    path('centreinteres', centreinteres_views.ListCentreInteresView.as_view(), name="centreinteres-all"),
    path('centreinteres/<id_centreinteres>', centreinteres_views.CentreInteresDetailView.as_view(), name="centreinteres-detail"),

    path('objectiu', objectius_view.ListObjectiuView.as_view(), name="objectiu-all"),
    path('objectiu/<id_objectiu>', objectius_view.ObjectiuDetailView.as_view(), name="objectiu-detail"),
    path('objectiu/centreinteres/<id_centreinteres>', objectius_view.ObjectiuFromCentreInteresView.as_view(), name="objectiu-from-centreinteres"),
]