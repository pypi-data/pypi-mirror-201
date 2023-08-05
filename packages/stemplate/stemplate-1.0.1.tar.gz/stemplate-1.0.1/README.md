# PyPack

> What does it mean?

The name "PyPack" comes from the contraction of "Python" and "Package".

> What is it for?

PyPack is a template for Python package repositories on GitLab.

> Is it hard to use?

You need to be a bit familiar with python project packaging.

## Background

Creating a [package distribution](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools) for a Python project is a process that can already take some time.
Putting it all together in a repository that allows full use of [GitLab's CI/CD](https://docs.gitlab.com/ee/ci) features can seem like a daunting extra step.
The goal here is to simplify these processes by presenting a working example of a package distribution repository that uses CI/CD features.

Here are some references and recommended readings about the creation of Python package distributions and the use of CI/CD features:

* [Tool recommendations](https://packaging.python.org/en/latest/guides/tool-recommendations)
* [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects)
* [PyPi classifiers](https://pypi.org/classifiers)
* [Git Basics - Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
* [`.gitlab-ci.yml` keyword reference](https://docs.gitlab.com/ee/ci/yaml)

## Usage

The Python package used as an example here is called "Stemplate".
The following explains how this package is automatically tested and deployed on [PyPi](https://pypi.org/project/stemplate) thanks to the CI/CD features.

### Deployment

To use this template follow these steps:

* Download or clone the PyPack project from its [GitLab repository](https://gitlab.com/stemplate/pypack).

```bash
git clone git@gitlab.com:stemplate/pypack.git
```

* Replace all occurrences of "stemplate" with the name of your Python package. (Use your editor's search tool.)
* Adapt the [`pyproject.toml`](/pyproject.toml) file, and add your potential dependencies. (Here NumPy is an example of dependency.)
* Use [`template.md`](/template.md) as a template for the new `README.md`.
* Install the Python virtual environment with the command `. setup.sh` or `source setup.sh`. (See the [`setup.sh`](/setup.sh) script for more information.)
* Incorporate/adapt your package source files in the [`src/`](/src) directory.
* Add the test functions for your package in the [`tests/run.py`](/tests/run.py) script.
* Remove the `.git` directory and initialize a new one:

```bash
git init --initial-branch=main
git add <your-files>
git commit -m "initial commit"
git tag -a v1.0.0rc1 -m "version 1.0.0rc1"
```

* Build and upload the package to [Pypi](https://pypi.org) with the command `upload` (accessible after sourcing `setup.sh`).
* Create an empty repository on [GitLab](https://gitlab.com) for your package distribution.
* Create an API token for the project on PyPi. (Use the url address of your GitLab repository to name the token in PyPi.)
* Add the PyPi Token variables on GitLab (Project > Settings > CI/CD > Variables):
    1. `TWINE_USERNAME`: `__token__` (Add "Protect", "Mask", and "Expand" options)
    2. `TWINE_PASSWORD`: *token value* (Add "Protect", "Mask", and "Expand" options)
* Protect the `v*` wildcard tag (Project > Settings > Repository > Protected tags).
* Make sure that the `main` branch is protected and set "Allowed to push and merge" to "No one" (Project > Settings > Repository > Protected branch).
* Push:

```bash
git remote add origin git@gitlab.com:<user/project>.git
git push origin main --tags
git branch --set-upstream-to=origin/main main
```

### Development

At this stage your project is deployed on both GitLab and PyPi, and the pipeline should have been launched on GitLab.
The latter is configured in the [`.gitlab-ci.yml`](/.gitlab-ci.yml) YAML file.
The configuration proposed in this file allows to run the tests each time GitLab receives a push.

* Do not work on the main branch, create another one (like `dev`).
* Use `run`, `lint` and `makedocs` commands to test, lint and document your package. (See the [`setup.sh`](/setup.sh) script for more information.)
* Make some potential modifications so that the pipeline runs without errors.
* After merging your working branch into the `main` branch, if the pipeline passed, add a tag `v1.0.0` "version 1.0.0" directly on GitLab.
This will automatically deploy the new release on PyPi and build the documentation.
* Delete the working branch.

Repeat these steps (from creating a new branch) for each modification made to the project (without forgetting to adapt the version in the tag name).

## Credits

* Dunstan Becht

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
