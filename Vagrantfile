# Vagrantfile
# spins up an Ubuntu VM suitable for running the CloudStack Ansible playbook

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "cloudstack-lab"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 2
  end

  config.vm.network "forwarded_port", guest: 8080, host: 8080, auto_correct: true

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y ansible git
    cd /vagrant
    ansible-playbook homelab-virtual-playground/main.yml
  SHELL
end
