import json


class message(dict):
    # the standard massage class
    def __init__(
            self, recv_from=None, send_to=None, content=None,
            timestamp=None, user_agent=None, memetype='Text',
            pack_num=None, recv_from_name='Unknown'):
        self['recv_from'] = recv_from
        self['send_to'] = send_to
        self['content'] = content
        self['timestamp'] = timestamp
        self['user_agent'] = user_agent
        self['memetype'] = memetype
        self['pack_num'] = pack_num
        self['recv_from_name'] = recv_from_name

    def recv_from(self):
        # return who send this message
        return self.get('recv_from')

    def send_to(self):
        return self.get('send_to')

    def content(self):
        return self.get('content')

    def content_join(self, comment):
        self['content'] = self['content'] + comment

    def package(self):
        return json.dumps(self)

    def unpackage(self, comment):
        try:
            me = json.loads(comment)
        except json.JSONDecodeError:
            return False
        try:
            for key in me:
                self[key] = me[key]
            return True
        except KeyError:
            return False


def message_pack(
        recv_from=None, send_to=None, content=None,
        timestamp=None, user_agent=None, memetype='Text',
        recv_from_name='Unknown', pack_lenth=2048):
    message_pack = []
    pack_num = 0
    if len(content) >= 2048:
        pack_num = 1
    while content:
        message_pack.append(
            message(
                    recv_from, send_to, content[:pack_lenth],
                    timestamp, user_agent, memetype,
                    pack_num, recv_from_name)
        )
        content = content[pack_lenth:]
        pack_num += 1
    message_pack[-1]['pack_num'] = -1
    return message_pack


def main():
    mp = message_pack('a', 'b', 'hello world')
    str1 = mp[0]
    print(str1.recv_from(), str1.send_to(), str1.content())
    str2 = str1.package()
    print(str2)
    str1.unpackage(str2)
    print(str1)
    print(type(str1))
    # str1.package()


if __name__ == '__main__':
    main()
