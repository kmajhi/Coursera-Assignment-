from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'lesson', 'grade')
    list_filter = ['lesson']
    search_fields = ['question_text']


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'course', 'order')
    list_filter = ['course']
    search_fields = ['title']


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date', 'total_enrollment')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Submission)
