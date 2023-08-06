<!-- vale Microsoft.Headings = NO -->
# Contributing Guideline
<!-- vale Microsoft.Headings = YES -->

## Requirements

| Tool                                                        | Version                                                                                     |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Node.js and npm                                             | `engines` values in [package.json](package.json)                                            |
| [gibo](https://github.com/simonwhitaker/gibo#readme)        | ^2.2.8                                                                                      |
| [Vale CLI](https://vale.sh/)                                | ^2.21.3                                                                                     |
| [yamllint](https://yamllint.readthedocs.io/)                | ^1.28.0                                                                                     |
| [ShellCheck](https://github.com/koalaman/shellcheck#readme) | >=0.9.0, <1.0.0                                                                             |
| [actionlint](https://github.com/rhysd/actionlint#readme)    | [.tool-versions](https://github.com/haru52/base_template_cli/blob/main/.tool-versions)      |
| Python                                                      | [.python-version](https://github.com/haru52/base_template_cli/blob/main/.python-version#L1) |
| Pipenv                                                      | >=2023.3.20                                                                                 |

## Rules

| Category               | Rule                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Git commit             | [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)                                                              |
|                        | [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/@commitlint/config-conventional#readme) |
| Git branching strategy | [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow)                                                               |
| Versioning             | [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)                                                                           |
| GitHub PR title        | Same as the commit message rule                                                                                                            |

## Development flow

1. Fork this repository
2. Develop and create a Pull Request (PR) according to [the preceding rules](#rules)
3. This repo maintainers will review the PR
4. The maintainers will merge the PR branch if they approved it, otherwise they will close it without merging

## Installation

```sh
git clone git@github.com:<your org>/base_template_cli.git
cd base_template_cli
make dev-install
```

## Run the script

```sh
cd path/to/base_template_cli
pipenv shell
```

```sh
cd src
python -m base_template_cli.main
```

## Lint

```sh
make lint
```

## Git commit

```sh
npm run commit # Commitizen with commitlint adapter
# or
npm run cm     # Alias for `npm run commit`
# or
git commit     # Standard Git commit
```
