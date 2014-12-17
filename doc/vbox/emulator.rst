VirtualBox Emuluator
====================

VirtualBox emulator allows to emulate a VirtualBox VM for a real proliant
bare metal. With this, proliantutils.ilo.IloClient can act as if talking
to a real iLO with RIBCL/RIS.  Not all the interfaces are supported today
and hence might raise NotImplementedError for whichever is not implemented.

Setup
-----

1. Install *pyremotevbox* module::

     pip install -U pyremotevbox

2. Create a shared folder between the VirtualBox host and the
   Linux VM acting as cloud controller. Create empty new directories on both
   VirtualBox host (let it be *<shared-directory-on-virtualbox-host>* and
   Linux VM (let it be *<mount-point-on-linux-vm>*). Add a new shared folder::

    Oracle VM VirtualBox Manager
      -> Right click on VM
      -> Settings
      -> Shared Folders
      -> Click "Adds a new shared folder" at right end of popped-up window
      -> Click Other and select the folder (C:\vbox_shared_folder in example)
      -> Provide a name in "Folder Name" as 'vbox_shared'
      -> Tick Make Permanent

3. On Linux VM install *VirtualBox Guest Additions* [1]

4. Mount the shared folder in Linux VM. For example::

     mount -t vboxsf vbox_shared /home/ubuntu/windows_shared_folder

5. In */etc/ironic/ironic.conf*, provide the following::

     [vbox_emulator]
     enabled = True
     shared_root = <location on the cloud controller guest
                    where shared folder is mounted>
     host_share_location = <location on the VirtualBox host which
                            is shared with cloud controller guest>

   For example::

     [vbox_emulator]
     enabled = True
     shared_root = /home/ubuntu/windows_shared_folder
     host_share_location = C:\\vbox_shared



References
----------
[1] https://help.ubuntu.com/community/VirtualBox/SharedFolders
