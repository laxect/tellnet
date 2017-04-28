class tunel:
    def __init__(self, tn_id, name=None, cnt=0):
        self.tn_id = tn_id
        if name:
            self.name = name
        else:
            self.name = 'tunel '+str(tn_id)[1:]
        self.cnt = cnt


class tunel_pool:
    def __init__(self):
        self.pool = {}
        self.pool['t0'] = tunel('t0', 'main tunel', 1)

    def join_tn(self, tn_id):
        self.pool.setdefault(tn_id, tunel(tn_id=tn_id, cnt=0))
        self.pool[tn_id].cnt += 1
        return tn_id

    def leave_tn(self, tn_id):
        if tn_id in self.pool:
            self.pool[tn_id].cnt -= 1
            if not self.pool[tn_id].cnt:
                self.pool.pop(tn_id)

    def ch_tn(self, tn_id_from, tn_id_to):
        self.join_tn(tn_id_to)
        self.leave_tn(tn_id_from)
        return tn_id_to

    def chname_tn(self, tn_id, new_name):
        if tn_id == 't0':
            return False
        self.pool[tn_id].name = new_name
        return True


__all__ = [tunel, tunel_pool]
