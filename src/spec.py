"""
A tool to generate scripts using rclone to do backups.

Allows some sanity checking over your config, etc.

The scripts outputted are meant to be human readable.
"""
from enum import Enum, auto


class Spec(Enum):
    """
    Basically, we use these as descriptions in a spec to say how to handle that
    part of the dictionary.
    """
    REQUIRED = auto()
    OPTIONAL = auto()
    HASH = auto()


class SpecTypes(Enum):
    """
    Types our format can contain.
    """
    STRING = auto()
    INT = auto()
    FLOAT = auto()
    NUMBER = auto()
    BOOL = auto()
    STR_LIST = auto()


class SpecInvalid(Exception):
    """
    Exception for when a input object doesn't match the spec.
    """
    def __init__(self, name):
        self.name = name
        super().__init__()

    def __str__(self):
        return self.name

def validate_dict(obj, spec):
    """
    Validates the dictionary component of the configuration format.
    """
    for key in obj:
        if key in spec:
            required, ftype = spec[key]

            if required == Spec.REQUIRED:
                # this value MUST be in the obj.
                if key not in obj:
                    raise SpecInvalid(
                        'required key `%s` not in object' % key)

                validate(obj[key], ftype)

            elif required == Spec.OPTIONAL:
                if key not in obj:
                    continue

                validate(obj[key], ftype)

            elif required == Spec.HASH:
                # Essentially a special case of optional
                for _, child in obj[key].items():
                    validate(child, ftype)

        else:
            raise SpecInvalid(
                'unknown key `%s` found in object' % key)
    
    return True


def validate_type(obj, spec):
    """
    Checks if the type matches up.
    """
    if spec == SpecTypes.STRING:
        return isinstance(obj, str)
    elif spec == SpecTypes.BOOL:
        return isinstance(obj, bool)
    elif spec == SpecTypes.INT:
        return isinstance(obj, int)
    elif spec == SpecTypes.FLOAT:
        return isinstance(obj, float)
    elif spec == SpecTypes.NUMBER:
        return isinstance(obj, float) or isinstance(obj, int)
    elif spec == SpecTypes.STR_LIST:
        if not isinstance(obj, list):
            return False
        for item in obj:
            if not isinstance(item, str):
                return False

        return True
    else:
        raise SpecInvalid('Unknown spec in spec?!')


def validate(obj, spec):
    """
    Checks if an object matches the spec.

    This is recursive to make it easier to write and I really don't expect this
    to be really deep in a call stack.
    """
    if isinstance(spec, dict):
        return validate_dict(obj, spec)
    else:
        if not validate_type(obj, spec):
            raise SpecInvalid(
                'Read value %s that doesn\'t match the required type %s' %
                              (obj, spec)
            )

    return True
