# Cookiecutter Encode Template

A cookiecutter template file for my usual encoding setups.

## Installation

To create a new project using this cookiecutter template,
you need to have `cookiecutter` installed.
If you don't have it installed yet,
you can install it using pip:

```shell
pip install cookiecutter
```

or,
as recommended by cookiecutter's developers themselves,
use pipx to install it:

```shell
pip install pipx
pipx install cookiecutter
```

## Usage

1. Create a new project using this template by running the following command:

   ```shell
   cookiecutter https://github.com/LightArrowsEXE/encode-template.git
   ```

   If you've already run the previous command before,
   you can use the template again with the following command:

   ```shell
   cookiecutter encode-template
   ```

   To update that template, run the first command again.

2. Follow the prompts to provide the necessary information for your project, such as the project name.
3. Navigate to the newly created project directory based on the project name you've given.<br>
   (Optional) Run `poetry exec get-vsjet-latest` to get the latest `vs-jet` packages.
4. Adjust `example_S01E01.py` and the included `filterchain/` package as necessary.

## Adding new python libraries

You can add new libraries via poetry:

```shell
poetry add vstools
```

## Running scripts

The most straightforward way to run scripts is via poetry:

```shell
poetry run python "example_S01E01.py"
```
