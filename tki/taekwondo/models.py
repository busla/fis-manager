from django.db import models
from django.db.models import permalink



class Member(models.Model):
    name = models.CharField(max_length=200)
    ssn = models.CharField(max_length=11, primary_key=True)
    photo = models.ImageField(upload_to='members/photos', height_field=None, width_field=None, max_length=100, blank=True)
    slug = models.SlugField()
    
    def __str__(self):
        return '%s' % self.name

class Club(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='clubs/logos', height_field=None, width_field=None, max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    website = models.URLField()
    members = models.ManyToManyField(Member, through='Membership', related_name='members')
    slug = models.SlugField()
    
    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return '%s' % self.name


class Membership(models.Model):    
    club = models.ForeignKey(Club)
    member = models.ForeignKey(Member)
    date_joined = models.DateField()
    date_left = models.DateField()

    def __str__(self):
        return '%s' % self.member

class Tournament(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='tournaments/images/%Y/%m/%d', max_length=100, blank=True)
    description = models.TextField()
    date = models.DateField()
    slug = models.SlugField()
    
    def __str__(self):
        return '%s' % self.title

class TournamentFile(models.Model):
    attachment = models.FileField(upload_to='tournaments/attachments/%Y/%m/%d', max_length=100, blank=True)
    tournament = models.ForeignKey('Tournament')

class ClubFile(models.Model):
    attachment = models.FileField(upload_to='clubs/attachments/%Y/%m/%d', max_length=100, blank=True)
    club = models.ForeignKey('Club')

class News(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.FileField(upload_to='news/images/%Y/%m/%d', max_length=100, blank=True)
    body = models.TextField()
    posted = models.DateField()

    @permalink
    def get_absolute_url(self):
        return ('view_news_post', None, { 'slug': self.slug })

    def __str__(self):
        return '%s' % self.title

class NewsFile(models.Model):
    attachment = models.FileField(upload_to='news/attachments/%Y/%m/%d', max_length=100, blank=True)
    tournament = models.ForeignKey('News')

