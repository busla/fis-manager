from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from taekwondo.models import *
from django.http import HttpResponse
from django.db.models import Q, Count, Min, Sum, Avg

# REST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taekwondo.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics

# Browsable API
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import viewsets

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'tournaments': reverse('tournament-list', request=request, format=format),
        'members': reverse('member-list', request=request, format=format),
        #'fights': reverse('fight-list', request=request, format=format),
        'clubs': reverse('club-list', request=request, format=format),
        
    })


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class ApiFightList(generics.ListCreateAPIView):
    """
    Birta alla bardaga eða bæta við nýjum bardaga.
    """
    queryset = Fight.objects.all()
    serializer_class = FightSerializer
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class ApiFightDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Sækja, uppfæra eða eyða móti.
    """
    queryset = Fight.objects.all()
    serializer_class = FightSerializer     


class ApiTournamentList(generics.ListCreateAPIView):
    """
    Birta öll mót eða bæta við nýju móti.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class ApiTournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Sækja, uppfæra eða eyða móti.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer     

class ApiMemberList(generics.ListCreateAPIView):
    """
    Birta alla iðkendur eða bæta við nýjum iðkanda.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class ApiMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Sækja, uppfæra eða eyða iðkanda.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer     

class ApiClubList(generics.ListCreateAPIView):
    """
    Birta öll félög eða bæta við nýju félagi.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

class ApiClubDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Sækja, uppfæra eða eyða félagi.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer  


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


class RankList(ListView):

    template_name = 'taekwondo/rank_list.html'
    def get_queryset(self):
        self.rank_list = Member.objects.annotate(player=Count('tournamentregistration__winner')).order_by('-player')
        
        #self.fights = Fight.objects.filter(blue_player__member=self.member)
        #self.fights = Fight.objects.all()
        return self.rank_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RankList, self).get_context_data(**kwargs)
        # Add in the publisher
        context['rank_list'] = self.rank_list
        return context

    #queryset = Fight.objects.all()
    #context_object_name = 'fight_list'

class RankList2(ListView):

    template_name = 'taekwondo/rank_list.html'
    def get_queryset(self):
        self.rank_list = Member.objects.annotate(player=Count('tournamentregistration__winner')).order_by('-player')
        
        #self.fights = Fight.objects.filter(blue_player__member=self.member)
        #self.fights = Fight.objects.all()
        return self.rank_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RankList, self).get_context_data(**kwargs)
        # Add in the publisher
        context['rank_list'] = self.rank_list
        return context

    #queryset = Fight.objects.all()
    #context_object_name = 'fight_list'

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


