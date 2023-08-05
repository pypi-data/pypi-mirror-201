# This file is generated by objective.metadata
#
# Last update: Mon Feb 21 23:21:06 2022
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
constants = """$SNClassifierIdentifierVersion1$SNErrorDomain$"""
enums = """$SNErrorCodeInvalidFile@5$SNErrorCodeInvalidFormat@3$SNErrorCodeInvalidModel@4$SNErrorCodeOperationFailed@2$SNErrorCodeUnknownError@1$SNTimeDurationConstraintTypeEnumerated@1$SNTimeDurationConstraintTypeRange@2$"""
misc.update(
    {
        "SNErrorCode": NewType("SNErrorCode", int),
        "SNTimeDurationConstraintType": NewType("SNTimeDurationConstraintType", int),
    }
)
misc.update({"SNClassifierIdentifier": NewType("SNClassifierIdentifier", str)})
misc.update({})
r = objc.registerMetaDataForSelector
objc._updatingMetadata(True)
try:
    r(
        b"NSObject",
        b"request:didFailWithError:",
        {
            "required": False,
            "retval": {"type": b"v"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"@"}},
        },
    )
    r(
        b"NSObject",
        b"request:didProduceResult:",
        {
            "required": True,
            "retval": {"type": b"v"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"@"}},
        },
    )
    r(
        b"NSObject",
        b"requestDidComplete:",
        {"required": False, "retval": {"type": b"v"}, "arguments": {2: {"type": b"@"}}},
    )
    r(
        b"SNAudioFileAnalyzer",
        b"addRequest:withObserver:error:",
        {"retval": {"type": b"Z"}, "arguments": {4: {"type_modifier": b"o"}}},
    )
    r(
        b"SNAudioFileAnalyzer",
        b"analyzeWithCompletionHandler:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {0: {"type": b"^v"}, 1: {"type": b"@"}},
                    }
                }
            }
        },
    )
    r(
        b"SNAudioFileAnalyzer",
        b"initWithURL:error:",
        {"arguments": {3: {"type_modifier": b"o"}}},
    )
    r(
        b"SNAudioStreamAnalyzer",
        b"addRequest:withObserver:error:",
        {"retval": {"type": b"Z"}, "arguments": {4: {"type_modifier": b"o"}}},
    )
    r(
        b"SNClassificationResult",
        b"timeRange",
        {"retval": {"type": b"{_CMTimeRange={_CMTime=qiIq}{_CMTime=qiIq}}"}},
    )
    r(
        b"SNClassifySoundRequest",
        b"initWithClassifierIdentifier:error:",
        {"arguments": {3: {"type_modifier": b"o"}}},
    )
    r(
        b"SNClassifySoundRequest",
        b"initWithMLModel:error:",
        {"arguments": {3: {"type_modifier": b"o"}}},
    )
    r(
        b"SNClassifySoundRequest",
        b"setWindowDuration:",
        {"arguments": {2: {"type": b"{_CMTime=qiIq}"}}},
    )
    r(
        b"SNClassifySoundRequest",
        b"windowDuration",
        {"retval": {"type": b"{_CMTime=qiIq}"}},
    )
    r(
        b"SNTimeDurationConstraint",
        b"durationRange",
        {"retval": {"type": b"{_CMTimeRange={_CMTime=qiIq}{_CMTime=qiIq}}"}},
    )
    r(
        b"SNTimeDurationConstraint",
        b"initWithDurationRange:",
        {"arguments": {2: {"type": b"{_CMTimeRange={_CMTime=qiIq}{_CMTime=qiIq}}"}}},
    )
finally:
    objc._updatingMetadata(False)
expressions = {}

# END OF FILE
