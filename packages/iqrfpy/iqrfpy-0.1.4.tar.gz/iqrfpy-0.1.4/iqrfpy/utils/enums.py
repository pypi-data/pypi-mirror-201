import enum

__all__ = ['IntEnumMember']


class IntEnumMember(enum.IntEnum):
    pass

    @classmethod
    def has_value(cls, value: int):
        """
        Check if enum contains member.

        Parameters
        ----------
        value: int
            Value to find in enum
        """
        return value in cls._value2member_map_
