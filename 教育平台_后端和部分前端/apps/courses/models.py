from django.db import models
from datetime import datetime

from organization.models import CourseOrg,Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE,verbose_name="所属机构",null=True, blank=True)
    name = models.CharField(max_length=50,verbose_name="课程名")
    desc = models.CharField(max_length=300,verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(verbose_name="难度",choices=(("cj","初级"),("zj","中级"),("gj","高级")),max_length=2)
    learn_time = models.IntegerField(default=0,verbose_name="学习时长（分钟数）")
    students = models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m",verbose_name="封面",max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")
    category = models.CharField('课程类别',max_length=20,default="")
    tag = models.CharField('课程标签',default='',max_length=10)
    teacher = models.ForeignKey(Teacher,verbose_name='讲师',null=True,blank=True,on_delete=models.CASCADE)
    youneed_know = models.CharField('课程须知',max_length=300,default='')
    teacher_tell = models.CharField('老师告诉你',max_length=300,default='')

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程的章节数
        return self.lesson_set.all().count()

    def get_learn_users(self):
        # 获取这门课程的学习用户
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        #获取课程章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="课程")
    name = models.CharField(max_length=100,verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_lesson_vedio(self):
        #获取章节所有视频
        return self.video_set.all()

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField('访问地址',default='',max_length=200)
    learn_times = models.IntegerField("学习时长(分钟数)", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="课程")
    name = models.CharField(max_length=100,verbose_name="视频名")
    download = models.FileField(upload_to="course/resource/%Y/%m",verbose_name="资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name



