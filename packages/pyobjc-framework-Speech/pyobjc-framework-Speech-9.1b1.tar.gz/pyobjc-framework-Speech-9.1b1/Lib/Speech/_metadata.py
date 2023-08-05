# This file is generated by objective.metadata
#
# Last update: Tue Jun  7 20:17:43 2022
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
enums = """$SFSpeechRecognitionTaskHintConfirmation@3$SFSpeechRecognitionTaskHintDictation@1$SFSpeechRecognitionTaskHintSearch@2$SFSpeechRecognitionTaskHintUnspecified@0$SFSpeechRecognitionTaskStateCanceling@3$SFSpeechRecognitionTaskStateCompleted@4$SFSpeechRecognitionTaskStateFinishing@2$SFSpeechRecognitionTaskStateRunning@1$SFSpeechRecognitionTaskStateStarting@0$SFSpeechRecognizerAuthorizationStatusAuthorized@3$SFSpeechRecognizerAuthorizationStatusDenied@1$SFSpeechRecognizerAuthorizationStatusNotDetermined@0$SFSpeechRecognizerAuthorizationStatusRestricted@2$"""
misc.update(
    {
        "SFSpeechRecognitionTaskHint": NewType("SFSpeechRecognitionTaskHint", int),
        "SFSpeechRecognitionTaskState": NewType("SFSpeechRecognitionTaskState", int),
        "SFSpeechRecognizerAuthorizationStatus": NewType(
            "SFSpeechRecognizerAuthorizationStatus", int
        ),
    }
)
misc.update({})
misc.update({})
r = objc.registerMetaDataForSelector
objc._updatingMetadata(True)
try:
    r(
        b"NSObject",
        b"speechRecognitionDidDetectSpeech:",
        {"required": False, "retval": {"type": b"v"}, "arguments": {2: {"type": b"@"}}},
    )
    r(
        b"NSObject",
        b"speechRecognitionTask:didFinishRecognition:",
        {
            "required": False,
            "retval": {"type": b"v"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"@"}},
        },
    )
    r(
        b"NSObject",
        b"speechRecognitionTask:didFinishSuccessfully:",
        {
            "required": False,
            "retval": {"type": b"v"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"Z"}},
        },
    )
    r(
        b"NSObject",
        b"speechRecognitionTask:didHypothesizeTranscription:",
        {
            "required": False,
            "retval": {"type": b"v"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"@"}},
        },
    )
    r(
        b"NSObject",
        b"speechRecognitionTaskFinishedReadingAudio:",
        {"required": False, "retval": {"type": b"v"}, "arguments": {2: {"type": b"@"}}},
    )
    r(
        b"NSObject",
        b"speechRecognitionTaskWasCancelled:",
        {"required": False, "retval": {"type": b"v"}, "arguments": {2: {"type": b"@"}}},
    )
    r(
        b"NSObject",
        b"speechRecognizer:availabilityDidChange:",
        {
            "required": False,
            "retval": {"type": b"v"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"Z"}},
        },
    )
    r(b"SFSpeechRecognitionRequest", b"addsPunctuation", {"retval": {"type": b"Z"}})
    r(
        b"SFSpeechRecognitionRequest",
        b"requiresOnDeviceRecognition",
        {"retval": {"type": b"Z"}},
    )
    r(
        b"SFSpeechRecognitionRequest",
        b"setAddsPunctuation:",
        {"arguments": {2: {"type": b"Z"}}},
    )
    r(
        b"SFSpeechRecognitionRequest",
        b"setRequiresOnDeviceRecognition:",
        {"arguments": {2: {"type": b"Z"}}},
    )
    r(
        b"SFSpeechRecognitionRequest",
        b"setShouldReportPartialResults:",
        {"arguments": {2: {"type": b"Z"}}},
    )
    r(
        b"SFSpeechRecognitionRequest",
        b"shouldReportPartialResults",
        {"retval": {"type": b"Z"}},
    )
    r(b"SFSpeechRecognitionResult", b"isFinal", {"retval": {"type": b"Z"}})
    r(b"SFSpeechRecognitionTask", b"isCancelled", {"retval": {"type": b"Z"}})
    r(b"SFSpeechRecognitionTask", b"isFinishing", {"retval": {"type": b"Z"}})
    r(b"SFSpeechRecognizer", b"isAvailable", {"retval": {"type": b"Z"}})
    r(
        b"SFSpeechRecognizer",
        b"recognitionTaskWithRequest:resultHandler:",
        {
            "arguments": {
                3: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {
                            0: {"type": b"^v"},
                            1: {"type": b"@"},
                            2: {"type": b"@"},
                        },
                    }
                }
            }
        },
    )
    r(
        b"SFSpeechRecognizer",
        b"requestAuthorization:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {0: {"type": b"^v"}, 1: {"type": b"q"}},
                    }
                }
            }
        },
    )
    r(
        b"SFSpeechRecognizer",
        b"setSupportsOnDeviceRecognition:",
        {"arguments": {2: {"type": b"Z"}}},
    )
    r(b"SFSpeechRecognizer", b"supportsOnDeviceRecognition", {"retval": {"type": b"Z"}})
finally:
    objc._updatingMetadata(False)
expressions = {}

# END OF FILE
