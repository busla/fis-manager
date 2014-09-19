from django.db import models
from django.db.models import permalink, Count, Q
from django.core.exceptions import ObjectDoesNotExist
from taekwondo import slug
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager

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

class TaekwondoUserManager(BaseUserManager):
    def create_user(self, email, ssn, password=None):
        if not email:
            raise ValueError('Users must have an email address')
 
        if not ssn:
            raise ValueError('Users must have a social security number')

        user = self.model(
            email=TaekwondoUserManager.normalize_email(email),
            ssn=ssn,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, ssn, password):
        user = self.create_user(email,
            password=password,
            ssn=ssn
        )
        user.is_admin = True
        user.save(using=self._db)
        return user    

 
class TaekwondoUser(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(max_length=254, unique=True)
    ssn = models.CharField(max_length=11, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = TaekwondoUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['ssn']

    def get_full_name(self):
        # For this case we return email. Could also be User.first_name User.last_name if you have these fields
        return self.email
 
    def get_short_name(self):
        # For this case we return email. Could also be User.first_name if you have this field
        return self.email
 
    def __unicode__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True
 
    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin
    

class Member(models.Model):
    
    name = models.CharField(max_length=200)
    ssn = models.CharField(max_length=11, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to='members/photos', height_field=None, width_field=None, max_length=100, blank=True)
    slug = models.SlugField(unique=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def _get_fights(self):
        fights = Fight.objects.filter(
            Q(red_player__member=self) | 
            Q(blue_player__member=self)
        )
        return fights

    all_fights = property(_get_fights)

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

    
    def save(self, **kwargs):
        slug.unique_slugify(self, self.slug)
        super(Member, self).save()
    
    
    def __str__(self):
        return '%s' % self.name


        #obj, created = self.membership_set.get_or_create(name=_name, pk=_ssn, club__
        #          defaults={'birthday': date(1940, 10, 9)})


class Club(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    short_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='clubs/logos', height_field=None, width_field=None, max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    website = models.URLField(blank=True, null=True)
    members = models.ManyToManyField(Member, through='Membership', related_name='members')
    slug = models.SlugField(unique=True)
    coaches = models.ManyToManyField(Member, through='CoachMeta')

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

# Coach joined date to club
class CoachMeta(models.Model):
    club = models.ForeignKey(Club)
    member = models.ForeignKey(Member)    
    joined = models.DateField(blank=True, null=True)

# Training groups within clubs
class ClubGroup(models.Model):
    title = models.CharField(max_length=200)
    age_min = models.IntegerField(blank=True, null=True)
    age_max = models.IntegerField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    club = models.ForeignKey(Club)

    def __str__(self):
        return '%s (%s)' % (self.title, self.date_from)

class Membership(models.Model):    
    club = models.ForeignKey(Club)
    member = models.ForeignKey(Member)
    date_joined = models.DateField(blank=True, null=True)
    date_left = models.DateField(blank=True, null=True)
    groups = models.ManyToManyField(ClubGroup, related_name='groups')


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
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return '%s' % self.title


class Tournament(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='tournaments/images/%Y/%m', max_length=100, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    point_system = models.ForeignKey(PointSystem, blank=True, null=True)
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

    def _get_fights(self):
        fights = Fight.objects.filter(division__tournament=self)
        return fights

    fights = property(_get_fights)

    def __str__(self):
        return '%s' % self.title

class TournamentDivision(models.Model):
    title = models.CharField(max_length=200)
    tournament = models.ForeignKey(Tournament)
    age = models.ForeignKey(TournamentCategoryItem, blank=True, null=True, related_name='age')
    weight = models.ForeignKey(TournamentCategoryItem, blank=True, null=True, related_name='weight')
    grade = models.ForeignKey(TournamentCategoryItem, blank=True, null=True, related_name='grade')
    gender = models.IntegerField(choices=GENDER_CHOICES)
    
    def __str__(self):
            return '%s' % self.title

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

    '''
    def save(self):
        _membership = Membership.objects.get(pk = self.member.active_membership)
        self.membership = _membership
        super(TournamentRegistration, self).save()
    '''

    def __str__(self):
        return '%s' % (self.member)


class ResultRank(models.Model):
    title = models.CharField(max_length=200)
    rank = models.IntegerField()

    def __str__(self):
        return '%s - %s' % (self.title, self.rank)


class TournamentResult(models.Model):
    registration = models.ForeignKey(TournamentRegistration, blank=True, null=True) #possibly a legacy
    division = models.ForeignKey(TournamentDivision)
    rank = models.ForeignKey(ResultRank) #note: remove from templates and use the result field
    result = models.ForeignKey(PointSystemItem) #note: add to templates instead of rank

    def __str__(self):
        return '%s - %s' % (self.registration, self.rank)

class Drill(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)

    def __str__(self):
        return '%s' % self.title

class TimeSheet(models.Model):
    date_from = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_to = models.DateTimeField(auto_now=False, auto_now_add=False)
    total_minutes = models.IntegerField(blank=True, null=True)
    drill = models.ManyToManyField(Drill, through='DrillMeta')
    groups = models.ManyToManyField(ClubGroup)
    
    def __str__(self):
        return '%s' % self.date_from

class DrillMeta(models.Model):
    drill = models.ForeignKey(Drill)
    timesheet = models.ForeignKey(TimeSheet)
    minutes = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)

class AttendanceType(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.title

class Attendance(models.Model):
    date = models.DateField(blank=True, null=True)
    club = models.ForeignKey(Club, blank=True, null=True)
    member = models.ManyToManyField(Member, through='AttendanceMeta')

    def __str__(self):
        return '%s - %s' % (self.member, self.date)

class AttendanceMeta(models.Model):
    member = models.ForeignKey(Member)
    attendance = models.ForeignKey(Attendance)
    label = models.ForeignKey(AttendanceType, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.member, self.label)

class BeltExam(models.Model):
    date = models.DateField(blank=True, null=True)
    club = models.ForeignKey(Club, blank=True, null=True)
    member = models.ManyToManyField(Member, through='BeltExamMeta')

    def __str__(self):
        return '%s - %s' % (self.club, self.date)

class BeltExamMeta(models.Model):
    member = models.ForeignKey(Member)
    belt_exam = models.ForeignKey(BeltExam)
    grade = models.IntegerField(blank=True, null=True, choices=GRADE_CHOICES)
    notes = models.TextField(blank=True, null=True)

class GradeRequirement(models.Model):
    title = models.CharField(max_length=200)
    belt_image = models.ImageField(upload_to='grade_requirements/belts/photos', height_field=None, width_field=None, max_length=100, blank=True)
    club = models.ManyToManyField(Club, related_name='club_requirements')
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return '%s' % self.title


class GradeRequirementPhoto(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='grade_requirements/photos', height_field=None, width_field=None, max_length=100, blank=True)
    photo_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.title

class GradeRequirementVideo(models.Model):
    title = models.CharField(max_length=200)
    video = EmbedVideoField()
    photo_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.title

class GradeRequirementItem(models.Model):
    title = models.CharField(max_length=200)
    grade = models.ForeignKey(GradeRequirement)
    photo = models.ManyToManyField(GradeRequirementPhoto, blank=True, null=True, related_name='grade_photo')
    video = models.ManyToManyField(GradeRequirementVideo, blank=True, null=True, related_name='grade_video')
    tags = TaggableManager()

    def __str__(self):
        return '%s' % self.title

    def _get_videos(self):
        q_video = GradeRequirementVideo.objects.filter(grade=self)
        return q_video
    
    videos = property(_get_videos)

class Fight(models.Model):
    fight_number = models.IntegerField(blank=True, null=True)
    division = models.ForeignKey(TournamentDivision, blank=True, null=True)
    blue_player = models.ForeignKey(TournamentRegistration, related_name='blue_player')
    red_player = models.ForeignKey(TournamentRegistration, related_name='red_player')
    blue_points = models.IntegerField(blank=True, null=True)
    red_points = models.IntegerField(blank=True, null=True)
    winner = models.ForeignKey(TournamentRegistration, blank=True, null=True, related_name='winner')

    def __str__(self):
        #return '%s vs. %s (nr: %s)' % (self.red_player, self.blue_player, self.fight_number)
        return '%s' % self.fight_number