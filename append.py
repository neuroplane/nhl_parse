import json
from datetime import datetime

#new_date = input('Введите дату:\t')
#new_time = input('Введите время:\t')
#new_task = input('Введите имя задания:\t')
#new_comment = input('Введите комментарий:\t')

new_date = 'New date'
new_time = 'new time'
new_task = 'new task'
new_comment = 'new comment'

new_recurrent = {'task_first_date': new_date, 'task_time': new_time, 'task_name': new_task, 'comment': new_comment}
new_data = None

with open('calendar.json') as cal:
    data = json.load(cal)
    print(data)
    data['recurrent'].append(new_recurrent)
    data['birthdays'] = []
    new_data = data['recurrent']
    #print(new_data)
    #json.dump(new_data, cal, ensure_ascii=False, indent=2)
print(data)
#print(new_date + new_time + new_task + new_comment)