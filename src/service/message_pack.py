import json


class message(dict):
    # the standard massage class
    def __init__(
            self, recv_from=None, send_to=None, content=None,
            timestamp=None, user_agent=None, recv_from_name='Unknown'):
        self['recv_from'] = recv_from
        self['send_to'] = send_to
        self['content'] = content
        self['timestamp'] = timestamp
        self['user_agent'] = user_agent
        self['recv_from_name'] = recv_from_name

    def recv_from(self):
        # return who send this message
        return self.get('recv_from')

    def send_to(self):
        return self.get('send_to')

    def content(self):
        return self.get('content')

    def package(self):
        return json.dumps(self)

    def unpackage(self, comment):
        try:
            me = json.loads(comment)
        except TypeError:
            return False
        try:
            self['recv_from'] = me.get('recv_from')
            self['send_to'] = me.get('send_to')
            self['content'] = me.get('content')
            self['timestamp'] = me.get('timestamp')
            self['user_agent'] = me.get('user_agent')
            self['recv_from_name'] = me.get('recv_from_name')
            return True
        except KeyError:
            return False


def main():
    str1 = message('a', 'b', 'hello world')
    print(str1.recv_from(), str1.send_to(), str1.content())
    str2 = str1.package()
    print(str2)
    str1.unpackage(str2)
    print(str1)
    print(type(str1))
    # str1.package()


if __name__ == '__main__':
    main()
