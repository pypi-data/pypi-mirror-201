import csv
import pathlib

import np_logging

import np_session

logger = np_logging.getLogger()

project = 'DR'

for session in np_session.sessions(project=project):
    m = session.get_missing_files()
    print(m)
    break
# for_csv = []
# for _ in missing:
#     for_csv.append(tuple([_, *missing[_]]))
        
# with open(f'{project}_missing.csv', 'w') as f:
#     csv.writer(f).writerows(for_csv)