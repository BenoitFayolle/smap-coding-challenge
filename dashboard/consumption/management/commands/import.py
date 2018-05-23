from django.core.management.base import BaseCommand, CommandError
from consumption.models import user, consumption_point
from os import path
import pandas as pd
from itertools import islice

class Command(BaseCommand):
    help = 'python manage.py import <path_to_data_folder>   import your data in the application database.'

    def add_arguments(self, parser):
        parser.add_argument('data_path', nargs='+', type=str)
        
    def handle(self, *args, **options):
        data_path_list=options['data_path']
        for data_path in data_path_list:
            if not path.isdir(data_path):
                raise CommandError('path "%s" does not exist' % data_path)    
            if not path.isfile(data_path + "/user_data.csv"):
                raise CommandError('no user_data.csv file in "%s"' % data_path)
            if not path.isdir(data_path + "/consumption"):
                raise CommandError('no consumption directory in ' + data_path + "consumption")
            self.stdout.write(self.style.SUCCESS('all files and directory found!'))
            
            user_raw= pd.read_csv(data_path + "/user_data.csv")
            for i in range(0,user_raw.shape[0]):
                u=user(user_id=user_raw.loc[i,'id'],
                        area=user_raw.loc[i,'area'],
                       tariff=user_raw.loc[i,'tariff'])
                cons_file = data_path + "/consumption/" + str(user_raw.loc[i,'id']) + '.csv'
                if not path.isfile(cons_file):
                    raise CommandError('no consumption file for user id "%s"' % str(user_raw.loc[i,'id']))
                ###consumption data for user i
                consumption_raw = pd.read_csv(cons_file)
                consumption_raw['datetime']=pd.to_datetime(consumption_raw['datetime'],utc=True)

                u.mean_consumption=consumption_raw['consumption'].mean()
                u.total_consumption=round(consumption_raw['consumption'].sum())
                u.save()
                
                ## we need to slice the consumption data before pushing to the database as sqlite only allows 999 variables per query
                objs = (consumption_point(datetime=consumption_raw.loc[j,'datetime'],
                                        user_fk=u,
                                        consumption=consumption_raw.loc[j,'consumption']) for j in range(consumption_raw.shape[0]-1))
                batch_size = 100
                while True:
                    batch = list(islice(objs, batch_size))
                    if not batch:
                        break
                    consumption_point.objects.bulk_create(batch, batch_size)

                self.stdout.write(self.style.SUCCESS('Successfully read and stored user "%s" data' % user_raw.loc[i,'id']))
            self.stdout.write(self.style.SUCCESS('Successfully read and stored all user data'))
