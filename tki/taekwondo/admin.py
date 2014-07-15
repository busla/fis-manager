from django.contrib import admin
from django.contrib.comments import Comment
from django_summernote.admin import SummernoteModelAdmin
from taekwondo.models import *

class TournamentCategoryItemInline(admin.TabularInline):
    model = TournamentCategoryItem

class TournamentResultInline(admin.TabularInline):
    model = TournamentResult

class PointSystemItemInline(admin.TabularInline):
    model = PointSystemItem

class PointSystemAdmin(admin.ModelAdmin):
    inlines = [PointSystemItemInline]
    list_display = ('title', 'description')

class TournamentCategoryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_type')

class TournamentRegistrationInline(admin.TabularInline):
    model = TournamentRegistration
    exclude = ('membership',)

class TournamentRegistrationAdmin(admin.ModelAdmin):
    inlines = [TournamentResultInline]
    list_display = ('member', 'tournament')

class TournamentResultAdmin(admin.ModelAdmin):
    search_fields = ['registration']
    list_display = ('registration', 'rank')

class ResultRankAdmin(admin.ModelAdmin):
    list_display = ('title', 'rank')

class ResultRankInline(admin.TabularInline):
    model = TournamentResult
    

class TournamentFileInline(admin.TabularInline):
    model = TournamentFile

class TournamentDivisionInline(admin.TabularInline):
    model = TournamentDivision

class ClubFileInline(admin.TabularInline):
    model = ClubFile

class MembershipInline(admin.TabularInline):
    model = Membership

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'club', 'date_joined', 'date_left')
    
class TournamentAdmin(admin.ModelAdmin):
    inlines = [TournamentFileInline, TournamentRegistrationInline, TournamentDivisionInline]
    prepopulated_fields = {"slug": ("title",)}

class ClubAdmin(SummernoteModelAdmin):
    inlines = [ClubFileInline]
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'felix_members')

class MemberAdmin(SummernoteModelAdmin):
    inlines = [MembershipInline]
    list_display = ('name', 'active_club')
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    
class NewsAdmin(SummernoteModelAdmin):
    model = News
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Club, ClubAdmin)
admin.site.register(PointSystem, PointSystemAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentRegistration, TournamentRegistrationAdmin)
admin.site.register(TournamentResult, TournamentResultAdmin)
admin.site.register(TournamentCategoryItem, TournamentCategoryItemAdmin)
admin.site.register(ResultRank, ResultRankAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(News, NewsAdmin)