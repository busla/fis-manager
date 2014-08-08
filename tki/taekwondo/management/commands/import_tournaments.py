
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option
import argparse
from taekwondo.models import *
import csv, os
from datetime import datetime    
from unidecode import unidecode
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import collections

class Command(BaseCommand):

    help = 'Sæki bardaga frá mótum úr CSV skrá frá TKÍ'
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

    def get_fight_info(self, item):
    
        self.fight_info =  (
            ('tournament_name', item[0]),
            ('fight_number', item[1]),
            ('age_division', item[2]),
            ('belt_group', item[3]),
            ('weight_group', item[4]),
            ('gender', item[5]),
            ('red_club', item[6]),
            ('blue_club', item[7]),
            ('red_player', item[8]),
            ('blue_player', item[9]),
            ('red_points', item[10]),
            ('blue_points', item[11]),
        )
        self.fight_info = collections.OrderedDict(self.fight_info)
        return self.fight_info

    def update_csv(self, updated_fight_info):
        updated_csv = self.original_csv.strip('.csv')+'-updated.csv'
        print(list(updated_fight_info.values()))
        with open(updated_csv, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(list(updated_fight_info.values()))

    def compare_members(self, _member, _club):
        selection = {}
        print('Reyni að prenta %s' % _member)
        try:
            member_list = list(Member.objects.filter(name__istartswith=_member.split()[0]))
            print('')
            print('"%s" í félaginu "%s" fannst ekki í FELIX. Var hann skráður með öðru nafni á mótið?' % (_member, _club))
            print('')

            if len(member_list) >= 1:
                print('### Listi með öllum iðkendum úr FELIX með sama fornafn ###')
                #print(member_list)
            else:
                print('### Enginn iðkandi með nafnið "%s" fannst í FELIX ###' % _member)
            
            selection[0] = ['Bæta við "%s" sem nýjum iðkanda' % _member]
            print('%s. %s' % (0, selection.get(0)))
            
            for i, member in enumerate(member_list):
                i = i+1
                selection[i] = [member, member.active_club]
                print('%s. %s - %s' % (i, member.name, member.active_club))
            
            
            while True:
                try:
                    user_input = int(input('Veldu númer: '))
                except ValueError:
                    print('Þetta er ekki tölustafur!')
                else:
                    if 0 <= user_input <= len(member_list):
                        break
                    else:
                        print('Kommon, tölu úr listanum maður!')


        
            if user_input == 0:
                m = Member(name=_member, slug=slugify(unidecode(_member)))
                m.save()
                ms = Membership(member=m, club=_club, date_joined=datetime.now())
                ms.save()

                return m

            else:
                print('Tengi "%s" við "%s"' % (_member, selection.get(user_input)[0]))
                return selection.get(user_input)[0]        

        except IndexError:
                print('Tókst ekki að leita eftir "%s"' % _member.split()[0])
    
    def validate_member(self, _member, _club):
        try:
            m = Member.objects.get(name=_member)
            print('"%s" fannst í FELIX, tengi við færslu.' % _member)
            return m

        except ObjectDoesNotExist:
            print('"%s" fannst ekki, kíkjum aðeins betur á þetta' % _member)
            return self.compare_members(_member, _club)

        except MultipleObjectsReturned:
            print('"%s" fannst oftar en einusinni' % _member)
            

        #rint('%s var búinn til!' % blue_player)
        
            

            

            #user_selection = selection.get(int(user_input))
            
            

            #print(user_selection)
            
            '''
            for i, member in enumerate(member_list):
                if i==int(user_input):
                    return member
                #user_input = input('Uhh, "%s" already exists, continue?' % member)
            '''

    def get_winner(self, red, blue, red_points, blue_points):
        if (int(blue_points) > int(red_points)):
            return blue
        return red

    def fight_import(self, item):
        #print(self.club_list)
        tournament_list = list(Tournament.objects.all())
        tournament_exists = False

        fight_info = self.get_fight_info(item)

        for listed_tournament in tournament_list:
            if listed_tournament.title in fight_info.get('tournament_name'):
                tournament_exists = True
                tournament_obj = listed_tournament
        
                

        if tournament_exists:
            print('Mót með heitinu "%s" er nú þegar til, bæti við bardaga ... ' % (fight_info.get('tournament_name')))

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

            #if not (fight_info.get('red_club')=='' or fight_info.get('red_club')==''):
                
            blue_club, created = Club.objects.get_or_create(
                    slug=slugify(unidecode(fight_info.get('blue_club'))),
                    defaults= {
                        'name': fight_info.get('blue_club'),
                        'short_name': fight_info.get('blue_club'),
                    }
                )
            
            
            red_club, created = Club.objects.get_or_create(
                    slug=slugify(unidecode(fight_info.get('red_club'))),
                    defaults= {
                        'name': fight_info.get('red_club'),
                        'short_name': fight_info.get('red_club'),
                    }

                )


            blue_player = self.validate_member(fight_info.get('blue_player').strip(), blue_club)
            
            #Checking if members exist before adding them to DB
            #member_qs = (Q(Member.objects.filter(name=fight_info.get('blue_player'))) | Q(Member.objects.filter(name=fight_info.get('red_player'))))):
            '''
            blue_player, created = Member.objects.get_or_create(
                    name=fight_info.get('blue_player'),
                    slug=slugify(unidecode(fight_info.get('blue_player'))),
                )
            '''

            #blue_membership = Membership(club=blue_club, member=blue_player)
                
            
            red_player = self.validate_member(fight_info.get('red_player').strip(), red_club)
            
            '''
            red_player, created = Member.objects.get_or_create(
                    name=fight_info.get('red_player'),
                    slug=slugify(unidecode(fight_info.get('red_player'))),
                )
            '''
            blue_registration, created = TournamentRegistration.objects.get_or_create(
                    member=blue_player,
                    tournament=tournament_obj,
                    #club=blue_club,
                    #registration_date=datetime.now()
                ) 
            
            red_registration, created = TournamentRegistration.objects.get_or_create(
                    member=red_player,
                    tournament=tournament_obj,
                    #club=red_club,
                    #registration_date=datetime.now()
                ) 


            
            fight, created = Fight.objects.get_or_create(
                    division = division,
                    fight_number=fight_info.get('fight_number'),
                    blue_player=blue_registration,
                    red_player=red_registration,
                    blue_points=fight_info.get('blue_points'),
                    red_points=fight_info.get('red_points'),
                    winner=self.get_winner(
                        red_registration, 
                        blue_registration, 
                        fight_info.get('red_points'),
                        fight_info.get('blue_points'),
                        )
                )
            fight_info['blue_player'] = blue_player.name
            fight_info['red_player'] = red_player.name
            self.update_csv(fight_info)

        elif not tournament_exists:
            print('Mót með heitinu "%s" er ekki til, bæti því við núna.... ' % fight_info.get('tournament_name'))
            new_tournament = Tournament(
                title=fight_info.get('tournament_name'), 
                date=datetime.now(), 
                slug=slugify(unidecode(fight_info.get('tournament_name')))
                )
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

        self.original_csv = options['filename']
        with open(options['filename'], newline='') as f:
            csv_fights = csv.reader(f, delimiter=';')
        #csv_fights = csv.reader(open(options['filename'], newline=''), delimiter=';')
            for i, row in enumerate(csv_fights):
                print(row)
                if not '' in row:
                    self.fight_import(row)
                else:
                    print('Gat ekki búið til bardaga, upplýsingar vantar í færsluna')
                    print(row)
