from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from taekwondo.models import *
from django.http import HttpResponse
from django.db.models import Q, Count, Min, Sum, Avg
import time
from datetime import date

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

class ApiClubDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Sækja, uppfæra eða eyða félagi.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer  

class ApiClubList(generics.ListCreateAPIView):
    """
    Birta öll félög eða bæta við nýju félagi.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ApiGradeRequirementDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Sækja, uppfæra eða eyða félagi.
    """
    
    serializer_class = GradeRequirementSerializer  


class ApiGradeRequirementList(generics.ListCreateAPIView):
    """
    Birta allar beltagráður eða bæta við.
    """
    queryset = GradeRequirement.objects.all()
    serializer_class = GradeRequirementSerializer

class ApiGradeRequirementItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Sækja, uppfæra eða eyða beltakröfu
    """
    serializer_class = GradeRequirementItemSerializer
    
    def get_queryset(self):
        grade = GradeRequirement.object.filter(pk=self.kwargs['pk'])
        return GradeRequirementItem.objects.filter(grade=grade)


def index(request):
    return HttpResponse('Enn að vinna í forsíðunni :-P Smelltu <a href="/felog">hér</a> til að skoða vefinn')

def member_statistics(request):

    def calculate_age(born):
        today = date.today()
        return today.year - born.tm_year - ((today.month, today.tm_mon) < (born.tm_mon, born.tm_mday))

    born = {}
    age_list = []
    members_ssn = Member.objects.values('ssn')

    
    for ssn in members_ssn:
        #print(member.ssn)
        if ssn['ssn']:
            if (len(ssn['ssn']) == 10):

                dob_from_ssn = ssn['ssn'][0:2] + '-' + ssn['ssn'][2:4] + '-' + ssn['ssn'][4:6]

                dob = time.strptime(dob_from_ssn, "%d-%m-%y")
                age_list.append(calculate_age(dob))
        '''    
        if ssn['ssn']:
            if (len(ssn['ssn']) == 10):
                dob = date(int(ssn['ssn'][4:6]), int(ssn['ssn'][2:4]), int(ssn['ssn'][0:2])) 


        if len(ssn == 10):
            born['date'] = member.ssn[0:1]
            born['month'] = member.ssn[2:3]
            born['year'] = member.ssn[4:5]

            dob = date(int(born['year']), int(born['month']), int(born['date']))
            #dob = time.strptime("born['date'] born['month'] born['year']", "%d %m %y")
            #dob = time.strptime("19 08 81", "%d %m %y")
            age_list.append(ssn['ssn'])
        '''
    
    return HttpResponse(dob.tm_year)


class GradeList(ListView):
    template_name = 'taekwondo/grade_list.html'
    def get_queryset(self):
        self.club = get_object_or_404(Club, slug=self.kwargs['slug'])
        self.grade_list = GradeRequirement.objects.filter(club=self.club)
        
        #self.fights = Fight.objects.filter(blue_player__member=self.member)
        #self.fights = Fight.objects.all()
        return self.grade_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GradeList, self).get_context_data(**kwargs)
        # Add in the publisher
        context['grade_list'] = self.grade_list
        context['club_detail'] = self.club
        return context


class ClubDetail(DetailView):
    '''
    
    template_name = 'taekwondo/grade_detail.html'
    model = GradeRequirement
    slug_field = 'slug'
    slug_url_kwarg = 'grade'
    context_object_name = 'grade_detail'
    '''

    template_name = 'taekwondo/club_detail.html'
    def get_queryset(self):
        self.club = Club.objects.filter(slug=self.kwargs['slug'])
        #self.grades = GradeRequirement.objects.filter(club=self.club)
        #self.grade_items = self.grades.objects.all()
        
        #self.fights = Fight.objects.filter(blue_player__member=self.member)
        #self.fights = Fight.objects.all()
        return self.club

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClubDetail, self).get_context_data(**kwargs)
        # Add in the publisher
        #context['grade_detail'] = self.grade_items
        context['club_detail'] = self.club
        return context




class ClubList(ListView):
    model = Club
    context_object_name = 'club_list'

'''
class ClubDetail(DetailView):
    queryset = Club.objects.select_related('members').all()
    context_object_name = 'club_detail'
'''

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


