#!/usr/bin/env python3

import os
import re
import shutil
import yaml

def get_registry_map():
    registry_map = {}
    default_map = ["quay.io", "docker.io", "gcr.io", "ghcr.io"]
    print("Enter replacement for each registry (leave blank to skip):")
    for registry in default_map:
        user_input = input(f"{registry} replacement? ").strip()
        if user_input:
            registry_map[registry] = user_input
    return registry_map

# matches both explicit and implicit image references
IMAGE_LINE_REGEX = re.compile(
    r'^(\s*)(image:|value:)\s*["\']?([\w\-/.:@]+)["\']?(.*)$'
)

def add_default_registry(image):
    if '/' not in image:
        return f'docker.io/library/{image}'
    if any(image.startswith(reg + '/') for reg in IMAGE_REPO_MAP):
        return image
    return f'docker.io/{image}'

def rewrite_image(image):
    image = add_default_registry(image)
    for src, dst in IMAGE_REPO_MAP.items():
        if image.startswith(src + "/"):
            return image.replace(src, dst, 1)
    return image

def is_kustomization_file(filepath):
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return isinstance(data, dict) and 'images' in data
    except Exception:
        return False

def patch_kustomization_yaml(filepath, target_tag=None):
    try:
        with open(filepath, 'r') as f:
            content = yaml.safe_load(f)

        if not content or 'images' not in content:
            return False

        patched = False
        for img in content['images']:
            name = img.get('name') or img.get('newName')
            if name:
                name = add_default_registry(name)
                for src, dst in IMAGE_REPO_MAP.items():
                    if name.startswith(src + '/'):
                        img['newName'] = name.replace(src, dst, 1)
                        if target_tag:
                            img['newTag'] = target_tag
                        patched = True

        if patched:
            shutil.copy(filepath, filepath + ".bak")
            with open(filepath, 'w') as f:
                yaml.dump(content, f, sort_keys=False)
            print(f"Patched {filepath} (as kustomization.yaml)")
        return patched
    except Exception as e:
        print(f"Failed to patch {filepath}: {e}")
        return False

def patch_yaml_lines(filepath):
    patched = False
    new_lines = []

    with open(filepath, 'r') as f:
        for line in f:
            match = IMAGE_LINE_REGEX.match(line)
            if match:
                indent, key, image_path, rest = match.groups()

                if "# aid-skip" in rest:
                    print(f"Skipping line in {filepath} (marked with '# aid-skip')")
                    new_lines.append(line)
                    continue

                new_image = rewrite_image(image_path)
                if new_image != image_path:
                    patched = True
                    new_line = f"{indent}{key} {new_image}{rest}\n"
                    new_lines.append(new_line)
                    continue

            new_lines.append(line)

    if patched:
        shutil.copy(filepath, filepath + ".bak")
        with open(filepath, 'w') as f:
            f.writelines(new_lines)
        print(f"Patched {filepath}")
    return patched

def walk_and_patch(directory, target_tag=None):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith((".yaml", ".yml")):
                full_path = os.path.join(root, filename)
                if is_kustomization_file(full_path):
                    patch_kustomization_yaml(full_path, target_tag=target_tag)
                else:
                    patch_yaml_lines(full_path)

if __name__ == "__main__":
    IMAGE_REPO_MAP = get_registry_map()
    MANIFESTS_DIR = "/tmp/manifests"
    walk_and_patch(MANIFESTS_DIR, target_tag=None)
