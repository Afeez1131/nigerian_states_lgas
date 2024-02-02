from django.core.management import BaseCommand
from nigerian_states.models import State, LocalGovernment
from tqdm import tqdm
import json

class Command(BaseCommand):
    help = "Load the data for all states and lgas into db"
    
    def handle(self, *args, **options):
        print('\n=====Loading data into DB===== \n')
        with open('states.json', 'r') as file:
            temp = file.read()
            json_file = json.loads(temp)
            progress_bar_states = tqdm(json_file, desc='States', unit='state')
            for item in progress_bar_states:
                state_name = item.get('state')
                lgas = item.get('lgas')
                zone = item.get('zone')
                
                state, _ = State.objects.get_or_create(name=state_name, zone=zone)
                
                progress_bar_lgas = tqdm(lgas, desc=f'LGAs for {state_name}', unit='lga')
                
                for lga in progress_bar_lgas:
                    LocalGovernment.objects.get_or_create(state=state, name=lga)

        self.stdout.write(self.style.SUCCESS("Data loading completed"))