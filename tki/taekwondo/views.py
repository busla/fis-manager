from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from taekwondo.models import *
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

class ClubList(ListView):
    model = Club
    context_object_name = 'club_list'

class ClubDetail(DetailView):
    queryset = Club.objects.select_related('members').all()
    context_object_name = 'club_detail'

class FightList(ListView):
    queryset = Fight.objects.all()
    context_object_name = 'fight_list'

class MemberList(ListView):
    model = Member
    context_object_name = 'member_list'

class MemberDetail(DetailView):
    queryset = Member.objects.all()
    context_object_name = 'member_detail'

class TournamentList(ListView):
    model = Tournament
    context_object_name = 'tournament_list'

class TournamentDetail(DetailView):
    queryset = Tournament.objects.all()
    context_object_name = 'tournament_detail'
'''

    def get_queryset(self):
        self.tournament = Tournament.objects.get(slug=self.kwargs['slug'])
        return self.tournament

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TournamentDetail, self).get_context_data(**kwargs)
        # Add in the publisher
        context['tournament'] = self.tournament
        return context
'''    
class NewsList(ListView):
    queryset = News.objects.all()
    context_object_name = 'news_list'

class NewsDetail(DetailView):
    queryset = News.objects.all()
    context_object_name = 'news_detail'


