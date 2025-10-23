from django.contrib import admin
from .models import Slip, SlipQuestion, ClassList, ExploreTopic, Profile, CommunityThread, CommunityReply
from .models import Slip, SlipQuestion, ClassList, ExploreTopic, Profile, CommunityThread, CommunityReply, Bookmark
# Register your models here.

class SlipAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_name', 'year', 'sem', 'uploaded_by', 'created_at')
    list_filter = ('class_name', 'year', 'sem')
    search_fields = ('title', 'class_name__class_name', 'year', 'sem')

class SlipQuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'slip', 'verified', 'question_text', 'solution_text', 'output', 'marks')
    list_filter = ('slip__class_name__class_name', 'slip__year', 'slip__sem', 'subject', 'verified')
    search_fields = ('subject', 'question_text', 'solution_text', 'explanation', 'output', 'marks')
    raw_id_fields = ('slip',)

class ExploreTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    list_filter = ('category', )
    search_fields = ('title', 'description', 'category')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'department', 'year')
    list_filter = ('department', 'year')
    search_fields = ('user__username', 'student_id', 'department', 'year')


class CommunityThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_solved', 'upvotes', 'views', 'created_at')
    list_filter = ('category', 'is_solved', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'author__first_name', 'author__last_name')
    raw_id_fields = ('author',)

class CommunityReplyAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'is_solution', 'upvotes', 'created_at')
    list_filter = ('is_solution', 'created_at')
    search_fields = ('content', 'author__username', 'thread__title')
    raw_id_fields = ('thread', 'author')

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content_type', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username', 'title', 'content_type')
    raw_id_fields = ('user',)

admin.site.register(Slip, SlipAdmin)
admin.site.register(SlipQuestion, SlipQuestionAdmin)
admin.site.register(ClassList)
admin.site.register(ExploreTopic, ExploreTopicAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CommunityThread, CommunityThreadAdmin)
admin.site.register(CommunityReply, CommunityReplyAdmin)
admin.site.register(Bookmark, BookmarkAdmin)