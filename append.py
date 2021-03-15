# Python program to update 
# JSON 

import json

# function to add to JSON 
def write_json(data, filename='calendar.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

new_date = input('Date:\t')
new_time = input('Time:\t')
new_task = input('Task:\t')
new_comment = input('Comment:\t')

with open('calendar.json') as json_file:
    data = json.load(json_file)

    temp = data['recurrent']

    # python object to be appended
    y = {"task_first_date": new_date,
         "task_time": new_time,
         "task_name": new_task,
         "comment": new_comment
         }

    # appending data to emp_details
    temp.append(y)

write_json(data) 

