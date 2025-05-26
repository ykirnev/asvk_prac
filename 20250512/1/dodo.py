import glob
from pathlib import Path
from doit.tools import create_folder
import tomllib

DOIT_CONFIG = {"default_tasks": ['html']}
PODEST = 'mood/po'
PROJECT_DIR = Path(__file__).parent


def dumpkeys(infile, table, outfile):
    '''Dumps TOML table keys one per line'''
    with open(infile, "rb") as fin:
        full = tomllib.load(fin)
    with open(outfile, "w") as fout:
        print(*full[table], sep="\n", file=fout)


def task_pot():
    return {
        'actions': [f'pybabel extract -o mood/po/mud.pot mood'],
        'file_dep': [str(i) for i in glob.glob('mood/server/*.py')] + [str(i) for i in glob.glob('mood/common/*.py')],
        'targets': ["mood/po/mud.pot"],
    }

def task_po():
    return {
        'actions': [f"pybabel update --init-missing --ignore-pot-creation-date -l ru -D mud -i mood/po/mud.pot -d {PODEST}"],
        'file_dep': ['mood/po/mud.pot'],
        'targets': ["mood/po/ru/LC_MESSAGES/mud.po"],
    }

def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, [f'mood/po/ru/LC_MESSAGES']),
                f'pybabel compile -D mud -l ru -i mood/po/ru/LC_MESSAGES/mud.po -d {PODEST}'
                       ],
            'file_dep': ['mood/po/ru/LC_MESSAGES/mud.po'],
            'targets': ['mood/po/ru/LC_MESSAGES/mud.mo'],
           }

def task_il8n():
    """Build il8n"""
    return {
            "file_dep": ['mood/po/ru/LC_MESSAGES/mud.po'],
            "actions": None,
            'task_dep': ['mo']
    }

def task_html():
    """Build html"""
    return {
            "actions": ["sphinx-build -M html source mood/docs"]
    }


def task_test():
    """Run tests"""
    return {
            'task_dep': ['il8n'],
            "actions": ["python3 -m unittest test_server.py", "python3 -m unittest test_client.py"],
    }


def task_erase():
    """Clean represitory"""
    return {
            'actions': ['git clean -xdf'],
    }

def task_sdist():
    """Create source distribution."""
    return {
            'actions': ['python -m build -s']
           }


def task_wheel():
    """Create binary wheel distribution."""
    return {
            'actions': ['python -m build -w'],
            'task_dep': ['mo'],
           }

def task_requirements():
    """Dump Pipfile requirements"""
    return {
            'actions': [(dumpkeys, ["Pipfile", "packages", "requirements.txt"])],
            'file_dep': ['Pipfile'],
            'targets': ['requirements.txt'],
           }

def clean_targets(task):
    for target in task.targets:
        Path(target).unlink(missing_ok=True)

def task_clean_all():
    """Полная очистка (включая документацию и кэш)"""
    return {
        'actions': [
            "rm -rf dist build *.egg-info",
            f"rm -rf {PROJECT_DIR / '_build'}",
            "find . -type d -name '__pycache__' -exec rm -rf {} +",
            "find . -type f -name '*.pyc' -delete"
        ],
        'verbosity': 2,
    }
