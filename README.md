# Virtual playground for getting reps in on platform engineering tech stacks

---

## CloudStack Homelab (via Ansible)

The provided Ansible playbook (`homelab-virtual-playground/main.yml`) automates the setup of an Apache CloudStack management server in simulation mode.

### Features
- Installs all dependencies (KVM, Java, MariaDB, etc.)
- Clones and builds Apache CloudStack from source
- Launches CloudStack in simulation mode
- UI accessible at `http://localhost:8080/client` (default credentials: `admin/password`)

### Usage
```bash
ansible-playbook homelab-virtual-playground/main.yml
```

Requires Ubuntu host with KVM/libvirt enabled.

---

## Kubeflow Manifests Image Rewrite Utility (Python)

This script (`kubeflow_rewrite.py`) recursively scans Kubernetes YAML manifests and rewrites container image references to point to user-defined internal mirrors (e.g., Artifactory).

### Use Case
Secure lab environments often require container images to be pulled from internal mirrors instead of public registries.

### How It Works
- Prompts user to specify replacements for: `quay.io`, `docker.io`, `gcr.io`, `ghcr.io`
- Recursively rewrites `image:` and `value:` lines
- Supports `kustomization.yaml`-style image declarations
- Creates `.bak` backups of every file modified

### Usage
```bash
python3 kubeflow_rewrite.py
```

---

## Vagrant Integration

A `Vagrantfile` is included to help you launch a pre-provisioned Ubuntu VM capable of running the homelab ansible playbook.

### Usage
```bash
make vagrant-up
```

Or directly:
```bash
vagrant up
```

---

## Cloud-Init Bootstrap

If you’re launching your own VM using Multipass or another cloud-native hypervisor, use the `cloud-init/user-data.yaml` file to auto-install Ansible and kick off the CloudStack setup.

---

## GitHub Actions CI

includes a GitHub Actions workflow (`.github/workflows/cloudstack-ci.yml`) that automatically:
- Lints your Ansible playbook
- Performs syntax validation


---

## Makefile Automation

The `Makefile` wraps common tasks:

### Available Commands
```bash
make help              # View all commands
make vagrant-up        # Launch and provision Vagrant VM
make ansible-run       # Run Ansible playbook locally
make test              # Placeholder for pytest
make clean             # Remove backup/temp files
```

