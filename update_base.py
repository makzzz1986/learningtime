from app import db
from app.models import User, Comment, Homework, Task, Subtask, Answers


u = User(username='Alice', password_hash='pbkdf2:sha256:50000$JzEe85lG$f0a10c3d079bc7c988adb9779f8cd9df5828f9466e1547dd7e300e9497ef9086', status='teacher')
db.session.add(u)
u = User(username='John', password_hash='pbkdf2:sha256:50000$JzEe85lG$f0a10c3d079bc7c988adb9779f8cd9df5828f9466e1547dd7e300e9497ef9086', status='student')
db.session.add(u)
u = User(username='Bob', password_hash='pbkdf2:sha256:50000$JzEe85lG$f0a10c3d079bc7c988adb9779f8cd9df5828f9466e1547dd7e300e9497ef9086', status='student')
db.session.add(u)

db.session.commit()


ts = Task(level=1, theme='Elementary gramma', name='Unit 1')
db.session.add(ts)
ts = Task(level=1, theme='Elementary gramma', name='Unit 2')
db.session.add(ts)
ts = Task(level=2, theme='Intermediate gramma', name='Unit 1')
db.session.add(ts)
ts = Task(level=3, theme='Upper intermediate speaking', name='Unit 4')
db.session.add(ts)

db.session.commit()

st = Subtask(task_id=1, body='London is Great Britain')
db.session.add(st)
st = Subtask(task_id=1, body='Paris is the capital of ')
db.session.add(st)
st = Subtask(task_id=1, body='My name  Alice')
db.session.add(st)
st = Subtask(task_id=1, body='I from Novosibirsk')
db.session.add(st)

st = Subtask(task_id=2, body='werwer')
db.session.add(st)
st = Subtask(task_id=2, body='qweqal of ')
db.session.add(st)
st = Subtask(task_id=3, body='FRENFe')
db.session.add(st)
st = Subtask(task_id=4, body='I WER#M')
db.session.add(st)

db.session.commit()

hm = Homework(finished=False, user_id=2, task_id=1)
db.session.add(hm)
hm = Homework(finished=False, user_id=2, task_id=3)
db.session.add(hm)
hm = Homework(finished=True, user_id=3, task_id=1)
db.session.add(hm)

db.session.commit()

ans = Answers(homework_id=1, comments='WTF?', body='[]{}FFF')
db.session.add(ans)


db.session.commit()
print('Updated!')