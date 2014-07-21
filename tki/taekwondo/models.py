from django.db import models
from django.db.models import permalink, Count

MALE = 1
FEMALE = 2
GENDER_CHOICES = (
        (MALE, 'Karl'),
        (FEMALE, 'Kona'),
    )

AGE = 1
WEIGHT = 2
GRADE = 3

CATEGORY_CHOICES = (
    (AGE, 'Aldur'),
    (WEIGHT, 'Þyngd'),
    (GRADE, 'Gráða'),
    )

GRADE_CHOICES = (
    (20, '10. geup'),
    (19, '9. geup'),
    (18, '8. geup'),
    (17, '7. geup'),
    (16, '6. geup'),
    (15, '5. geup'),
    (14, '4. geup'),
    (13, '3. geup'),
    (12, '2. geup'),
    (11, '1. geup'),
    (10, '1. dan'),
    (9,  '2. dan'),
    (8,  '3. dan'),
    (7,  '4. dan'),
    (6,  '5. dan'),
    (5,  '6. dan'),
    (4,  '7. dan'),
    (3,  '8. dan'),
    (2,  '9. dan'),
    )

class Member(models.Model):
    
    name = models.CharField(max_length=200)
    ssn = models.CharField(max_length=11, primary_key=True)
    photo = models.ImageField(upload_to='members/photos', height_field=None, width_field=None, max_length=100, blank=True)
    slug = models.SlugField()
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)

    def _get_active_club(self):
        try:
            ac = self.membership_set.all()[0]
        except IndexError:
            ac = None
        return ac
    
    active_club = property(_get_active_club)
    
    def _get_active_membership(self):
        
        ac = Membership.objects.filter(member=self)#self.membership_set.all()[0]
        return ac
    
    active_membership = property(_get_active_membership)
    
    class Meta:
        ordering = ["name"]
    
    def _get_results(self):
        res = TournamentResult.objects.filter(registration__member=self)
        return res
    
    results = property(_get_results)    

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def __str__(self):
        return '%s' % self.name


        #obj, created = self.membership_set.get_or_create(name=_name, pk=_ssn, club__
        #          defaults={'birthday': date(1940, 10, 9)})

class Club(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='clubs/logos', height_field=None, width_field=None, max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    website = models.URLField(blank=True, null=True)
    members = models.ManyToManyField(Member, through='Membership', related_name='members')
    slug = models.SlugField()
    
    class Meta:
        ordering = ["name"]

    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url        

    
    def _felix_members(self):
        q = Membership.objects.filter(club=self).count()
        return q

    felix_members = property(_felix_members)
    def __str__(self):
        return '%s' % self.name


class Membership(models.Model):    
    club = models.ForeignKey(Club)
    member = models.ForeignKey(Member)
    date_joined = models.DateField(blank=True, null=True)
    date_left = models.DateField(blank=True, null=True)

    def __str__(self):
        return '%s' % (self.club)

class PointSystem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s' % self.title

class PointSystemItem(models.Model):
    title = models.CharField(max_length=200)
    points = models.IntegerField(blank=True)
    point_system = models.ForeignKey(PointSystem)

    def __str__(self):
        return '%s' % self.title

class TournamentCategoryItem(models.Model):
    category_type = models.IntegerField(choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    min_value = models.IntegerField()
    max_value = models.IntegerField()


    def __str__(self):
        return '%s' % self.title


class Tournament(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='tournaments/images/%Y/%m', max_length=100, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    slug = models.SlugField()
    point_system = models.ForeignKey(PointSystem)
    competitors = models.ManyToManyField(Member, through='TournamentRegistration', related_name='competitors') 
    

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url    

    def _get_registrations(self):
        regs = TournamentRegistration.objects.filter(tournament=self)
        return regs
    registrations = property(_get_registrations)
    
    def _get_results(self):
        res = TournamentResult.objects.filter(registration__tournament=self)
        return res
    results = property(_get_results)

    def __str__(self):
        return '%s' % self.title

class TournamentDivision(models.Model):
    title = models.CharField(max_length=200)
    tournament = models.ForeignKey(Tournament)
    age = models.ForeignKey(TournamentCategoryItem, blank=True, null=True, related_name='age')
    weight = models.ForeignKey(TournamentCategoryItem, blank=True, null=True, related_name='weight')
    grade = models.ForeignKey(TournamentCategoryItem, blank=True, null=True, related_name='grade')
    gender = models.IntegerField(choices=GENDER_CHOICES)


class TournamentFile(models.Model):
    attachment = models.FileField(upload_to='tournaments/attachments/%Y/%m', max_length=100, blank=True)
    tournament = models.ForeignKey('Tournament')

class ClubFile(models.Model):
    attachment = models.FileField(upload_to='clubs/attachments/%Y/%m', max_length=100, blank=True)
    club = models.ForeignKey('Club')

class News(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.FileField(upload_to='news/images/%Y/%m', max_length=100, blank=True)
    body = models.TextField()
    posted = models.DateField()

    @permalink
    def get_absolute_url(self):
        return ('view_news_post', None, { 'slug': self.slug })

    def __str__(self):
        return '%s' % self.title

class NewsFile(models.Model):
    attachment = models.FileField(upload_to='news/attachments/%Y/%m', max_length=100, blank=True)
    tournament = models.ForeignKey('News')

class TournamentRegistration(models.Model):
    member = models.ForeignKey(Member, blank=True, null=True)
    club = models.ForeignKey(Club, blank=True, null=True)
    membership = models.ForeignKey(Membership, blank=True, null=True)
    tournament = models.ForeignKey(Tournament)
    registration_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    weight = models.IntegerField(blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True, choices=GRADE_CHOICES)

    def age(self): # calculate age from member.ssn
        pass

    def save(self):
        _membership = Membership.objects.get(pk = self.member.active_membership)
        self.membership = _membership
        super(TournamentRegistration, self).save()
    
    def __str__(self):
        return '%s - %s' % (self.member, self.tournament)


class ResultRank(models.Model):
    title = models.CharField(max_length=200)
    rank = models.IntegerField()

    def __str__(self):
        return '%s - %s' % (self.title, self.rank)


class TournamentResult(models.Model):
    registration = models.ForeignKey(TournamentRegistration)
    rank = models.ForeignKey(ResultRank)
    result = models.ForeignKey(PointSystemItem)

    def __str__(self):
        return '%s - %s' % (self.registration, self.rank)
