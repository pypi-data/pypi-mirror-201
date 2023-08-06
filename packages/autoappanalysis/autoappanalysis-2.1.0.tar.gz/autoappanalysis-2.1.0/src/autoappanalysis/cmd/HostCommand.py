from string import Template

class HostCommand():
    ADB_ROOT = "adb root"
    ADB_PULL = Template("adb pull $androidPath $hostPath")
    ADB_SNAPSHOT_SAVE = Template("adb emu avd snapshot save $name")
    ADB_UNINSTALL = Template("adb uninstall $packageName")