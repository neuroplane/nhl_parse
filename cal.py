import datetime
from datetime import datetime

task_date_time = "30.05.1984 09:00"
task_name = "День рождения папы"
obj = datetime.strptime(task_date_time, "%d.%m.%Y %H:%M")

print(obj)
