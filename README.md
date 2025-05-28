# Virtual playground for getting reps in on platform engineering tech stacks

---

## CloudStack Homelab (via Ansible)

The provided Ansible playbook (`homelab-virtual-playground/main.yml`) automates setup of an Apache CloudStack management server in simulation mode. This avoids the need for real hypervisor nodes, making it perfect for education or testing.

### Features
- Installs all dependencies (KVM, Java, MariaDB, etc.)
- Clones and builds Apache CloudStack
- Launches the management server
- Accessible at `http://localhost:8080/client` (default credentials: `admin/password`)

### Usage
```bash
ansible-playbook main.yml
```

Make sure you're running on an Ubuntu host with KVM/libvirt enabled.

---

## Kubeflow Manifests Image Rewrite Utility (Python)

This script (`kubeflow_rewrite.py`) recursively scans Kubeflow YAML manifests and rewrites container image references to point to an internal Artifactory mirror.

### Example Use Case
When migrating ML workflows to a secured lab environment, you often need to replace public container registry links (like `quay.io/...`) with internal mirrors (like `artifactory.company.com/...`).

### How It Works
- Parses YAML manifests for `image:` and `value:` lines
- Rewrites registries based on user input
- Supports `kustomization.yaml` files
- Creates backups of all modified files

### Usage
```bash
python3 kubeflow_rewrite.py
```

At runtime, the script will prompt you to enter replacement domains for common registries:
```
quay.io replacement? artifacts.example.com/aid-quay.io
```

