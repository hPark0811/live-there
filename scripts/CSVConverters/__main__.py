""" Entry point of conversion module """
from UniversityCSVConvert import UniversityConverter
import os
import sys

CSV_RAW_PATH = os.path.join(os.path.dirname(__file__), 'csv', 'raw')

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        if args[1] == '--university':
            # Execute university csv conversion

            # Retrieve parameters
            host = '35.225.74.52' #input('Enter Host: ')
            user = 'root' #input('Enter user: ')
            pw = 'livethere2020' #input('Enter password: ')

            # Configure path
            uni_csv_path = os.path.join(CSV_RAW_PATH, 'university.csv')
            print(f'Converting CSV @ {uni_csv_path} to SQL')

            converter = UniversityConverter(host, user, pw, uni_csv_path)

            commit = input('To commit type y [y/n] ')
            if commit == 'y':
                # Commit new changes
                converter.commit()
                print('DB is updated.')
