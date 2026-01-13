# Auto-Verify

[![PyPI version](https://img.shields.io/pypi/v/auto-verify.svg?color=green)](https://pypi.org/project/auto-verify/)
[![Tests](https://github.com/ada-research/auto-verify/actions/workflows/tests.yml/badge.svg)](https://github.com/ada-research/auto-verify/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-BSD%203--Clause-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-auto--verify-blue)](https://ada-research.github.io/auto-verify/)

## What is Auto-Verify? 

[Auto-Verify](https://pypi.org/project/auto-verify/) is a framework that provides an abstraction layer for a range of neural network verifiers, handling their installation, configuration, and execution. 
The package can be used together with another package by our research group, [ada-verona](https://pypi.org/project/ada-verona/), to simplify the setup of neural network verification experiments for evaluating formal verification tools. For more details, see the [How does Auto-Verify work with ada-verona?](#how-does-auto-verify-work-with-ada-verona) section in [Getting Started](#getting-started).

---

> **Update November 2025:** As of the latest Auto-Verify release v1.0.0, the package also supports **L2 Verification** via integration of the SDP-CROWN verifier.
>
> See the original [SDP-CROWN research repository](https://github.com/Hong-Ming/SDP-CROWN) and the corresponding paper:
>
> **[SDP-CROWN: Efficient Bound Propagation for Neural Network Verification with Tightness of Semidefinite Programming](https://arxiv.org/pdf/2506.06665)**  
> **ICML 2025**  
> Hong-Ming Chiu, Hao Chen, Huan Zhang, Richard Y. Zhang

---

## Installation
We recommend using [miniforge](https://github.com/conda-forge/miniforge) to set up the environment for auto-verify.

After Miniconda is installed, setup auto-verify by running the following commands:

```bash
conda create -n auto-verify python=3.10
conda activate auto-verify
pip install auto-verify  #or use uv pip if you have uv installed
```

## Getting started 
To get started, the [How-To Guides](https://ada-research.github.io/auto-verify/how-to-guides/) offer a useful starting point. 

We also recommend having a look at the [API documentation](https://ada-research.github.io/auto-verify/api/).

### How do Auto-Verify and ADA-verona relate?

- Auto-Verify wraps neural network verifiers and provides a unified interface for installing, configuring, and running them.
- **[ADA-verona](https://pypi.org/project/ada-verona/)** uses Auto-Verify to easily set up formal verification experiments through its [`AutoVerifyModule`](https://github.com/ADA-research/VERONA/blob/main/ada_verona/verification_module/auto_verify_module.py) class.

For concrete examples, refer to the examples provided in the [ada-verona tutorial](https://github.com/ADA-research/VERONA/blob/main/examples/notebooks/VERONA_tutorial_with_AutoAttack_and_AutoVerify.ipynb).

## CLI Commands

You can access the help and examples for the command-line interface by using the `--help` flag.
```bash
auto-verify --help
```
### Installing Verifiers
Currently, auto-verify supports the following verifiers:

- [nnenum](https://github.com/stanleybak/nnenum) (Stanley Bak)
- [AB-CROWN](https://github.com/Verified-Intelligence/alpha-beta-CROWN) (Zhang et al.)
- [VeriNet](https://github.com/vas-group-imperial/VeriNet) (VAS Group)
- [Oval-BaB](https://github.com/oval-group/oval-bab) (OVAL Research Group)
- [SDP-CROWN](https://github.com/Hong-Ming/SDP-CROWN) (Chiu et al. - OVAL Research Group) – efficient L2-norm robustness verification via semidefinite-program-based bound propagation.
 
These verifiers can be installed as follows:
```bash
auto-verify install nnenum
auto-verify install sdpcrown
auto-verify install abcrown
auto-verify install verinet
auto-verify install ovalbab
```

You can also install multiple verifiers in one go with the following command:

```bash
auto-verify install nnenum abcrown ovalbab verinet sdpcrown
```

#### Specifying Verifier Versions

You can specify which version of a verifier to install:

```bash
auto-verify install abcrown --verifier-version "877afa32d9d314fcb416436a616e6a5878fdab78"

auto-verify install abcrown --verifier-version most-recent
```

**Note:** If a short hash is provided and cannot be resolved, the installation will fall back to the default version for that verifier.

This allows you to:
- Use the default tested stable version
- Install a specific version by commit hash
- Install the latest version from the repository

#### Environment Selection

You can also specify which environment management strategy to use:

```bash
# Force using conda
auto-verify install nnenum --env conda

# Force using venv
auto-verify install nnenum --env venv
```

Note: We recommend to use the conda option and using [miniforge](https://github.com/conda-forge/miniforge) as the package manager.

### Listing Installed Verifiers

You can view all installed verifiers with the `list` command:

```bash
# List all installed verifiers
auto-verify list

# List only venv-based verifiers
auto-verify list --env venv

# List only conda-based verifiers
auto-verify list --env conda

# Show detailed information about installed verifiers
auto-verify list --verbose
```

The verbose mode shows additional information such as:
- Git branch and commit hash
- Path to the virtual environment
- Activation command

### Removing Verifiers

To remove installed verifiers:

```bash
# Remove a verifier (uninstall command)
auto-verify uninstall nnenum

# Remove multiple verifiers
auto-verify uninstall nnenum abcrown

# Alternative delete command (alias for uninstall)
auto-verify delete nnenum

# Remove only venv-based installations
auto-verify delete nnenum --env venv

# Remove only conda-based installations
auto-verify delete nnenum --env conda
```

## Configuration Options

Auto-verify provides several configuration options to customize its behavior. You can view your current configuration with:

```bash
auto-verify config show
```

### Environment Strategy

Controls how verification tool environments are managed:

- `conda`: Use Conda environments **(recommended)**
- `auto`: Automatically detect and use the best available option (prefers venv if uv is available)
- `venv`: Use Python virtual environments with uv **(experimental feature)**


```bash
# Set environment strategy to venv
auto-verify config set-env venv

# Set environment strategy to conda
auto-verify config set-env conda

# Set environment strategy to auto-detect
auto-verify config set-env auto
```

### Installation Path

Set a custom location for verifier installations:

```bash
# Set custom installation path
auto-verify config set-install-path /path/to/custom/location

# Reset to default path
auto-verify config set-install-path default
```

### GPU Preference

Control whether to prefer GPU-enabled installations:

```bash
# Enable GPU preference
auto-verify config set-gpu true

# Disable GPU preference
auto-verify config set-gpu false
```

### Default Timeout

Set the default verification timeout (in seconds):

```bash
# Set timeout to 300 seconds (5 minutes)
auto-verify config set-timeout 300
```

### Logging Options

Configure logging verbosity:

```bash
# Set log level
auto-verify config set-log-level INFO  # Options: DEBUG, INFO, WARNING, ERROR

# Enable verbose installation
auto-verify config set-verbose-installation true

# Disable verbose installation
auto-verify config set-verbose-installation false
```

### Advanced Options

Configure advanced behavior:

```bash
# Allow conda fallback if venv+uv is not available
auto-verify config set-conda-fallback true

# Disable conda fallback
auto-verify config set-conda-fallback false

# Require uv when using venv strategy
auto-verify config set-require-uv true

# Make uv optional
auto-verify config set-require-uv false
```

### Other Configuration Commands

```bash
# Create example configuration file
auto-verify config example

# Reset all configuration to defaults
auto-verify config reset
```

### Configuration File

You can also edit the configuration file directly:

```bash
# Create example configuration file if it doesn't exist
auto-verify config example

# Edit the configuration file with your preferred editor
nano ~/.config/autoverify/autoverify.toml
```

Available configuration options:

| Option | Description | Default | CLI Command |
|--------|-------------|---------|------------|
| `env_strategy` | Environment management strategy ("conda", "venv", or "auto") | "auto" | `set-env` |
| `custom_install_path` | Custom location for verifier installations | None (uses XDG data directories) | `set-install-path` |
| `prefer_gpu` | Whether to prefer GPU-enabled installations | true | `set-gpu` |
| `default_timeout` | Default verification timeout in seconds | 600 | `set-timeout` |
| `log_level` | Logging verbosity ("DEBUG", "INFO", "WARNING", "ERROR") | "INFO" | `set-log-level` |
| `verbose_installation` | Show detailed output during installation | false | `set-verbose-installation` |
| `allow_conda_fallback` | Allow falling back to conda if venv+uv is not available | true | `set-conda-fallback` |
| `require_uv` | Require uv to be installed when using venv strategy | false | `set-require-uv` |

Example configuration file:

```toml
# Environment management strategy: "conda", "venv", or "auto"
env_strategy = "venv"

# Custom installation path (optional)
# custom_install_path = "/path/to/custom/location"

# Runtime preferences
prefer_gpu = true
default_timeout = 600

# Logging
log_level = "INFO"
verbose_installation = false

# Advanced options
allow_conda_fallback = true
require_uv = false
```

## Installation Paths

By default, auto-verify uses the following installation paths:

### Default Installation Paths

When using the venv strategy, verifiers are installed at:
```
~/.local/share/autoverify-venv/verifiers/
```

When using the conda strategy, verifiers are installed at:
```
~/.local/share/autoverify/verifiers/
```

Each verifier is installed in its own subdirectory:

```
# For venv-based installations
~/.local/share/autoverify-venv/verifiers/
├── nnenum/
│   ├── venv/          # Python virtual environment
│   ├── tool/          # Git repository
│   └── activate.sh    # Activation script
├── abcrown/
└── verinet/

# For conda-based installations
~/.local/share/autoverify/verifiers/
├── nnenum/
│   └── tool/          # Git repository
├── abcrown/
└── verinet/
```

### Custom Installation Path

You can set a custom installation path using the CLI or by editing the configuration file:

```bash
# Set custom path via CLI
auto-verify config set-install-path /path/to/custom/location
```

```toml
# Set custom path in config file
custom_install_path = "/path/to/custom/location"
```

When a custom path is set, both venv and conda verifiers will be installed under this directory, maintaining the same structure:

```
/path/to/custom/location/
├── verifiers/
│   ├── nnenum/
│   ├── abcrown/
│   └── verinet/
```

## Using with ada-verona

Auto-verify can be used as a plugin for the robustness experiment setup package [ada-verona](https://github.com/ADA-research/VERONA), providing formal verification capabilities.

