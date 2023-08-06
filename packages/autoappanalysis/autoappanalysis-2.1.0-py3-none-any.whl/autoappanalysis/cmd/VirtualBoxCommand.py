from string import Template

class VirtualBoxCommand():
    VM_START = Template("VBoxManage startvm $vmName --type headless")
    SHARED_FOLDER_ADD = Template("VBoxManage sharedfolder add $vmName --name $hostShareName --hostpath $hostPath --automount")
    GUEST_CONTROL = Template("VBoxManage guestcontrol $vmName run --username $user --password $pw --exe $path --wait-stdout --wait-stderr")
    GUEST_CONTROL_PARAM = Template("VBoxManage guestcontrol $vmName run --username $user --password $pw --exe $path --wait-stdout --wait-stderr --putenv PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin -- $args")