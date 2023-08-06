class Cr:
    def __init__(self, obj_class, _print):
        self._print = _print
        self._obj_class = obj_class
        
    def new(self, data):
        item = self._obj_class(data)
        return item.save()
        
    def get(self, id):
        item = self._obj_class.find_by_id(id)
        return item
        
    def destroy(self, id):
        item = self.get(id)
        if item is None:
            return None
        return item.destroy()
        
    def update(self, id, data):
        item = self.get(id)
        if item is None:
            return None
        return item.update(data)
        
    def find_all(self):
        return self._obj_class.all()
        
    def has_children_in_relation(self, id):
        return True
        
    def find_relation(id):
        return []
        
    def find_by_id(self, id):
        return self.get(id)
