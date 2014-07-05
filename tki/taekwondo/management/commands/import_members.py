from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option
from taekwondo.models import Club, Member, Membership, Tournament, News
import csv, os

class Command(BaseCommand):
    help = 'Imports Taekwondo members from a Felix CSV file.'
    
    option_list = BaseCommand.option_list + (
        make_option(
            "-f", 
            "--file", 
            dest = "filename",
            help = "specify import file", 
            metavar = "FILE"
        ),
    )
    
    def handle(self, *args, **options):
        if options['filename'] == None :
            raise CommandError("Option `--file=...` must be specified.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']) :
            raise CommandError("File does not exist at the specified path.")

        
        students = csv.reader(open(options['filename']))


        for student in students:
            m = Member(name = student[1], ssn=student[2], slug=slugify(student[1]))
            m.save()
        
        self.stdout.write('Successfully imported members from "%s"' % options['filename'])


