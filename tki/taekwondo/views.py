from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from taekwondo.models import Club, Member, Membership, Tournament, News
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

class ClubList(ListView):
    model = Club
    context_object_name = 'club_list'

class ClubDetail(DetailView):
    queryset = Club.objects.select_related('members').all()
    context_object_name = 'club_detail'

class TournamentList(ListView):
    model = Tournament
    context_object_name = 'tournament_list'

class TournamentDetail(DetailView):
    queryset = Tournament.objects.all()
    context_object_name = 'tournament_detail'

class NewsList(ListView):
    queryset = News.objects.all()
    context_object_name = 'news_list'

class NewsDetail(DetailView):
    queryset = News.objects.all()
    context_object_name = 'news_detail'