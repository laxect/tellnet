import json


class message(dict):
    # the standard massage class
    def __init__(
            self, user_from=None, user_to=None, content=None,
            timestamp=None, user_agent=None):
        self['user_from'] = user_from
        self['user_to'] = user_to
        self['content'] = content
        self['timestamp'] = timestamp
        self['user_agent'] = user_agent

    def package(self):
        return json.dumps(self)

    def unpackage(self, comment):
        me = json.loads(comment)
        try:
            self['user_from'] = me['user_from']
            self['user_to'] = me['user_to']
            self['content'] = me['content']
            self['timestamp'] = me['timestamp']
            self['user_agent'] = me['user_agent']
            return True
        except KeyError:
            return False


def main():
    str1 = message('a', 'b', 'hello world', '2017-05-01 00:00', 'cli-TK-0.1')
    str2 = str1.package()
    print(str2)
    str1.unpackage(str2)
    print(str1)
    print(type(str1))
    # str1.package()


if __name__ == '__main__':
    main()
