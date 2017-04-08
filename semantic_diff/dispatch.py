import functools

def type_dispatch(*args, **kwargs):
    if not args:
        return lambda fn: real_type_dispatch(fn, **kwargs)
    else:
        return real_type_dispatch(*args, **kwargs)

type_dispatch.NEXT = object()

def real_type_dispatch(fn, fatal=False):
    fn_name = fn.__name__

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        if result != type_dispatch.NEXT:
            return result

        dispatch_arg = args[0] # methods only
        dispatch_fn_name = fn_name + '_' + type(dispatch_arg).__name__
        if not hasattr(self, dispatch_fn_name):
            if fatal:
                # XXX better exception type
                raise Exception('No dispatcher {}'.format(dispatch_fn_name))
            else:
                return
        dispatch_fn = getattr(self, dispatch_fn_name)
        return dispatch_fn(*args, **kwargs)
    return wrapper

