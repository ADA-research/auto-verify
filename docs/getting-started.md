### System requirements

Auto-Verify has only been tested for Linux and will not work on MacOS and Windows. Alternatively, using [Windows Subsystem for Linux](https://learn.microsoft.com/nl-nl/windows/wsl/about) is also an option.

Additionally, if you want to make use of the GPU based verification algorithms, you will need a CUDA-enabled GPU.

### Installing Auto-Verify

First, install [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/). Miniconda is used to manage the environments of different verification tools, other environment managers will _not_ work.
!!! warning

    Anaconda can fail trying to install environments in some cases where Miniconda does not.

After Miniconda is installed, setup Auto-Verify by running the following commands:

```
> conda create -n auto-verify python=3.10
> conda activate auto-verify
> pip install auto-verify
```

To check if the installation was succesful, run:

```bash
> auto-verify --version
```

### Installing Verification Tools

Currently, Auto-Verify supports the following verifiers:

- [nnenum](https://github.com/stanleybak/nnenum) (_Stanley Bak_)
- [AB-Crown](https://github.com/Verified-Intelligence/alpha-beta-CROWN) (_Zhang et al_)
- [VeriNet](https://github.com/vas-group-imperial/VeriNet) (_VAS Group_)
- [Oval-BaB](https://github.com/oval-group/oval-bab) (_OVAL Research Group_)

These verifiers can be installed as follows:

```
> auto-verify install nnenum
> auto-verify install abcrown
> auto-verify install verinet
> auto-verify install ovalbab
```

To uninstall a verifier, run:

```
> auto-verify uninstall [verifier]
```

### Downloading Datasets

If you have your own models to use with Auto-Verify, you can use those. However, if you just want to try it out, we recommend using the datasets that are provided for the VNNCOMP competition. These datasets are already made compatible with Auto-Verify and APIs are available to directly work with them. You can find the datasets from the previous years over here:

- [VNNCOMP 2023](https://github.com/stanleybak/vnncomp2023)
- [VNNCOMP 2022](https://github.com/stanleybak/vnncomp2022)
- [VNNCOMP 2021](https://github.com/stanleybak/vnncomp2021)
- [VNNCOMP 2020](https://github.com/verivital/vnn-comp)

### Usage
If you want to get started with Auto-verify quickly, you can go to the [examples](examples.md).
To inspect the available functionalities of the package, please refer to the [API documentation](api.md). 