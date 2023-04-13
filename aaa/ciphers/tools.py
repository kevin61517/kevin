class Valid:
    @staticmethod
    def pass_if_type(*types):
        def _new(instance, attribute, obj):
            msg = 'Positional argument must be types '
            if type(obj) not in types:
                raise TypeError(msg + ' or '.join(f'{t.__name__}' for t in types) + f', not {type(obj).__name__}')
        return _new

    @staticmethod
    def raise_if_type(*types):
        def _new(instance, attribute, obj):
            msg = 'Positional argument must be not types '
            if type(obj) in types:
                raise TypeError(msg + ' or '.join(f'{t.__name__}' for t in types))
        return _new
