# voluntariapp/urls.py
from django.urls import path
from voluntariapp.views_directory import user_views, event_views, forum_views, comment_views, rate_views, \
                                        eventattendee_views, course_views, quarter_views, week_views, \
                                        centreinteres_views, goals_views, schedule_views, user_profile_views
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
    path('event/new', event_views.EventCreateView.as_view()),
    path('event/<int:id>', event_views.EventDetailView.as_view(), name="event-details"),
    path('event-before', event_views.EventBeforeCurrentDateListView.as_view(), name="event-before-current-date"),
    path('event-after', event_views.EventAfterCurrentDateListView.as_view(), name="event-after-current-date"),
    path('event/week/<id_week>', event_views.EventFromWeekView.as_view(), name="event-from-week"),

    path('forum', forum_views.ForumThemeListView.as_view(), name="forum"),
    path('forum/<int:id>', forum_views.ForumThemeDetailView.as_view(), name="forumtheme-detail"),

    path('comment', comment_views.ListCommentView.as_view(), name="comments-all"),
    path('comment/<int:id>', comment_views.CommentDetailView.as_view(), name="comments-detail"),
    path('comment/forum/<id_forumtheme>', comment_views.CommentFromThemeView.as_view(), name="comments-from-theme"),

    path('rate', rate_views.ListRateView.as_view(), name="rate-all"),
    path('rate/<id_rate>', rate_views.RateDetailView.as_view(), name="rate-detail"),
    path('rate/event/<id_event>', rate_views.RateFromEventView.as_view(), name="rate-from-event"),

    path('eventattendee', eventattendee_views.ListEventAttendeeView.as_view(), name="eventattendee-all"),
    path('event/<id_event>/attendee', eventattendee_views.AttendeeView.as_view(), name="eventattendee-detail"),
    path('event/<int:pk>/unattend', eventattendee_views.UnattendView.as_view(), name="unattend"),

    path('course', course_views.ListCourseView.as_view(), name="course-all"),
    path('course/<int:id>', course_views.CourseDetailView.as_view(), name="course-detail"),

    path('quarter', quarter_views.ListQuarterView.as_view(), name="quarter-all"),
    path('quarter/<id_quarter>', quarter_views.QuarterDetailView.as_view(), name="quarter-detail"),
    path('quarter/course/<id_course>', quarter_views.QuarterFromCoursView.as_view(), name="quarter-from-cours"),

    path('week', week_views.ListWeekView.as_view(), name="week-all"),
    path('week/<id_week>', week_views.WeekDetailView.as_view(), name="week-detail"),
    path('week/quarter/<id_quarter>', week_views.WeekFromQuarterView.as_view(), name="week-from-quarter"),
    path('week/quarter-no-pagination/<id_quarter>', week_views.WeekFromQuarterViewWithoutPagination.as_view(), name="week-from-quarter-without-pagination"),

    path('centreinteres', centreinteres_views.ListCentreInteresView.as_view(), name="centreinteres-all"),
    path('centreinteres/<int:id>', centreinteres_views.CentreInteresDetailView.as_view(), name="centreinteres-detail"),

    path('goal', goals_views.ListGoalView.as_view(), name="goal-all"),
    path('goal/<int:id>', goals_views.GoalDetailView.as_view(), name="goal-detail"),
    path('goal/centreinteres/<id_centreinteres>', goals_views.GoalFromCentreInteresView.as_view(), name="goal-from-centreinteres"),
    path('goal/centreinteres-no-pagination/<id_centreinteres>', goals_views.GoalFromCentreInteresWithoutPaginationView.as_view(), name="goal-from-centreinteres-no-pagination"),

    path('schedule', schedule_views.ListScheduleView.as_view(), name="schedule-all"),
    path('schedule/<id_schedule>', schedule_views.ScheduleDetailView.as_view(), name="schedule-detail"),
    path('schedule/centreinteres/<id_centreinteres>', schedule_views.ScheduleFromCentreInteresView.as_view(), name="schedule-from-centreinteres"),
    path('schedule/centreinteres-no-pagination/<id_centreinteres>', schedule_views.ScheduleFromCentreInteresWithoutPaginationView.as_view(), name="schedule-from-centreinteres-no-pagination"),
]