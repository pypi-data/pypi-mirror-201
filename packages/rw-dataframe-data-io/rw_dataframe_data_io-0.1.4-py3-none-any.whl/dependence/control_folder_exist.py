from pathlib import Path


def create_parent_dirs_if_not_exists(file_path):
    print("je crée un dossier")
    parent_dir = Path(file_path).parent
    parent_dir.mkdir(parents=True, exist_ok=True)

