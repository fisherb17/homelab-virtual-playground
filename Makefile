# Makefile for homelab-virtual-playground

.PHONY: all help vagrant-up vagrant-destroy ansible-run test clean

help:
	@echo "Available commands:"
	@echo "  make vagrant-up       # Start Vagrant VM and provision CloudStack"
	@echo "  make vagrant-destroy  # Destroy Vagrant VM"
	@echo "  make ansible-run      # Run Ansible playbook locally"
	@echo "  make test             # Run Python tests (placeholder)"
	@echo "  make clean            # Remove backups and temporary files"

vagrant-up:
	vagrant up

vagrant-destroy:
	vagrant destroy -f

ansible-run:
	ansible-playbook homelab-virtual-playground/main.yml -i localhost,
	touch .ansible-success

# Placeholder for future test coverage
test:
	@echo "Running Python unit tests (future placeholder)"
	pytest tests/

clean:
	rm -f **/*.bak
	rm -f .ansible-success
	find . -name '__pycache__' -exec rm -r {} + || true
