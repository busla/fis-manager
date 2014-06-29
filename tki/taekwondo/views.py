from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from taekwondo.models import Club, Member, Membership, Tournament
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

class ClubList(ListView):
    model = Club
    context_object_name = 'club_list'

class ClubDetail(DetailView):
    queryset = Club.objects.select_related('members').all()
    context_object_name = 'club_detail'
