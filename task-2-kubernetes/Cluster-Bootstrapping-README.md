## Task  2 — Kubernetes Cluster Setup (Vagrant + KVM/libvirt + k3s)
### 🧠 Overview

#### project provisions a self-managed Kubernetes cluster using:

Ubuntu 24.04 (host OS)
Vagrant
KVM / libvirt
k3s (lightweight Kubernetes distribution)

#### Cluster topology:

1 × control-plane node
1 × worker node

### Phase 1: Install the VM tooling

``` bash 
sudo apt update
sudo apt install -y \
qemu-kvm \
libvirt-daemon-system \
libvirt-clients \
virtinst \
bridge-utils
```

### Phase 2: Install Vagrant
``` bash 
wget -qO- https://apt.releases.hashicorp.com/gpg \
  | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update
sudo apt install -y vagrant
```

### Phase 3: Install the vagrant plugin for libvirt

``` bash
vagrant plugin install vagrant-libvirt
```

### to verify the installation of the plugin, run the following commands:

``` bash
virsh list --all
vagrant --version
```

### run the following command to start the VMs
``` bash
vagrant up  
```
the output should be similar to the following:

``` bash
omar@omar-kubuntu:/media/omar/01DADC72FB780420/Projects/DevSecOps-Cyshield-assessment/task-2-kubernetes$ vagrant up
Bringing machine 'control-plane' up with 'libvirt' provider...
Bringing machine 'worker-1' up with 'libvirt' provider...
[fog][WARNING] Unrecognized arguments: libvirt_ip_command
==> worker-1: Box 'generic/ubuntu2204' could not be found. Attempting to find and install...
    worker-1: Box Provider: libvirt
    worker-1: Box Version: >= 0
[fog][WARNING] Unrecognized arguments: libvirt_ip_command
==> worker-1: Loading metadata for box 'generic/ubuntu2204'
    worker-1: URL: https://vagrantcloud.com/api/v2/vagrant/generic/ubuntu2204
==> worker-1: Adding box 'generic/ubuntu2204' (v4.3.12) for provider: libvirt (amd64)
    worker-1: Downloading: https://vagrantcloud.com/generic/boxes/ubuntu2204/versions/4.3.12/providers/libvirt/amd64/vagrant.box
==> worker-1: Box download is resuming from prior download progress
    worker-1: Calculating and comparing box checksum...
==> worker-1: Successfully added box 'generic/ubuntu2204' (v4.3.12) for 'libvirt (amd64)'!
==> control-plane: Box 'generic/ubuntu2204' could not be found. Attempting to find and install...
    control-plane: Box Provider: libvirt
    control-plane: Box Version: >= 0
==> worker-1: Uploading base box image as volume into Libvirt storage...
Progress: 31%==> control-plane: Loading metadata for box 'generic/ubuntu2204'
    control-plane: URL: https://vagrantcloud.com/api/v2/vagrant/generic/ubuntu2204
Progress: 35%==> control-plane: Adding box 'generic/ubuntu2204' (v4.3.12) for provider: libvirt (amd64)
==> worker-1: Creating image (snapshot of base box volume).
==> control-plane: Creating image (snapshot of base box volume).
==> worker-1: Creating domain with the following settings...
==> control-plane: Creating domain with the following settings...
==> worker-1:  -- Name:              task-2-kubernetes_worker-1
==> control-plane:  -- Name:              task-2-kubernetes_control-plane
==> worker-1:  -- Description:       Source: /media/omar/01DADC72FB780420/Projects/DevSecOps-Cyshield-assessment/task-2-kubernetes/Vagrantfile
==> control-plane:  -- Description:       Source: /media/omar/01DADC72FB780420/Projects/DevSecOps-Cyshield-assessment/task-2-kubernetes/Vagrantfile
==> worker-1:  -- Domain type:       kvm
==> control-plane:  -- Domain type:       kvm
==> worker-1:  -- Cpus:              1
==> control-plane:  -- Cpus:              1
==> worker-1:  -- Feature:           acpi
==> control-plane:  -- Feature:           acpi
==> worker-1:  -- Feature:           apic
==> control-plane:  -- Feature:           apic
==> worker-1:  -- Feature:           pae
==> control-plane:  -- Feature:           pae
==> worker-1:  -- Clock offset:      utc
==> control-plane:  -- Clock offset:      utc
==> worker-1:  -- Memory:            1024M
==> control-plane:  -- Memory:            1024M
==> worker-1:  -- Base box:          generic/ubuntu2204
==> control-plane:  -- Base box:          generic/ubuntu2204
==> worker-1:  -- Storage pool:      default
==> control-plane:  -- Storage pool:      default
==> worker-1:  -- Image(vda):        /var/lib/libvirt/images/task-2-kubernetes_worker-1.img, virtio, 128G
==> control-plane:  -- Image(vda):        /var/lib/libvirt/images/task-2-kubernetes_control-plane.img, virtio, 128G
==> worker-1:  -- Disk driver opts:  cache='default'
==> control-plane:  -- Disk driver opts:  cache='default'
==> worker-1:  -- Graphics Type:     vnc
==> control-plane:  -- Graphics Type:     vnc
==> worker-1:  -- Video Type:        cirrus
==> worker-1:  -- Video VRAM:        256
==> control-plane:  -- Video Type:        cirrus
==> worker-1:  -- Video 3D accel:    false
==> control-plane:  -- Video VRAM:        256
==> worker-1:  -- Keymap:            en-us
==> control-plane:  -- Video 3D accel:    false
==> worker-1:  -- TPM Backend:       passthrough
==> control-plane:  -- Keymap:            en-us
==> worker-1:  -- INPUT:             type=mouse, bus=ps2
==> control-plane:  -- TPM Backend:       passthrough
==> control-plane:  -- INPUT:             type=mouse, bus=ps2
==> worker-1: Creating shared folders metadata...
==> control-plane: Creating shared folders metadata...
==> worker-1: Starting domain.
==> control-plane: Starting domain.
==> worker-1: Domain launching with graphics connection settings...
==> control-plane: Domain launching with graphics connection settings...
==> worker-1:  -- Graphics Port:      5900
==> control-plane:  -- Graphics Port:      5901
==> worker-1:  -- Graphics IP:        127.0.0.1
==> control-plane:  -- Graphics IP:        127.0.0.1
==> worker-1:  -- Graphics Password:  Not defined
==> control-plane:  -- Graphics Password:  Not defined
==> worker-1:  -- Graphics Websocket: 5700
==> control-plane:  -- Graphics Websocket: 5701
==> worker-1: Waiting for domain to get an IP address...
==> control-plane: Waiting for domain to get an IP address...
==> worker-1: Waiting for machine to boot. This may take a few minutes...
==> control-plane: Waiting for machine to boot. This may take a few minutes...
    worker-1: SSH address: 192.168.121.6:22
    control-plane: SSH address: 192.168.121.224:22
    worker-1: SSH username: vagrant
    control-plane: SSH username: vagrant
    worker-1: SSH auth method: private key
    control-plane: SSH auth method: private key
    worker-1: Warning: Connection refused. Retrying...
    worker-1: Vagrant insecure key detected. Vagrant will automatically replace
    worker-1: this with a newly generated keypair for better security.
    control-plane: 
    control-plane: Vagrant insecure key detected. Vagrant will automatically replace
    control-plane: this with a newly generated keypair for better security.
    worker-1: 
    worker-1: Inserting generated public key within guest...
    worker-1: Removing insecure key from the guest if it's present...
    control-plane: 
    control-plane: Inserting generated public key within guest...
    worker-1: Key inserted! Disconnecting and reconnecting using new SSH key...
    control-plane: Removing insecure key from the guest if it's present...
==> worker-1: Machine booted and ready!
==> worker-1: Setting hostname...
    control-plane: Key inserted! Disconnecting and reconnecting using new SSH key...
==> control-plane: Machine booted and ready!
==> control-plane: Setting hostname...
==> worker-1: Configuring and enabling network interfaces...
==> control-plane: Configuring and enabling network interfaces...
```

