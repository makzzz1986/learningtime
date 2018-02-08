import json

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
