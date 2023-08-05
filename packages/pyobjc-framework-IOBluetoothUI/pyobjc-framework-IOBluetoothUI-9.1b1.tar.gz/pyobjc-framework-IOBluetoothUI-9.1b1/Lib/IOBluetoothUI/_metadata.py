# This file is generated by objective.metadata
#
# Last update: Sat Jan 14 21:30:00 2023
#
# flake8: noqa

import objc, sys
from typing import NewType

if sys.maxsize > 2**32:

    def sel32or64(a, b):
        return b

else:

    def sel32or64(a, b):
        return a


if objc.arch == "arm64":

    def selAorI(a, b):
        return a

else:

    def selAorI(a, b):
        return b


misc = {}
constants = """$$"""
enums = """$kBluetoothKeyboardANSIReturn@0$kBluetoothKeyboardISOReturn@1$kBluetoothKeyboardJISReturn@2$kBluetoothKeyboardNoReturn@3$kIOBluetoothServiceBrowserControllerOptionsAutoStartInquiry@1$kIOBluetoothServiceBrowserControllerOptionsDisconnectWhenDone@2$kIOBluetoothServiceBrowserControllerOptionsNone@0$kIOBluetoothUISuccess@-1000$kIOBluetoothUIUserCanceledErr@-1001$"""
misc.update(
    {
        "BluetoothKeyboardReturnType": NewType("BluetoothKeyboardReturnType", int),
        "IOBluetoothServiceBrowserControllerOptions": NewType(
            "IOBluetoothServiceBrowserControllerOptions", int
        ),
    }
)
misc.update({})
misc.update({})
functions = {
    "IOBluetoothGetDeviceSelectorController": (b"^{OpaqueIOBluetoothObjectRef=}",),
    "IOBluetoothValidateHardwareWithDescription": (b"i^{__CFString=}^{__CFString=}",),
    "IOBluetoothGetPairingController": (b"^{OpaqueIOBluetoothObjectRef=}",),
}
aliases = {
    "IOBluetoothServiceBrowserControllerRef": "IOBluetoothObjectRef",
    "IOBluetoothDeviceSelectorControllerRef": "IOBluetoothObjectRef",
    "IOBluetoothPairingControllerRef": "IOBluetoothObjectRef",
}
r = objc.registerMetaDataForSelector
objc._updatingMetadata(True)
try:
    r(
        b"IOBluetoothDeviceSelectorController",
        b"setSearchAttributes:",
        {"arguments": {2: {"type_modifier": b"n"}}},
    )
    r(
        b"IOBluetoothObjectPushUIController",
        b"isTransferInProgress",
        {"retval": {"type": b"Z"}},
    )
    r(
        b"IOBluetoothPairingController",
        b"setSearchAttributes:",
        {"arguments": {2: {"type_modifier": b"n"}}},
    )
    r(b"IOBluetoothPasskeyDisplay", b"isIncomingRequest", {"retval": {"type": b"Z"}})
    r(
        b"IOBluetoothPasskeyDisplay",
        b"setIsIncomingRequest:",
        {"arguments": {2: {"type": b"Z"}}},
    )
    r(
        b"IOBluetoothPasskeyDisplay",
        b"setPasskey:forDevice:usingSSP:",
        {"arguments": {4: {"type": b"Z"}}},
    )
    r(
        b"IOBluetoothPasskeyDisplay",
        b"setPasskeyIndicatorEnabled:",
        {"arguments": {2: {"type": b"Z"}}},
    )
    r(
        b"IOBluetoothPasskeyDisplay",
        b"setUsePasskeyNotificaitons:",
        {"arguments": {2: {"type": b"Z"}}},
    )
    r(
        b"IOBluetoothPasskeyDisplay",
        b"usePasskeyNotificaitons",
        {"retval": {"type": b"Z"}},
    )
    r(
        b"IOBluetoothServiceBrowserController",
        b"discover:",
        {"arguments": {2: {"type_modifier": b"o"}}},
    )
    r(
        b"IOBluetoothServiceBrowserController",
        b"discoverAsSheetForWindow:withRecord:",
        {"arguments": {3: {"type_modifier": b"o"}}},
    )
    r(
        b"IOBluetoothServiceBrowserController",
        b"discoverWithDeviceAttributes:serviceList:serviceRecord:",
        {"arguments": {2: {"type_modifier": b"n"}, 4: {"type_modifier": b"o"}}},
    )
    r(
        b"IOBluetoothServiceBrowserController",
        b"setSearchAttributes:",
        {"arguments": {2: {"type_modifier": b"n"}}},
    )
finally:
    objc._updatingMetadata(False)
expressions = {}

# END OF FILE