## to check the status of the VMs, run the following command:

``` bash
omar@omar-kubuntu:/media/omar/01DADC72FB780420/Projects/DevSecOps-Cyshield-assessment/task-2-kubernetes$ vagrant global-status
id       name          provider state   directory                                                                             
------------------------------------------------------------------------------------------------------------------------------
3b79019  worker-1      libvirt running /media/omar/01DADC72FB780420/Projects/DevSecOps-Cyshield-assessment/task-2-kubernetes 
94005a4  control-plane libvirt running /media/omar/01DADC72FB780420/Projects/DevSecOps-Cyshield-assessment/task-2-kubernetes 
```

### SSH into the control-plane node and install k3s using the following command:  


``` bash
vagrant ssh control-plane
curl -sfL https://get.k3s.io | sh -

sudo cat \
/var/lib/rancher/k3s/server/node-token
```

### SSH into the worker-1 node and install k3s agent using the following command (replace <TOKEN> with the token you got from the control-plane node):  

``` bash
curl -sfL https://get.k3s.io | \
K3S_URL=https://192.168.56.10:6443 \
K3S_TOKEN='<TOKEN>' \
sh -
```

### to check the status of the nodes, run the following command on the control-plane node:

``` bash
vagrant@control-plane:~$ sudo kubectl get nodes
NAME            STATUS     ROLES           AGE     VERSION
control-plane   NotReady   control-plane   8m30s   v1.35.5+k3s1
worker-1        Ready      <none>          73s     v1.35.5+k3s1
```


### get kubectl config from the control-plane node and save it to your local machine to be able to access the cluster from your local machine but use correct ip address of the control-plane node instead of 127.0.0.1:

``` bash
vagrant@control-plane:~$ sudo cat /etc/rancher/k3s/k3s.yaml
``` 

![alt text](images/image.png)
