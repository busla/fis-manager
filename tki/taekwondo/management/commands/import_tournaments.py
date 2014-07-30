
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option
import argparse
from taekwondo.models import *
import csv, os
from datetime import datetime    
from unidecode import unidecode

class Command(BaseCommand):

    help = 'Imports Taekwondo tournament from a tournament-result CSV file.'
    #club_list = list(Club.objects.all())
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
        print('Trying to create membership using %s and %s' % (m.active_club, c.name))
        
        if str(m.active_club) == c.name:
        #Membership.objects.filter(member=_member.pk, club__name=_member.active_club).exists():        
            print(m.name + ' is already registered at ' + c.name)
        else:
            ms = Membership(member=m, club_id=int(c.id), date_joined=datetime.now())
            ms.save()
            print(m.name + ' is now a member of ' + c.name)

    def fight_import(self, item):
        #print(self.club_list)
        tournament_list = list(Tournament.objects.all())
        tournament_exists = False

        fight_info =  {
            'tournament_name': item[0],
            'fight_number': item[1],
            'age_division': item[2],
            'belt_group': item[3],
            'weight_group': item[4],
            'gender': item[5],
            'red_club': item[6],
            'blue_club': item[7],
            'red_player': item[8],
            'blue_player': item[9],
            'red_points': item[10],
            'blue_points': item[10],
        }
        '''
        _tournament_name = item[0]
        _match_number = item[1]
        _age_division = item[2]
        _belt_group = item[3]
        _weight_group = item[4]
        _gender = item[5]
        _red_club = item[6]
        _blue_club = item[7]
        _red_player = item[8]
        _blue_player = item[9]
        _red_points = item[10]
        _blue_points = item[11]
        '''
        for listed_tournament in tournament_list:
            if listed_tournament.title in fight_info.get('tournament_name'):
                tournament_exists = True
                tournament_obj = listed_tournament
        

        '''            
        m = Match(pk=_felix_ssn, address=_address, name=_felix_member, slug=slugify(unidecode(_felix_member)))
        m.save()
        #self.stdout.write(m.name + ' active club is: ' + str(m.active_club))
        '''
                

        if tournament_exists:
            print('The tournament "%s" already exists, adding fight now ... ' % (fight_info.get('tournament_name')))

            tournament_age_division, created = TournamentCategoryItem.objects.get_or_create(
                category_type=1,
                title=fight_info.get('age_division')
                )

            tournament_weight_group, created = TournamentCategoryItem.objects.get_or_create(
                category_type=2,
                title=fight_info.get('weight_group')
                )

            tournament_belt_group, created = TournamentCategoryItem.objects.get_or_create(
                category_type=3,
                title=fight_info.get('belt_group')
                )

            division, created = TournamentDivision.objects.get_or_create(
                title='%s - %s - %s' % (
                    tournament_age_division.title,
                    tournament_weight_group.title,
                    tournament_belt_group.title,
                    ),
                tournament=tournament_obj,
                age = tournament_age_division,
                weight = tournament_weight_group,
                grade = tournament_belt_group,
                gender = 1
                )


            
            fight, created = Fight.objects.get_or_create(
                    division = division,
                    fight_number=fight_info.get('fight_number'),
                    blue_player=fight_info.get('blue_player'), 
                    red_player=fight_info.get('red_player'),
                    blue_points=fight_info.get('blue_points'),
                    red_points=fight_info.get('red_points'),
                    )
            

                    

        elif not tournament_exists:
            print('A tournament with the title "%s" does not exist, creating it now.... ' % fight_info.get('tournament_name'))
            new_tournament = Tournament(title=fight_info.get('tournament_name'), date=datetime.now(), slug=slugify(unidecode(fight_info.get('tournament_name'))))
            new_tournament.save()
            
            
                
        #self.create_membership(m, c)
        
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

                
        csv_fights = csv.reader(open(options['filename'], newline=''), delimiter=';')
        for i, row in enumerate(csv_fights):
            print(row)
            self.fight_import(row)
    