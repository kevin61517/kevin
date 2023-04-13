from tenacity import retry, retry_if_exception_type, wait_fixed, stop_after_attempt


retry = retry(
    reraise=True,
    retry=retry_if_exception_type(
        exception_types=tuple([TimeoutError, TypeError])
    ),
    wait=wait_fixed(3),
    stop=stop_after_attempt(10)
)


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
