import os
import sys
import datetime as dt
from datetime import date

# Takes a folder as an argument
# Returns the name of the appropriate timetable - the current day must be between the dates in the file name
# in the case of many such days, the one with the latest timestamp wins

def get_latest_timetable_containing_today(folder):
    folder_content = os.listdir(folder)
    date_zips = []
    successful = []
    # The program will only run correctly if the zips have the format date_date#########-timestamp########.zip
    # E.g. 20220701_20240630_PKS_POZNAN-20220616T102949Z@#$#@$.zip
    for filename in folder_content:
        # Preventively takes only zips with 2 at the start (will work until year 3000)
        if filename[-3:] == 'zip' and filename[0] == '2':
            date_zips.append((filename[:17].split('_'), filename))
    for timetable in date_zips:
        dates = timetable[0]
        # Date comparison with today's date
        for i in range(2):
            dates[i] = dt.datetime.strptime(dates[i], '%Y%m%d').date()
        if dates[0] <= date.today() <= dates[1]:
            successful.append(timetable[1])
    if successful == []:
        print('No suitable file found.')
    else:
        maxi = ''
        winner = 0
        for count, element in enumerate(successful):
            # Everything will work only if the format is correct
            timestamp = element.split('-')[1][:17]
            if timestamp > maxi:
                maxi = timestamp
                winner = count
        return successful[winner]
        

if __name__ == "__main__":
    get_latest_timetable_containing_today(sys.argv[1])




