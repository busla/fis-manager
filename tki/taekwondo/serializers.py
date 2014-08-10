from django.forms import widgets
from rest_framework import serializers
from taekwondo.models import *

class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='tournament-detail', format='html')

    class Meta:
        model = Tournament
        fields = ('id', 'title', 'image', 'description', 'date', 'slug', 'point_system', 'competitors', 'url')
    

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='member-detail', format='html')

    class Meta:
        model = Member
        fields = ('id', 'name', 'slug', 'ssn', 'photo', 'address', 'url')

class FightSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='fight-detail', format='html')

    class Meta:
        model = Fight
        fields = ('id', 'fight_number', 'division', 'blue_player', 'red_player', 'blue_points', 'red_points', 'winner', 'url')

class ClubSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='club-detail', format='html')

    class Meta:
        model = Club
        fields = ('id','name', 'short_name', 'slug', 'description', 'logo', 'email', 'website', 'url')

    fight_number = models.IntegerField(blank=True, null=True)
    division = models.ForeignKey(TournamentDivision, blank=True, null=True)
    blue_player = models.ForeignKey(TournamentRegistration, related_name='blue_player')
    red_player = models.ForeignKey(TournamentRegistration, related_name='red_player')
    blue_points = models.IntegerField(blank=True, null=True)
    red_points = models.IntegerField(blank=True, null=True)
    winner = models.ForeignKey(TournamentRegistration, blank=True, null=True, related_name='winner')        