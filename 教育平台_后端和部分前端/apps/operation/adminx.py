__author__ = 'Vincent'

import xadmin

from .models import UserAsk,UserCourse,UserFavorite,UserMessage,CourseComments

class UserAskAdmin(object):

    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']




class UserCourseAdmin(object):
    list_display = ['user', 'course',  'add_time']
    search_fields = ['user', 'course']
    list_filter =  ['user', 'course',  'add_time']




class UserFavoriteAdimn(object):
    list_display = ['user', 'fav_id','Fav_type','add_time']
    search_fields = ['user', 'fav_id','Fav_type']
    list_filter =  ['user', 'fav_id','Fav_type','add_time']




class UserMessageAdmin(object):
    list_display = ['user', 'message','has_read','add_time']
    search_fields = ['user', 'message','has_read']
    list_filter =  ['user', 'message','has_read','add_time']



class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']




xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdimn)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)