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
        fields = ('id', 'name', 'slug', 'photo', 'url')

class FightSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='fight-detail', format='html')

    class Meta:
        model = Fight
        fields = ('id', 'fight_number', 'division', 'blue_player', 'red_player', 'blue_points', 'red_points', 'winner', 'url')

class GradeRequirementItemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='graderequirementitem-detail',
        format='html'
        )

    class Meta:
        model = GradeRequirementItem
        fields = ('id','title', 'title_translated', 'grade', 'photo', 'video', 'order')


class GradeRequirementSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='graderequirement-detail',
        format='html'
        )
    
    grade_items = GradeRequirementItemSerializer(many=True)

    class Meta:
        model = GradeRequirement
        fields = ('id','title', 'belt_image', 'club', 'description', 'slug', 'graderequirementitem_set')

class ClubSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='club-detail',
        format='html'
        )

    grades = GradeRequirementSerializer(many=True)

    class Meta:
        model = Club
        fields = ('id','name', 'short_name', 'slug', 'description', 'logo', 'email', 'website', 'url', 'members', 'club_requirements')



'''
    fight_number = models.IntegerField(blank=True, null=True)
    division = models.ForeignKey(TournamentDivision, blank=True, null=True)
    blue_player = models.ForeignKey(TournamentRegistration, related_name='blue_player')
    red_player = models.ForeignKey(TournamentRegistration, related_name='red_player')
    blue_points = models.IntegerField(blank=True, null=True)
    red_points = models.IntegerField(blank=True, null=True)
    winner = models.ForeignKey(TournamentRegistration, blank=True, null=True, related_name='winner')        
'''