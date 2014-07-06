# -*- coding: ISO-8859-1 -*-
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option
from taekwondo.models import Club, Member, Membership, Tournament, News
import csv, os
from datetime import datetime    


class Command(BaseCommand):
    help = 'Imports Taekwondo members from a Felix CSV file.'
    club_list = Club.objects.values('id', 'name')
    option_list = BaseCommand.option_list + (
        make_option(
            "-f", 
            "--file", 
            dest = "filename",
            help = "specify import file", 
            metavar = "FILE"
        ),
    ) 
    def felix_import(self, _ssn, _name, _club):
        for value in self.club_list.values('id', 'name'):
            if _club in list(value.values()):
                c = Club.objects.get(pk=int(list(value.values())[0]))
                m = Member(name=_name, pk=_ssn)
                m.save()
                
                #ms = Membership(member=m, club=c, date_joined=datetime.now(), date_left=datetime.now())
                ms = Membership(member=m, club=c)
                ms.save()
                return self.stdout.write('Saved to db: %s' % _club)
            else: 
                _missing_club = _club
        
        self.stdout.write('Club does not exit: %s, adding now...' % _club)
        c = Club(name=_missing_club)
        c.save()


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
            
        self.stdout.write('Successfully imported %s members from "%s"' % (i, options['filename']))


