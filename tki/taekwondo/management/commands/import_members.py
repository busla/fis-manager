# -*- coding: ISO-8859-1 -*-
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option
from taekwondo.models import Club, Member, Membership, Tournament, News
import csv, os
from datetime import datetime    


class Command(BaseCommand):
    missing_clubs = set()
    help = 'Imports Taekwondo members from a Felix CSV file.'
    club_list = list(Club.objects.all())
    option_list = BaseCommand.option_list + (
        make_option(
            "-f", 
            "--file", 
            dest = "filename",
            help = "specify import file", 
            metavar = "FILE"
        ),
    ) 
    
    def create_membership(self, m, c):
        if str(m.active_club) == c.name:

        #Membership.objects.filter(member=_member.pk, club__name=_member.active_club).exists():        
            print(m.name + ' is already registered at ' + c.name)
        else:
            ms = Membership(member=m, club_id=int(c.id), date_joined=datetime.now())
            ms.save()
            print(m.name + ' is now a member of ' + c.name)

    def felix_import(self, _felix_ssn, _felix_member, _felix_club):
        #print(self.club_list)
        club_exists = False
        m = Member(pk=_felix_ssn, name=_felix_member, slug=slugify(_felix_member))
        m.save()
        #self.stdout.write(m.name + ' active club is: ' + str(m.active_club))
        
        for item in self.club_list:
            if item.name in _felix_club:
                club_exists = True

        if club_exists:
            print('The club "%s" already exists, creating membership now... ' % _felix_club)
            for item in self.club_list:
                if item.name in _felix_club:
                    c = item
                    

        else:
            print('The club "%s" does not exist, creating it now.... ' % _felix_club)
            c = Club(name=_felix_club, slug=slugify(_felix_club))
            c.save()
            
            
                
        self.create_membership(m, c)
        
    def handle(self, *args, **options):

        if options['filename'] == None :
            raise CommandError("Option `--file=...` must be specified.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']) :
            raise CommandError("File does not exist at the specified path.")

        
        students = csv.reader(open(options['filename']))


        for i, student in enumerate(students):
            self.felix_import(student[2], student[1], student[3])
            
            #m = Member(name = student[1], ssn=student[2], slug=slugify(student[1]))
            #m.save()
        if self.missing_clubs:
            print('Missing clubs: ' + self.missing_clubs)
            
        print('Successfully imported %s members from "%s"' % (i, options['filename']))


