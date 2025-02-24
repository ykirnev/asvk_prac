import zlib
from sys import argv
from os.path import basename
from pathlib import Path


def list_branches(repo_path):
    heads_path = Path(repo_path) / '.git' / 'refs' / 'heads'
    branches = [basename(branch) for branch in heads_path.rglob('*')]
    for branch in branches:
        print(branch)


def get_last_commit(repo_path, branch_name):
    head_path = Path(repo_path) / '.git' / 'refs' / 'heads' / branch_name
    if not head_path.exists():
        print(f"Branch '{branch_name}' not found")
        return

    commit_hash = head_path.read_text().strip()
    walk_commit_history(repo_path, commit_hash)


def walk_commit_history(repo_path, commit_hash):
    while commit_hash:
        print(f"TREE for commit {commit_hash}")
        commit_hash = print_commit_object(repo_path, commit_hash)


def print_commit_object(repo_path, commit_hash):
    object_path = Path(repo_path) / '.git' / 'objects' / commit_hash[:2] / commit_hash[2:]
    if not object_path.exists():
        print(f"Commit object '{commit_hash}' not found")
        return None

    with object_path.open('rb') as f:
        decompressed_data = zlib.decompress(f.read()).decode()
        print(decompressed_data)

        tree_hash = None
        parent_hash = None

        for line in decompressed_data.splitlines():
            if line.startswith('tree'):
                tree_hash = line.split()[1]
            elif line.startswith('parent') and not parent_hash:
                parent_hash = line.split()[1]

        if tree_hash:
            print_tree_object(repo_path, tree_hash)

        return parent_hash


def print_tree_object(repo_path, tree_hash):
    object_path = Path(repo_path) / '.git' / 'objects' / tree_hash[:2] / tree_hash[2:]
    if not object_path.exists():
        print(f"Tree object '{tree_hash}' not found")
        return

    with object_path.open('rb') as f:
        decompressed_data = zlib.decompress(f.read())
        content = decompressed_data.split(b'\x00', 1)[1]

        while content:
            meta, _, content = content.partition(b'\x00')
            if not meta:
                break
            mode, name = meta.split(b' ', 1)
            sha = content[:20].hex()
            content = content[20:]
            object_type = 'tree' if mode == b'40000' else 'blob'
            print(f"{object_type} {sha} {name.decode()}")


if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: python3 prog.py <repo_path> [branch_name]")
    else:
        repo_path = argv[1]
        if len(argv) == 2:
            list_branches(repo_path)
        else:
            branch_name = argv[2]
            get_last_commit(repo_path, branch_name)