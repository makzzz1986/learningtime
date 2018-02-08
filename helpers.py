import json
from flask import request

# класс задания
class Box():
    level = 0
    course = ''
    theme = ''
    name = ''
    subs = [[]]

    def __init__(self, name=''):
        self.name = name

    def add_subs(self, lst):
        temp_lst = []
        for elem in lst:
            if len(elem.strip())>0:
                temp_lst.append(elem)
        self.subs.append(lst)

    def export_dict(self):
        return {'level': self.level, 'course': self.course, 'theme': self.theme, 'name': self.name, 'subs': self.subs}

    def export_json(self):
        return json.dumps(self.get_dict())

    def import_json(self, string):
        try:
            decoded = json.loads(string)
            self.level = decoded['level']
            self.course = decoded['course']
            self.theme = decoded['theme']
            self.name = decoded['level']
            self.add_subs(decoded['subs'])
            return True
        except JSONDecodeError:
            print('Wrong import, decoder Error!')
            return False
        except Exception as e:
            print('Wrong import')
            print(str(e))
            return False

    def import_request(req):
        sended = {}
        # превращаем формы в словарь
        for elem in request.form:
            sended[elem] = request.form[elem]
        # {'finish': '', 'level': '', 'theme': '', 'name': 'name', '1/1': 'werwe', '1/2': 'd', '1/3': '', 
        # '1/4': '', '1/5': '', '2/1': '', '2/2': '', '2/3': '', '2/4': '', '2/5': '', '2/6': '', '3/1': '', '3/2': '', '3/3': ''}
        self.level = sended['level']
        self.course = sended['course']
        self.theme = sended['theme']
        self.name = sended['level']
        temp_dict = {}
        for elem in sended:
            if '/' in elem:
                sublist, line = elem.split('/')
                if sublist in temp_dict:
                    temp_dict[sublist] = {line: sended[elem]}
        print(temp_dict)