class CrObject:
    def __init__(self, _print):
        self._print = _print
        
    def save(self):
        return True
        
    def all(_print):
        result = []
        for x in range(6):
            result.append(CrObject(_print))
        return result
        
    def find_by_id(id, _print):
        return CrObject(_print)
        
    def update(self, cr_object):
        return True
        
    def destroy(self):
        return True
        
    def has_children(self):
        return True
        
    def find_relation(self):
        return True

