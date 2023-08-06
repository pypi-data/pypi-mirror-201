class RequestNadrInvalidError(ValueError):
    """
    Invalid NADR value.

    This error is raised whenever a request object receives
    address that is out of allowed range ([C]: 0, [N]: 1-239).
    """
    pass


class RequestHwpidInvalidError(ValueError):
    """
    Invalid HWPID value.

    This error is raised whenever a request object receives
    HWPID that is out of allowed range (0-65535 / 0x00-0xFF).
    """
    pass


class RequestParameterInvalidValueError(ValueError):
    """
    Invalid request parameter value.

    This error is raised whenever a request object receives
    a parameter with value outside of it's defined domain.
    """
    pass


class DpaConfirmationPacketError(ValueError):
    """
    Invalid DPA confirmation packet.

    This error is raised whenever a packet does not meet requirements
    of a DPA confirmation packet.
    """
    pass


class DpaConfirmationPacketLengthError(ValueError):
    """
    Invalid DPA confirmation packet length.

    This error is raised whenever a DPA confirmation packet length does
    not match expected packet length.
    """
    pass


class DpaResponsePacketLengthError(ValueError):
    """
    Invalid DPA response packet length.

    This error is raised whenever a DPA response packet length
    does not match the expected packet length of a specific DPA response.
    """
    pass


class JsonMsgidMissingError(KeyError):
    """
    msgId property missing.

    This error is raised whenever a json response object
    does not contain the msgId property.
    """
    pass


class JsonMTypeMissingError(KeyError):
    """
    mType property missing.

    This error is raised whenever a json response object
    does not contain the mType property.
    """
    pass


class JsonNadrMissingError(KeyError):
    """
    nAdr property missing.

    This error is raised whenever a json response object
    does not contain the nAdr property.
    """
    pass


class JsonHwpidMissingError(KeyError):
    """
    hwpId property missing.

    This error is raised whenever a json response object
    does not contain the hwpId property.
    """
    pass


class JsonRCodeMissingError(KeyError):
    """
    rCode property missing.

    This error is raised whenever a json response object
    does not contain the rCode property.
    """
    pass


class JsonDpaValueMissingError(KeyError):
    """
    dpaVal property missing.

    This error is raised whenever a json response object
    does not contain the dpaVal property.
    """
    pass


class JsonResultMissingError(KeyError):
    """
    result property missing.

    This error is raised whenever a json response object
    does not contain the result property.
    """
    pass


class JsonStatusMissingError(KeyError):
    """
    status property missing.

    This error is raised whenever a json response object
    does not contain the status property.
    """
    pass


class InvalidPeripheralValueError(ValueError):
    """
    Invalid peripheral value.

    This error is raised whenever a peripheral parameter value is out
    of defined range.
    """
    pass


class InvalidPeripheralCommandValueError(ValueError):
    """
    Invalid peripheral command value.

    This error is raised whenever a peripheral command parameter value is out
    of defined range.
    """
    pass


class UnsupportedPeripheralError(ValueError):
    """
    Peripheral unknown or unsupported.

    This error is raised whenever a peripheral parameter value is valid,
    but not recognized as a known and supported peripheral.
    """
    pass


class UnsupportedPeripheralCommandError(ValueError):
    """
    Peripheral command unknown or unsupported.

    This error is raised whenever a peripheral parameter command value is valid,
    but not recognized as a known and supported peripheral command.
    """
    pass


class UnsupportedMessageTypeError(ValueError):
    """
    Message type unknown or unsupported.

    This error is raised whenever a message type parameter is used
    to determine a value, but the message type parameter value is not
    recognized as a known and supported message type.
    """
    pass
