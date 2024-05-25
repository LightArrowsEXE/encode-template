import os
import subprocess
from pathlib import Path


def main() -> None:
    """Additional setup for the project using Poetry."""

    project_dir = Path.cwd()
    os.chdir(project_dir)

    print("\nSetting up project...\n")

    # Install dependencies
    try:
        subprocess.run(['poetry', 'install'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command 'poetry install' failed with error: {e}")
        return

    # Generate Vapoursynth stubs
    try:
        subprocess.run(['vsgenstubs4'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command 'vsgenstubs4' failed with error: {e}")


if __name__ == "__main__":
    main()
