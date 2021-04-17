class Model():
    def __init__(self, *args, **kwargs):
        pass
    def to_dict(self):
        return {a: self.a for a in dir(obj) if not a.startswith('__') and not callable(getattr(obj, a))}