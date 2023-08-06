import os
import glob

from tkinter import *

from autoappanalysis.processor.Processor import Processor

from autoappanalysis.cmd.HostCommand import HostCommand
from autoappanalysis.cmd.VirtualBoxCommand import VirtualBoxCommand

class Gui():
    def __init__(self, config) -> None:
        self.config = config
        self.processor = Processor(config["log"])
        # Tk window
        self.root = Tk()
        self.root.title('AutoAppAnalysis')
        self.root.resizable(False, False)

        # Layouts
        frameLeft = Frame(self.root)
        frameLeft.grid(row=0, column=0, padx=10, pady=10)
        frameLeftBottom = Frame(self.root)
        frameLeftBottom.grid(row=1, column=0, padx=10, pady=5)
        frameLeftBottom2 = Frame(self.root)
        frameLeftBottom2.grid(row=2, column=0, padx=10, pady=5)
        frameRight = Frame(self.root)
        frameRight.grid(row=0, column=1, padx=10, pady=10)
        frameRightBottom = Frame(self.root)
        frameRightBottom.grid(row=1, column=1, padx=10, pady=0)
        frameRightBottom2 = Frame(self.root)
        frameRightBottom2.grid(row=2, column=1, padx=10, pady=0)

        # Button
        self.rootBtn = Button(frameRight, text="Root", command=self._rootAVD)
        self.rootBtn.grid(row=0, column=0, pady=2, sticky="w")
        self.createBtn = Button(frameRight, text="Create Snapshot", command=self._createSnapshot)
        self.createBtn.grid(row=1, column=0, pady=2, sticky="w")
        self.decryptBtn = Button(frameRight, text="Decrypt Snapshots", command=self._decryptSnapshots)
        self.decryptBtn.grid(row=2, column=0, pady=2, sticky="w")
        self.createIdiffBtn = Button(frameRight, text="Create .idiff", command=self._createIdiff)
        self.createIdiffBtn.grid(row=3, column=0, pady=2, sticky="w")
        self.analyseIdiffBtn = Button(frameRight, text="Analyse .idiff", command=self._analyseIdiff)
        self.analyseIdiffBtn.grid(row=4, column=0, pady=2, sticky="w")
        self.analyseDbBtn = Button(frameRight, text="Analyse .db", command=self._analyseDb)
        self.analyseDbBtn.grid(row=5, column=0, pady=2, sticky="w")
        self.uninstallBtn = Button(frameRight, text="Uninstall", command=self._uninstall)
        self.uninstallBtn.grid(row=6, column=0, pady=2, sticky="w")
        
        self.extractBtn = Button(frameRightBottom, text="Extract Files", command=self._extractFiles)
        self.extractBtn.grid(row=0, column=0, pady=2, sticky="w")
        self.searchBtn = Button(frameRightBottom2, text="Search Files", command=self._searchFiles)
        self.searchBtn.grid(row=0, column=0, pady=2, sticky="w")

        # Text
        self.labelVm = Label(frameLeft, text='VM Name:')
        self.labelVm.grid(row=0, column=0, sticky="w")
        self.vmTxt = Text(frameLeft, height = 1, width = 20)
        self.vmTxt.insert('1.0', config["vm"])
        self.vmTxt.grid(row=1, column=0)
        
        self.labelUser = Label(frameLeft, text='VM User Name:')
        self.labelUser.grid(row=0, column=1, sticky="w")
        self.userTxt = Text(frameLeft, height = 1, width = 20)
        self.userTxt.insert('1.0', config["user"])
        self.userTxt.grid(row=1, column=1)
        
        self.labelPw = Label(frameLeft, text='VM Password:')
        self.labelPw.grid(row=0, column=2, sticky="w")
        self.pwTxt = Text(frameLeft, height = 1, width = 20)
        self.pwTxt.insert('1.0', config["pw"])
        self.pwTxt.grid(row=1, column=2)

        self.labelInputDir = Label(frameLeft, text='VM Input Directory:')
        self.labelInputDir.grid(row=2, column=0, sticky="w")
        self.inputTxt = Text(frameLeft, height = 1, width = 20)
        self.inputTxt.insert('1.0', config["input"])
        self.inputTxt.grid(row=3, column=0)

        self.labelOutputDir = Label(frameLeft, text='VM Output Directory:')
        self.labelOutputDir.grid(row=2, column=1, sticky="w")
        self.outputTxt = Text(frameLeft, height = 1, width = 20)
        self.outputTxt.insert('1.0', config["output"])
        self.outputTxt.grid(row=3, column=1)

        self.labelhOutputDir = Label(frameLeft, text='Host Output Directory:')
        self.labelhOutputDir.grid(row=2, column=2, sticky="w")
        self.hOutputTxt = Text(frameLeft, height = 1, width = 20)
        self.hOutputTxt.insert('1.0', config["outputHost"])
        self.hOutputTxt.grid(row=3, column=2)

        self.labelAvdPath = Label(frameLeft, text='AVD Path:')
        self.labelAvdPath.grid(row=4, column=0, sticky="w")
        self.avdPathTxt = Text(frameLeft, height = 1, width = 20)
        self.avdPathTxt.insert('1.0', config["snapshot"])
        self.avdPathTxt.grid(row=5, column=0)

        self.labelSName = Label(frameLeft, text='Snapshot Name:')
        self.labelSName.grid(row=4, column=1, sticky="w")
        self.sNameTxt = Text(frameLeft, height = 1, width = 20)
        self.sNameTxt.insert('1.0', "snap")
        self.sNameTxt.grid(row=5, column=1)

        self.labelSNumber = Label(frameLeft, text='Snapshot Number:')
        self.labelSNumber.grid(row=4, column=2, sticky="w")
        self.sNumberTxt = Text(frameLeft, height = 1, width = 20)
        self.sNumberTxt.insert('1.0', "1")
        self.sNumberTxt.grid(row=5, column=2)

        self.labelPkgName = Label(frameLeft, text='App Package Name:')
        self.labelPkgName.grid(row=6, column=0, sticky="w")
        self.pkgNameTxt = Text(frameLeft, height = 1, width = 20)
        self.pkgNameTxt.insert('1.0', config["pkgName"])
        self.pkgNameTxt.grid(row=7, column=0)

        self.labelExtractFiles = Label(frameLeftBottom, text='AVD Files to be extracted:')
        self.labelExtractFiles.grid(row=6, column=0, sticky="w")
        self.extFilesTxt = Text(frameLeftBottom, height = 15, width = 60)
        
        for file in config["files"]:
            self.extFilesTxt.insert(END, file + "\n")
        self.extFilesTxt.grid(row=7, column=0)

        self.labelSearchFiles = Label(frameLeftBottom2, text='Files to be searched:')
        self.labelSearchFiles.grid(row=6, column=0, sticky="w")
        self.searchFilesTxt = Text(frameLeftBottom2, height = 15, width = 60)

        for file in config["search"]["files"]:
            self.searchFilesTxt.insert(END, file + "\n")
        self.searchFilesTxt.grid(row=7, column=0)

    def _rootAVD(self):
        cmd = HostCommand.ADB_ROOT
        cmdResult = self.processor.process(cmd)
        print(cmdResult)

    def _extractFiles(self):
        outputHost = self.hOutputTxt.get("1.0", "end-1c")
        sName = self.sNameTxt.get("1.0", "end-1c")
        sNumber = self.sNumberTxt.get("1.0", "end-1c")
        paths_ = self.extFilesTxt.get("1.0", "end-1c")
        files = paths_.split("\n")
        hostPath = outputHost + "\\files\\" + sName + "." + sNumber

        if(not os.path.isdir(hostPath)):
            os.mkdir(hostPath)

        for file in files: 
            if(file != ""):
                fileName = file.strip('/').strip('\\').split('/')[-1].split('\\')[-1]
                destPath = hostPath + "\\" + fileName
                cmd = HostCommand.ADB_PULL.substitute(androidPath=file, hostPath=destPath)
                cmdResult = self.processor.process(cmd)
                print(cmdResult)

    def _createSnapshot(self):
        name_ = self.sNameTxt.get("1.0", "end-1c")
        number = self.sNumberTxt.get("1.0", "end-1c")
        self.processor.logInfo("--> Snapshot Creation started!")

        cmd = HostCommand.ADB_SNAPSHOT_SAVE.substitute(name=name_ + "." + number)
        cmdResult = self.processor.process(cmd)
        print(cmdResult)
        self._extractFiles()

        self.processor.logInfo("--> Snapshot Creation finished!")
        print("\n --> Snapshot created \n")

    def _getSnapshotList(self):
        snapshots = []
        avdDir = self.avdPathTxt.get("1.0", "end-1c")
        for path, dirs, files in os.walk(os.path.join(avdDir, "snapshots"), topdown=False):
            for name in dirs:
                if("default_boot" not in name):
                    snapshots.append(name)
        return snapshots
    
    def _decryptSnapshots(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        avdPath = self.inputTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c") + "/decrypted"
        outputHost = self.hOutputTxt.get("1.0", "end-1c") + "\\decrypted"
        snapshots = self._getSnapshotList()

        self.processor.logInfo("--> Snapshot Decryption started!")
        for snapshot in snapshots:
            fullPath = outputHost + "\\" + snapshot + ".raw"
            if(os.path.isfile(fullPath) == False):
                py = "/usr/bin/python3"
                avdecrypt = "/home/" + user + "/scripts/avdecrypt/avdecrypt.py"
                params = "-a " + avdPath + " -s " + snapshot + " -o " + outputDir
                args = py + " " + avdecrypt + " " + params

                cmd = VirtualBoxCommand.GUEST_CONTROL_PARAM.substitute(vmName=vm, user=user, pw=pw, path=py, args=args)
                self.processor.logInfo("Decrypt " + snapshot)
                cmdResult = self.processor.process(cmd)
                print(cmdResult)
            else:
                self.processor.logWarn(fullPath + " already decrypted!")

        for path, dirs, files in os.walk(outputHost, topdown=False):
            for file in files:
                if(".enc" in file):
                    fileToBeRemoved = os.path.join(path, file)
                    os.remove(fileToBeRemoved)
                    self.processor.logInfo(fileToBeRemoved + " removed successfully!")

        self.processor.logInfo("--> Snapshot Decryption finished!")
        print("\n --> Decryption finished \n")
 

    def _createIdiff(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c")
        decryptedDir = outputDir + "/decrypted"
        snapshots = self._getSnapshotList()
        outputHost = self.hOutputTxt.get("1.0", "end-1c")

        print("\n --> .idiff Creation started! \n")
        self.processor.logInfo("--> .idiff Creation started!")

        py = "/usr/bin/python3"
        dfxml = "/home/" + user + "/scripts/dfxml_python/dfxml/bin/idifference2.py"

        for comparison in self.config["comparison"]:
            resultPath = outputHost + "\\actions\\" + comparison["name"] 
            firstSnapshot = comparison["first"]
            secondSnapshots = comparison["second"]
            noise = comparison["noise"]

            if(not os.path.isdir(resultPath)):
                os.mkdir(resultPath)
                os.mkdir(resultPath + "\\ge")

            # Compare Snapshots
            for snapshotName in secondSnapshots:
                snList = [i for i in snapshots if snapshotName == i.split(".")[0]]
                for snapshot in snList:
                    before = decryptedDir + "/" + firstSnapshot + ".1.raw"
                    after = decryptedDir + "/" + snapshot + ".raw"
                    target = resultPath + "\\ge\\" + snapshot + ".idiff"
                    args = py + " " + dfxml + " " + before + " " + after + " > " + target
                    cmd = VirtualBoxCommand.GUEST_CONTROL_PARAM.substitute(vmName=vm, user=user, pw=pw, path=py, args=args)
                    cmdResult = self.processor.process(cmd)
                    print(cmdResult)

            # Compare Noise
            before = decryptedDir + "/" + firstSnapshot + ".1.raw"
            after = decryptedDir + "/" + noise + ".1.raw"
            target = resultPath + "\\ge\\" + noise + ".1.idiff"
            args = py + " " + dfxml + " " + before + " " + after + " > " + target
            cmd = VirtualBoxCommand.GUEST_CONTROL_PARAM.substitute(vmName=vm, user=user, pw=pw, path=py, args=args)
            cmdResult = self.processor.process(cmd)
            print(cmdResult)
        
        self.processor.logInfo("--> .idiff Creation finished!")
        print("\n --> *.idiff created \n")

    def _analyseIdiff(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c")
        actionsDir = self.hOutputTxt.get("1.0", "end-1c") + "\\" + "actions"
        py = "/usr/bin/python3"
        evidence = "-m evidence"
        
        self.processor.logInfo("--> .idiff Analysis started!")
        print("\n --> .idiff Analysis started! \n")
        for dir in os.listdir(actionsDir):
            noiseName = ""
            for c in self.config["comparison"]:
                if(c["name"] == dir):
                    noiseName = c["noise"]
            argsP = "-p " + outputDir + "/actions/" + dir + "/ge" 
            argsO = "-o " + outputDir + "/actions/" + dir + "/output"
            argsN = "-n " + noiseName
            args = py + " " + evidence + " " + argsP + " " + argsO + " " + argsN

            if(not os.path.isdir(actionsDir + "\\" + dir + "\\output")):
                os.mkdir(actionsDir + "\\" + dir + "\\output")

            cmd = VirtualBoxCommand.GUEST_CONTROL_PARAM.substitute(vmName=vm, user=user, pw=pw, path=py, args=args)
            cmdResult = self.processor.process(cmd)
            print(cmdResult)

        self.processor.logInfo("--> .idiff Analysis finished!")
        print("\n --> *.idiff Analysis finished! \n")
            
    def _analyseDb(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c")
        outputHost = self.hOutputTxt.get("1.0", "end-1c")
        paths_ = self.extFilesTxt.get("1.0", "end-1c")
        files_ = paths_.split("\n")
        hostPath = outputHost + "\\files\\"
        py = "/usr/bin/python3"
        sqlitediff = "-m sqlitediff"
        sqliteview = "-m sqliteview"

        self.processor.logInfo("--> .db Analysis started!")
        print("\n --> .db Analysis started! \n")

        # SQLite View
        for path, dirs, files in os.walk(hostPath):
            for file in files:
                fName = self._getFileName(file)
                parts = fName.split(".")
                if(parts[-1] == "db"):
                    p = os.path.join(path, file)
                    target = p + ".sqliteview"
                    argsP = "-p " + self._winPathToLinPath(p)
                    args = py + " " + sqliteview + " " + argsP + " > " + target
                    cmd = VirtualBoxCommand.GUEST_CONTROL_PARAM.substitute(vmName=vm, user=user, pw=pw, path=py, args=args)
                    cmdResult = self.processor.process(cmd)
                    print(cmdResult)

        # SQLite Diff
        for comparison in self.config["comparison"]:
            firstSnapshot = comparison["first"]
            secondSnapshots = comparison["second"]

            for file_ in files_:
                if(file_ != ""):
                    fileName = self._getFileName(file_)
                    if(".db" in fileName):
                          
                        firstSnapshotFullPath = hostPath + firstSnapshot + ".1" + "\\" + fileName

                        for sSnap in secondSnapshots:
                            sSnapPath = hostPath + sSnap + ".1" + "\\"
                            sSnapFullPath = sSnapPath + fileName
                            bPath = self._winPathToLinPath(firstSnapshotFullPath)
                            aPath = self._winPathToLinPath(sSnapFullPath)
                            bPathIsFile = False
                            aPathIsFile = False
                            if(os.path.isfile(firstSnapshotFullPath)):
                                bPathIsFile = True
                            if(os.path.isfile(sSnapFullPath)):
                                aPathIsFile = True

                            if(bPathIsFile and aPathIsFile):
                                argsb = "-b " + bPath
                                argsa = "-a " + aPath
                                args = py + " " + sqlitediff + " " + argsb + " " + argsa + " > " + sSnapPath + firstSnapshot + "." + sSnap + "." + fileName + ".sqlitediff"
                                cmd = VirtualBoxCommand.GUEST_CONTROL_PARAM.substitute(vmName=vm, user=user, pw=pw, path=py, args=args)
                                cmdResult = self.processor.process(cmd)
                                print(cmdResult)
                            elif(bPathIsFile and not aPathIsFile):
                                self.processor.logWarn(bPath + " available (before) | " + aPath + " not available (after)")
                            elif(aPathIsFile and not bPathIsFile):
                                self.processor.logWarn(bPath + " not available (before) | " + aPath + " available (after)")
                            elif(not aPathIsFile and not bPathIsFile):
                                self.processor.logWarn("no .db file found")


        self.processor.logInfo("--> .db Analysis finished!")
        print("\n --> *.db Analysis finished! \n")

    def _uninstall(self):
        pkgName = self.pkgNameTxt.get("1.0", "end-1c")
        self.processor.logInfo("--> Uninstall started!")

        cmd = HostCommand.ADB_UNINSTALL.substitute(packageName=pkgName)
        cmdResult = self.processor.process(cmd)
        print(cmdResult)

        self.processor.logInfo("--> Uninstall finished!")


    def _searchFiles(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c")
        actionsDir = self.hOutputTxt.get("1.0", "end-1c") + "\\" + "actions"
        py = "/usr/bin/python3"
        lineident = "-m lineident"
        paths_ = self.searchFilesTxt.get("1.0", "end-1c")
        files = paths_.split("\n")

        self.processor.logInfo("--> Keyword Search started!")
        print("\n --> Keyword Search started! \n")
        for file in files:
            globedFiles = glob.glob(file)
            for f in globedFiles:
                path = self._winPathToLinPath(f)
                argsP = "-p " + path
                for searchAction in self.config["search"]["actions"]:
                    argsM = "-m " + searchAction["method"] 
                    argsW = "-w " + searchAction["words"]
                    argsF = "-f " + searchAction["format"]
                    out = "> " + f + "." + searchAction["name"].replace(" ", "_") + ".lineident.txt"
                    args = py + " " + lineident + " " + argsP + " " + argsM + " " + argsW + " " + argsF + " " + out
                    cmd = VirtualBoxCommand.GUEST_CONTROL_PARAM.substitute(vmName=vm, user=user, pw=pw, path=py, args=args)
                    cmdResult = self.processor.process(cmd)
                    print(cmdResult)
                print("---")
                

        self.processor.logInfo("--> Keyword Search finished!")
        print("\n --> Keyword Search finished! \n")

    def _getFileName(self, path):
        return path.strip('/').strip('\\').split('/')[-1].split('\\')[-1]

    def _processSnapshots(self):
      pass

    def _winPathToLinPath(self, winPath):
        outputDir = self.outputTxt.get("1.0", "end-1c")
        linPath = winPath.rsplit("results")[1].replace("\\", "/")
        return outputDir + linPath

    def start(self):
        self.root.mainloop()