from pathlib import Path

def task_docs():
    """Build docs"""
    return {
            "file_dep" : [*Path(".").glob("*.py"), *Path(".").glob("*.rst")],
            "actions" : ["sphinx-build -M html . _build"],
    }

def task_zip():
    """ZipZZZZip"""
    return {
        "actions":[ "zip -r docs.zip _build/html"]
    }
def task_erase():
    """ Eraze everything"""
    return {
            "actions" : ["git reset --hard", "git clean -xdf"]
    }

