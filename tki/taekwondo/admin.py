from django.contrib import admin
from django.contrib.comments import Comment
from django_summernote.admin import SummernoteModelAdmin
from taekwondo.models import Club, Tournament, Member, Membership, TournamentFile, ClubFile, News


class TournamentFileInline(admin.TabularInline):
    model = TournamentFile

class ClubFileInline(admin.TabularInline):
    model = ClubFile

class MembershipInline(admin.TabularInline):
    model = Membership
    
class TournamentAdmin(admin.ModelAdmin):
    inlines = [TournamentFileInline]
    prepopulated_fields = {"slug": ("title",)}

class ClubAdmin(SummernoteModelAdmin):
    inlines = [ClubFileInline]
    prepopulated_fields = {"slug": ("name",)}

class MemberAdmin(SummernoteModelAdmin):
    inlines = [MembershipInline]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    
class NewsAdmin(SummernoteModelAdmin):
    model = News
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Club, ClubAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Membership)
admin.site.register(Member, MemberAdmin)
admin.site.register(News, NewsAdmin)