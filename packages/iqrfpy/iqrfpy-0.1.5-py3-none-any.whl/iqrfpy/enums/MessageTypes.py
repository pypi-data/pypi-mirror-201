"""
Message types module.

This module contains embed peripherals and standards message type enums.
These enums are extended with has_value() method for member identification.
"""

import enum

__all__ = [
    'MessageType',
    'GenericMessages',
    'ExplorationMessages',
    'CoordinatorMessages',
    'NodeMessages',
    'OSMessages',
    'EEPROMMessages',
    'EEEPROMMessages',
    'RAMMessages',
    'LEDRMessages',
    'LEDGMessages',
    'IOMessages',
    'ThermometerMessages',
    'UartMessages',
    'FrcMessages',
    'DALIMessages',
    'BinaryOutputMessages',
    'SensorMessages',
    'LightMessages'
]


class MessageType(enum.Enum):
    pass

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class GenericMessages(MessageType):
    RAW = 'iqrfRaw'
    RAW_HDP = 'iqrfRawHdp'


class ExplorationMessages(MessageType):
    ENUMERATE = 'iqrfEmbedExplore_Enumerate'
    PERIPHERAL_INFORMATION = 'iqrfEmbedExplore_PeripheralInformation'
    MORE_PERIPHERALS_INFORMATION = 'iqrfEmbedExplore_MorePeripheralsInformation'


class CoordinatorMessages(MessageType):
    ADDR_INFO = 'iqrfEmbedCoordinator_AddrInfo'
    DISCOVERED_DEVICES = 'iqrfEmbedCoordinator_DiscoveredDevices'
    BONDED_DEVICES = 'iqrfEmbedCoordinator_BondedDevices'
    CLEAR_ALL_BONDS = 'iqrfEmbedCoordinator_ClearAllBonds'
    BOND_NODE = 'iqrfEmbedCoordinator_BondNode'
    REMOVE_BOND = 'iqrfEmbedCoordinator_RemoveBond'
    DISCOVERY = 'iqrfEmbedCoordinator_Discovery'
    SET_DPA_PARAMS = 'iqrfEmbedCoordinator_SetDpaParams'
    SET_HOPS = 'iqrfEmbedCoordinator_SetHops'
    BACKUP = 'iqrfEmbedCoordinator_Backup'
    RESTORE = 'iqrfEmbedCoordinator_Restore'
    AUTHORIZE_BOND = 'iqrfEmbedCoordinator_AuthorizeBond'
    SMART_CONNECT = 'iqrfEmbedCoordinator_SmartConnect'
    SET_MID = 'iqrfEmbedCoordinator_SetMID'


class NodeMessages(MessageType):
    READ = 'iqrfEmbedNode_Read'
    REMOVE_BOND = 'iqrfEmbedNode_RemoveBond'
    BACKUP = 'iqrfEmbedNode_Backup'
    RESTORE = 'iqrfEmbedNode_Restore'
    VALIDATE_BONDS = 'iqrfEmbedNode_ValidateBonds'


class OSMessages(MessageType):
    READ = 'iqrfEmbedOs_Read'
    RESET = 'iqrfEmbedOs_Reset'
    READ_CFG = 'iqrfEmbedOs_ReadCfg'
    RFPGM = 'iqrfEmbedOs_Rfpgm'
    SLEEP = 'iqrfEmbedOs_Sleep'
    BATCH = 'iqrfEmbedOs_Batch'
    SET_SECURITY = 'iqrfEmbedOs_SetSecurity'
    INDICATE = 'iqrfEmbedOs_Indicate'
    RESTART = 'iqrfEmbedOs_Restart'
    WRITE_CFG_BYTE = 'iqrfEmbedOs_WriteCfgByte'
    LOAD_CODE = 'iqrfEmbedOs_LoadCode'
    SELECTIVE_BATCH = 'iqrfEmbedOs_SelectiveBatch'
    TEST_RF_SIGNAL = 'iqrfEmbedOs_TestRfSignal'
    FACTORY_SETTINGS = 'iqrfEmbedOs_FactorySettings'
    WRITE_CFG = 'iqrfEmbedOs_WriteCfg'


class RAMMessages(MessageType):
    READ = 'iqrfEmbedRam_Read'
    WRITE = 'iqrfEmbedRam_Write'


class EEPROMMessages(MessageType):
    READ = 'iqrfEmbedEeprom_Read'
    WRITE = 'iqrfEmbedEeprom_Write'


class EEEPROMMessages(MessageType):
    READ = 'iqrfEmbedEeeprom_Read'
    WRITE = 'iqrfEmbedEeeprom_Write'


class LEDRMessages(MessageType):
    SET = 'iqrfEmbedLedr_Set'
    GET = 'iqrfEmbedLedr_Get'
    PULSE = 'iqrfEmbedLedr_Pulse'
    FLASHING = 'iqrfEmbedLedr_Flashing'


class LEDGMessages(MessageType):
    SET = 'iqrfEmbedLedg_Set'
    GET = 'iqrfEmbedLedg_Get'
    PULSE = 'iqrfEmbedLedg_Pulse'
    FLASHING = 'iqrfEmbedLedg_Flashing'


class IOMessages(MessageType):
    DIRECTION = 'iqrfEmbedIo_Direction'
    SET = 'iqrfEmbedIo_Set'
    GET = 'iqrfEmbedIo_Get'


class ThermometerMessages(MessageType):
    READ = 'iqrfEmbedThermometer_Read'


class UartMessages(MessageType):
    OPEN = 'iqrfEmbedUart_Open'
    CLOSE = 'iqrfEmbedUart_Close'
    WRITE_READ = 'iqrfEmbedUart_WriteRead'
    CLEAR_WRITE_READ = 'iqrfEmbedUart_ClearWriteRead'


class FrcMessages(MessageType):
    SEND = 'iqrfEmbedFrc_Send'
    EXTRA_RESULT = 'iqrfEmbedFrc_ExtraResult'
    SEND_SELECTIVE = 'iqrfEmbedFrc_SendSelective'
    SET_PARAMS = 'iqrfEmbedFrc_SetParams'


class DALIMessages(MessageType):
    SEND_COMMANDS = 'iqrfDali_SendCommands'
    SEND_COMMANDS_ASYNC = 'iqrfDali_SendCommandsAsync'
    FRC = 'iqrfDali_Frc'


class BinaryOutputMessages(MessageType):
    SET_OUTPUT = 'iqrfBinaryOutput_SetOutput'
    ENUMERATE = 'iqrfBinaryOutput_Enumerate'


class SensorMessages(MessageType):
    READ_SENSORS_WITH_TYPES = 'iqrfSensor_ReadSensorsWithTypes'
    ENUMERATE = 'iqrfSensor_Enumerate'
    FRC = 'iqrfSensor_Frc'


class LightMessages(MessageType):
    SET_POWER = 'iqrfLight_SetPower'
    INCREMENT_POWER = 'iqrfLight_IncrementPower'
    DECREMENT_POWER = 'iqrfLight_DecrementPower'
    ENUMERATE = 'iqrfLight_Enumerate'
