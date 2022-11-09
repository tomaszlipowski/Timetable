import os
import subprocess
import timetable_name
import shutil
from dataclasses import dataclass


@dataclass
class DataClassCarriers:
   name: str
   path_to_winner: str
   path_to_backups: str
   path_to_timetables: str

def main():
   # The script finds the latest timetable from the docker
   # Works when these folders exist: winner with 1 file, backups and timetables

   carriers = [
            DataClassCarriers('pkspoznan', '/var/www/clients/client1/web1/web/download', '/home/wojciech', '/home/wojciech/rozklady'),
            DataClassCarriers('swarzedz', '/var/www/iplaner.pl/public_html/gtfs', '/home/wojciech/backup', '/home/wojciech/rozklady'),
            DataClassCarriers('test', 'winner', 'backups', 'timetables')
               ]

   print('Please enter a number:')
   for count, carrier in enumerate(carriers):
      print(f'{count + 1}. {carrier.name}')
   while True:
      try:
         choice = int(input()) - 1
      except ValueError:
         print('Please enter a number.')
         continue
      if 0 <= choice <= len(carriers) - 1:
         break
      else:
         print(f'Wrong number, enter 1 to {len(carriers)}.')
   carrier = carriers[choice]
   print(f'Selected for {carrier.name}')

   # A copy of the GTFS file goes to the folder 'path_to_backups'

   folder_with_gtfs = carrier.path_to_winner
   path = os.listdir(folder_with_gtfs)[0]
   assert len(os.listdir(folder_with_gtfs)) == 1
   full_path = os.path.join(folder_with_gtfs, path)
   shutil.copy2(full_path, carrier.path_to_backups)

   # The latest timetables stored in a temporary folder are updated and moved to the final timetables folder

   subprocess.call(f"docker cp datatools-server:/tmp. {carrier.path_to_timetables}", shell=True)

   # Running the script that finds the appropriate timetable

   winner = timetable_name.get_latest_timetable_containing_today(carrier.path_to_timetables)
   print(winner)


   # Deletion of the current timetable

   os.remove(f'{full_path}')

   # Copy the found timetable to the folder 'path_to_winner' and changes his name
   winner_full_path = os.path.join(carrier.path_to_timetables, winner)
   shutil.copy2(winner_full_path, carrier.path_to_winner)
   newZip = f'{carrier.name}.zip'
   os.chdir(carrier.path_to_winner)
   os.replace(winner, newZip)
   print(newZip)

if __name__ == "__main__":
    main()