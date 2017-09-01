# Module types

import _qpid_proton_impl.types as _types

# Scalar data types

class Null(object):
    """
    An empty value.
    """

    pass

class Boolean(object):
    """
    A true or false value.
    """

    pass

class Char(object):
    """
    A single Unicode character.
    """

    pass

class String(object):
    """
    A sequence of Unicode characters.
    """

    pass

class Binary(object):
    """
    A sequence of bytes.
    """

    pass

class Float(object):
    """
    A 32-bit floating point number.
    """

    pass

class Double(object):
    """
    A 64-bit floating point number.
    """

    pass

class Byte(object):
    """
    A signed 8-bit integer.
    """

    pass

class Short(object):
    """
    A signed 16-bit integer.
    """

    pass

class Int(object):
    """
    A signed 32-bit integer.
    """

    pass

class Long(object):
    """
    A signed 64-bit integer.
    """

    pass

class Ubyte(object):
    """
    An unsigned 8-bit integer.
    """

    pass

class Ushort(object):
    """
    An unsigned 16-bit integer.
    """

    pass

class Uint(object):
    """
    An unsigned 32-bit integer.
    """

    pass

class Ulong(object):
    """
    An unsigned 64-bit integer.
    """

    pass

# Composite data types

class Array(object):
    """
    A sequence of values of a single type.
    """

    pass

class List(object):
    """
    A sequence of values of variable type.
    """

    pass

class Map(object):
    """
    A mapping from distinct keys to values.
    """

    pass

# Semantic data types

class Symbol(object):
    """
    A 7-bit ASCII string from a constrained domain.
    """

    pass

class Timestamp(object):
    """
    An absolute point in time.
    """

    pass

class Uuid(object):
    """
    A universally unique identifier.
    """

    pass

class MessageId(object):
    """
    A message identifier.  Legal types are ulong, uuid, binary, and
    string.
    """

    pass

# Decimal floating-point data types

class Decimal32(object):
    """
    A 32-bit decimal floating point number.
    """

    pass

class Decimal64(object):
    """
    A 64-bit decimal floating point number.
    """

    pass

class Decimal128(object):
    """
    A 128-bit decimal floating point number.
    """

    pass

# API data types

class Duration(object):
    """
    A span of time.
    """

    pass

class Iterator(object):
    """
    A traversal of a collection.
    """

    pass

class Object(object):
    """
    The most basic type.
    """

    pass

# End of module types
