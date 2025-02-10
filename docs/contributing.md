# Contriburing

Auto-Verify is an open source project that accepts contributions. You can find open issues [here](https://github.com/ADA-research/auto-verify/issues).

## Setting up the development environment

### Forking the repository

To make changes to the code, you will need to fork the [repository](https://github.com/ADA-research/auto-verify).

### Setting up the conda environment

To use set up your development environment for Auto-Verify, you will need to install [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/). Other environment managers will not work.

After installing Miniconde, you will need to create a conda environment. For example, you can use the commands below to create an environment for Auto-Verify.

```
> conda create -n auto-verify python=3.10
> conda activate auto-verify
```

### Setting up Auto-Verify for development

To install your local package of Auto-Verify, you will need to install an editable version. You can do this using the following command in your forked repository:

```
> pip install -e .
```

After doing this, you can run scripts locally and make your changes to the code.

!!! warning

    You will still need to install the different verification algorithms with the CLI tool to use them.

### Running tests with Tox

To ensure that all the original code is working and everything is neat and tidy, you should run Tox to run the tests, linter and integration tests. To do this, you will need to install pytest and tox before you can run it. You can do this with the following commands.

```
> pip install tox
> tox
```

## Submitting your code

After you have made modifications to your code, open a pull request [here](https://github.com/ADA-research/auto-verify/pulls). If a maintainer approves of the changes and the pipeline succeeds, the pull request will be merged into the main repository. If the pipeline fails, please fix them and submit a new pull request or close and reopen the issue.
