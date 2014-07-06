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
    club_list = Club.objects.all().values('id', 'name')
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
        if str(m.active_club) == c.get('name'):

        #Membership.objects.filter(member=_member.pk, club__name=_member.active_club).exists():        
            self.stdout.write(m.name + ' is already registered at ' + c.get('name'))
        else:
            ms = Membership(member=m, club_id=int(c.get('id')), date_joined=datetime.now())
            ms.save()
            self.stdout.write('Registering ' + m.name + ' to ' + c.get('name'))

    def felix_import(self, _felix_ssn, _felix_member, _felix_club):
        #print(self.club_list)

        m = Member(pk=_felix_ssn, name=_felix_member)
        m.save()
        #self.stdout.write(m.name + ' active club is: ' + str(m.active_club))
        if not _felix_club in self.missing_clubs:
            self.stdout.write('Club does not exist: ' + club.get('name')) 

        for club in self.club_list:
            #print(club.get('name'))
            

            #m = Member.objects.get(pk=int(_ssn))
            if club.get('name') in _felix_club:
                self.create_membership(m, club)
                self.stdout.write('Club name in list: ' + club.get('name'))
                break

            elif club.get('name') not in _felix_club:
                self.stdout.write('Club name not in list: ' + club.get('name')) 
                


            #_club_id = int(value('id')
            #if _club:
                #m = Member(name=_name, pk=_ssn)
                #m.save()
                
                #if not Membership.objects.filter(club__id=_ssn):

                
                #ms = Membership(member=m, club=c)
                #ms.save()
            #print self.stdout.write('Saved to db: %s' % _club)
        
            #self.stdout.write('Club does not exit: %s, adding now...' % _club)
        #c = Club(name=_missing_club)
        #c.save()


        #print(str(c)+_name)
        #m = Membership.objects.create(member__name=_name, club__id=c['id'].get())
        
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
            self.stdout.write('Missing clubs: ' + str(self.missing_clubs))
            
        self.stdout.write('Successfully imported %s members from "%s"' % (i, options['filename']))


