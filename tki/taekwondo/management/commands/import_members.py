
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option
import argparse
from taekwondo.models import Club, Member, Membership, Tournament, News
import csv, os
from datetime import datetime    
from unidecode import unidecode

class Command(BaseCommand):
    csv_header = [
        'Nafn', 
        'Kennitala', 
        'Fæðingard.', 
        'Aldur', 
        'Hópur', 
        'Hópaslóð', 
        'Virkni', 
        'Heimilisfang', 
        'Póstfang', 
        'Land', 
        'Sími', 
        'Netfang', 
        'Upplýsingadálkur 1', 
        'Upplýsingadálkur 2', 
        'Upplýsingadálkur 3', 
        'Nafn forráðamanns', 
        'Kt. forráðam.', 
        'Sími forráðam.',
        ]
    
        

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
        make_option(
            "--felix", 
            dest = "felix",
            help = "'new' or 'old' Felix version", 
            metavar = "STRING"
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
        _club_list = list(Club.objects.all())
        club_exists = False
        m = Member(pk=_felix_ssn, name=_felix_member, slug=unidecode(_felix_member))
        m.save()
        #self.stdout.write(m.name + ' active club is: ' + str(m.active_club))
        
        for item in _club_list:
            if item.name in _felix_club:
                club_exists = True
                

        if club_exists:
            print('The club "%s" already exists, creating membership now... ' % _felix_club)
            for item in _club_list:
                if item.name in _felix_club:
                    c = item
                    

        elif not club_exists:
            print('The club "%s" does not exist, creating it now.... ' % _felix_club)
            c = Club(name=_felix_club, slug=unidecode(_felix_club))
            c.save()
            
            
                
        self.create_membership(m, c)
    
    #def felix2_import(self):
    def get_club(self, club):
        if not 'ÍSÍ' in club:
            print('Fann ekki félag í línunni: ' + club)
        return club.split('/')[-3]

    def handle(self, *args, **options):

        if options['filename'] == None :
            raise CommandError("Option `--file=...` must be specified.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']) :
            raise CommandError("File does not exist at the specified path.")

        if options['felix'] == None :
            raise CommandError("Option `--felix=...` must be specified (1/2).")
        
        elif options['felix'] == '1' :
            students = csv.reader(open(options['filename']))
            for i, student in enumerate(students):
                self.felix_import(student[2], student[1], student[3])

        elif options['felix'] == '2':
            start_matrix = False
            #with open(options['filename'], newline='', encoding='ISO-8859-1') as felix_file:
            felix_lines = csv.reader(open(options['filename'], encoding='ISO-8859-1', newline=''), delimiter=';')
            for i, row in enumerate(felix_lines):
                #self.felix2_import(row[0])
                
                
                if start_matrix:
                    print('%s, %s, %s' % (row[1].replace("-",''), row[0], self.get_club(row[5])))
                    self.felix_import(row[1].replace("-",''), row[0], self.get_club(row[5]))

                if not start_matrix:
                    if (set(row) == set(self.csv_header)):
                        start_matrix = True
                        print('This is our header:' + str(row))





            #students = csv.reader(open(options['filename']))
            
            #m = Member(name = student[1], ssn=student[2], slug=slugify(student[1]))
            #m.save()
            
        print('Successfully imported %s members from "%s"' % (i, options['filename']))


