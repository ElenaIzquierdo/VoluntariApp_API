# voluntariapp/urls.py
from django.urls import path
from voluntariapp.views_directory import user_views, event_views, forum_views, comment_views, rate_views, \
                                        eventattendee_views, cours_views, quarter_views, week_views, \
                                        centreinteres_views, objectius_view, explicacio_views, user_profile_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
urlpatterns = [

    path('users', user_views.UserListView.as_view()),
    path('user', user_views.UserDetailView.as_view(), name='user_details'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('userprofile', user_profile_views.UserProfileListView.as_view(), name='profiles'),
    path('userprofile/<id_user>', user_profile_views.UserProfileDetailView.as_view(), name='user_profile'),

    path('event', event_views.EventListView.as_view()),
    path('event/<int:id>', event_views.EventDetailView.as_view(), name="event-details"),
    path('event-before', event_views.EventBeforeCurrentDateListView.as_view(), name="event-before-current-date"),
    path('event-after', event_views.EventAfterCurrentDateListView.as_view(), name="event-after-current-date"),
    path('event/week/<id_week>', event_views.EventFromWeekView.as_view(), name="event-from-week"),

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
    path('event/<int:pk>/unattend', eventattendee_views.UnattendView.as_view(), name="unattend"),

    path('cours', cours_views.ListCoursView.as_view(), name="cours-all"),
    path('cours/<id_cours>', cours_views.CoursDetailView.as_view(), name="cours-detail"),

    path('quarter', quarter_views.ListQuarterView.as_view(), name="quarter-all"),
    path('quarter/<id_quarter>', quarter_views.QuarterDetailView.as_view(), name="quarter-detail"),
    path('quarter/cours/<id_cours>', quarter_views.QuarterFromCoursView.as_view(), name="quarter-from-cours"),

    path('week', week_views.ListWeekView.as_view(), name="week-all"),
    path('week/<id_week>', week_views.WeekDetailView.as_view(), name="week-detail"),
    path('week/quarter/<id_quarter>', week_views.WeekFromQuarterView.as_view(), name="week-from-quarter"),
    path('week/quarter-no-pagination/<id_quarter>', week_views.WeekFromQuarterViewWithoutPagination.as_view(), name="week-from-quarter-without-pagination"),

    path('centreinteres', centreinteres_views.ListCentreInteresView.as_view(), name="centreinteres-all"),
    path('centreinteres/<id_centreinteres>', centreinteres_views.CentreInteresDetailView.as_view(), name="centreinteres-detail"),

    path('objectiu', objectius_view.ListObjectiuView.as_view(), name="objectiu-all"),
    path('objectiu/<id_objectiu>', objectius_view.ObjectiuDetailView.as_view(), name="objectiu-detail"),
    path('objectiu/centreinteres/<id_centreinteres>', objectius_view.ObjectiuFromCentreInteresView.as_view(), name="objectiu-from-centreinteres"),
    path('objectiu/centreinteres-no-pagination/<id_centreinteres>', objectius_view.ObjectiuFromCentreInteresWithoutPaginationView.as_view(), name="objectiu-from-centreinteres"),

    path('explicacio', explicacio_views.ListExplicacioView.as_view(), name="objectiu-all"),
    path('explicacio/<id_explicacio>', explicacio_views.ExplicacioDetailView.as_view(), name="objectiu-detail"),
    path('explicacio/centreinteres/<id_centreinteres>', explicacio_views.ExplicacioFromCentreInteresView.as_view(), name="objectiu-from-centreinteres"),
    path('explicacio/centreinteres-no-pagination/<id_centreinteres>', explicacio_views.ExplicacioFromCentreInteresWithoutPaginationView.as_view(), name="objectiu-from-centreinteres"),
]