# -*- coding: utf-8 -*-
# coding: utf8


#import datetime
import json
from datetime import datetime

task_object = {}

task_date_time = "15.03.2021,08:00"
task_name = "Алина. Ледовый"
task_time = datetime.strptime(task_date_time, "%d.%m.%Y,%H:%M").strftime('%H:%M')
task_date = datetime.strptime(task_date_time, "%d.%m.%Y,%H:%M").strftime('%d.%m.%Y')
is_recurrent_weekly = True
comment = ''

task_file = {}
task_file['recurrent'] = []

task_object = {'task_first_date': task_date, 'task_time': task_time, 'task_name': task_name, 'is_recurrent_weekly': is_recurrent_weekly, 'comment': comment}
task_object_dumped = json.dumps(task_object, ensure_ascii=False, indent=2)

task_file['recurrent'].append(task_object)
task_output = task_file
with open('calendar.json', 'w') as outfile:
    json.dump(task_output, outfile, ensure_ascii=False, indent=2)


print(task_object_dumped)
print(json.loads(task_object_dumped))
