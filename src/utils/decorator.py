def call(cls):
    def inside(*args, **kwargs):
        return cls(*args, **kwargs)
    return inside()
