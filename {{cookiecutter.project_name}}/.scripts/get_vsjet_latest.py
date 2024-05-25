import subprocess
import os
from pathlib import Path
import git

VSJET_PACKAGES = [
    'tools',
    'pyplugin',
    'kernels',
    'exprtools',
    'rgtools',
    'masktools',
    'aa',
    'scale',
    'denoise',
    'dehalo',
    'deband',
    'deinterlace',
    'source'
]

GITHUB_BASE_URL = "https://github.com/Jaded-Encoding-Thaumaturgy/{package}.git"


def run_command(command: list[str], exit_on_error: bool = True) -> str:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    output = []

    try:
        for line in process.stdout:  # type:ignore
            print(line, end='')
            output.append(line)

        process.wait()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)

    except subprocess.CalledProcessError:
        if exit_on_error:
            print(f"Command '{' '.join(command)}' ran into an error.")
            raise

    return ''.join(output)


def lsremote(url: str) -> dict[str, str]:
    remote_refs = {}

    g = git.cmd.Git()

    for ref in g.ls_remote(url).split('\n'):
        hash_ref_list = str(ref).split('\t')
        remote_refs[hash_ref_list[1]] = hash_ref_list[0]

    return remote_refs


def main() -> None:
    project_dir = Path.cwd()
    os.chdir(project_dir)

    run_command(['poetry', 'remove', 'vsjet'])

    for package in VSJET_PACKAGES:
        package_name = f'vs{package}'
        remote_url = GITHUB_BASE_URL.format(package=f"vs-{package}")

        head = lsremote(remote_url)['HEAD']
        git_url = f'git+{remote_url}@{head}'

        run_command(['poetry', 'remove', package_name], exit_on_error=False)
        run_command(['poetry', 'add', git_url])


if __name__ == "__main__":
    main()
