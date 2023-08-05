# This file is generated by objective.metadata
#
# Last update: Sun Feb 20 18:55:13 2022
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
constants = """$InstallerState_Choice_CustomLocation$InstallerState_Choice_Identifier$InstallerState_Choice_Installed$"""
enums = """$InstallerDirectionBackward@1$InstallerDirectionForward@0$InstallerDirectionUndefined@2$"""
misc.update({"InstallerSectionDirection": NewType("InstallerSectionDirection", int)})
misc.update({})
r = objc.registerMetaDataForSelector
objc._updatingMetadata(True)
try:
    r(b"InstallerPane", b"gotoNextPane", {"retval": {"type": "Z"}})
    r(b"InstallerPane", b"gotoPreviousPane", {"retval": {"type": "Z"}})
    r(b"InstallerPane", b"nextEnabled", {"retval": {"type": "Z"}})
    r(b"InstallerPane", b"previousEnabled", {"retval": {"type": "Z"}})
    r(b"InstallerPane", b"setNextEnabled:", {"arguments": {2: {"type": "Z"}}})
    r(b"InstallerPane", b"setPreviousEnabled:", {"arguments": {2: {"type": "Z"}}})
    r(b"InstallerPane", b"shouldExitPane:", {"retval": {"type": "Z"}})
    r(b"InstallerSection", b"gotoPane:", {"retval": {"type": "Z"}})
    r(b"InstallerSection", b"shouldLoad", {"retval": {"type": "Z"}})
    r(b"InstallerState", b"installStarted", {"retval": {"type": "Z"}})
    r(b"InstallerState", b"installSucceeded", {"retval": {"type": "Z"}})
    r(b"InstallerState", b"licenseAgreed", {"retval": {"type": "Z"}})
finally:
    objc._updatingMetadata(False)
expressions = {}

# END OF FILE
