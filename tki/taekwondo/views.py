from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from taekwondo.models import *
from django.http import HttpResponse
from django.db.models import Q

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

class ClubList(ListView):
    model = Club
    context_object_name = 'club_list'

class ClubDetail(DetailView):
    queryset = Club.objects.select_related('members').all()
    context_object_name = 'club_detail'

class FightList(ListView):

    template_name = 'taekwondo/member_detail.html'
    def get_queryset(self):
        self.member = get_object_or_404(Member, slug=self.kwargs['slug'])
        self.fights = Fight.objects.filter(Q(red_player__member=self.member) | Q(blue_player__member=self.member))
        #self.fights = Fight.objects.filter(blue_player__member=self.member)
        #self.fights = Fight.objects.all()
        return self.fights

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FightList, self).get_context_data(**kwargs)
        # Add in the publisher
        context['fight_list'] = self.fights
        return context

    #queryset = Fight.objects.all()
    #context_object_name = 'fight_list'
'''
class FightList(ListView):
    template_name = 'taekwondo/member_detail.html'
    model = Fight
    context_object_name = 'fight_list'

'''

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


