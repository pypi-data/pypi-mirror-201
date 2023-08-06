import warnings



__all__ = ['deprecated']

def deprecated(version=None):
    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            if version is None:
                warning_string = f"Call to deprecated function {func.__name__}. " \
                                f"This function will be removed in the future."
            else:
                warning_string = f"Call to deprecated function {func.__name__}. " \
                            f"This function will be removed in version {version}."
            warnings.warn(warning_string, 
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)
        return deprecated_func
    return deprecated_decorator