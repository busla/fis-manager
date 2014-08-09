from django.forms import widgets
from rest_framework import serializers
from taekwondo.models import *

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('name', 'slug', 'ssn', 'photo', 'address')