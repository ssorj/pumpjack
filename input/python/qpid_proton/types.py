# Module types

import _qpid_proton_impl.types as _core

# Scalar data types

class Null(object):
    """
    An empty value.
    """

    # End of class Null

class Boolean(object):
    """
    A true or false value.
    """

    # End of class Boolean

class Char(object):
    """
    A single Unicode character.
    """

    # End of class Char

class String(object):
    """
    A sequence of Unicode characters.
    """

    # End of class String

class Binary(object):
    """
    A sequence of bytes.
    """

    # End of class Binary

class Float(object):
    """
    A 32-bit floating point number.
    """

    # End of class Float

class Double(object):
    """
    A 64-bit floating point number.
    """

    # End of class Double

class Byte(object):
    """
    A signed 8-bit integer.
    """

    # End of class Byte

class Short(object):
    """
    A signed 16-bit integer.
    """

    # End of class Short

class Int(object):
    """
    A signed 32-bit integer.
    """

    # End of class Int

class Long(object):
    """
    A signed 64-bit integer.
    """

    # End of class Long

class Ubyte(object):
    """
    An unsigned 8-bit integer.
    """

    # End of class Ubyte

class Ushort(object):
    """
    An unsigned 16-bit integer.
    """

    # End of class Ushort

class Uint(object):
    """
    An unsigned 32-bit integer.
    """

    # End of class Uint

class Ulong(object):
    """
    An unsigned 64-bit integer.
    """

    # End of class Ulong

# Composite data types

class Array(object):
    """
    A sequence of values of a single type.
    """

    # End of class Array

class List(object):
    """
    A sequence of values of variable type.
    """

    # End of class List

class Map(object):
    """
    A mapping from distinct keys to values.
    """

    # End of class Map

# Semantic data types

class Symbol(object):
    """
    A 7-bit ASCII string from a constrained domain.
    """

    # End of class Symbol

class Timestamp(object):
    """
    An absolute point in time.
    """

    # End of class Timestamp

class Uuid(object):
    """
    A universally unique identifier.
    """

    # End of class Uuid

class MessageId(object):
    """
    A message identifier.  Legal types are ulong, uuid, binary, and
    string.
    """

    # End of class MessageId

# Decimal floating-point data types

class Decimal32(object):
    """
    A 32-bit decimal floating point number.
    """

    # End of class Decimal32

class Decimal64(object):
    """
    A 64-bit decimal floating point number.
    """

    # End of class Decimal64

class Decimal128(object):
    """
    A 128-bit decimal floating point number.
    """

    # End of class Decimal128

# API data types

class Duration(object):
    """
    A span of time.
    """

    # End of class Duration

class Iterator(object):
    """
    A traversal of a collection.
    """

    # End of class Iterator

class Object(object):
    """
    The most basic type.
    """

    # End of class Object

# End of module types
