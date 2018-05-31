__author__ = 'Vincent'


from django.urls import path,re_path
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddCommentsView

# 要写上app的名字
app_name = "courses"

urlpatterns = [
    path('list/',CourseListView.as_view(),name='course_list'),
    re_path('courses/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    re_path('info/(?P<course_id>\d+)',CourseInfoView.as_view(),name="course_info"),
    re_path(r'^comment/(?P<course_id>\d+)/',CommentsView.as_view(),name="course_comments"),
    path('add_comment/',AddCommentsView.as_view(),name = "add_comment")
]