"""This moduke contains utilities.

.. currentmodule:: marketplace.app.utils
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""

import functools
import re


def check_capability_availability(func_or_capability, capability=None):
    """Decorator for checking that a certain app supports a given capability.

    Args:
        capability (str): capability that should be in capabilities
    """
    if callable(func_or_capability):
        # get a func
        func = func_or_capability

        @functools.wraps(func)
        def wrapper(instance, *args, **kwargs):
            _capability = capability or func.__name__

            if _capability not in instance.capabilities:
                raise NotImplementedError("The app does not support this capability.")
            return func(instance, *args, **kwargs)

        return wrapper

    elif isinstance(func_or_capability, str):
        # get a str for capability
        return functools.partial(
            check_capability_availability, capability=func_or_capability
        )


def camel_to_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
