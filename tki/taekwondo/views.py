from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from taekwondo.models import *
from django.http import HttpResponse
from django.db.models import Q


from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from taekwondo.serializers import MemberSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def member_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)        

@csrf_exempt
def member_detail(request, slug):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        member = Member.objects.get(slug=slug)
    except Member.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MemberSerializer(member)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(member, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        member.delete()
        return HttpResponse(status=204)

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


