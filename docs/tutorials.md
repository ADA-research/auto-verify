# Tutorial

!!! UNDER CONSTRUCTION !!!

!!! UNDER CONSTRUCTION !!!

!!! UNDER CONSTRUCTION !!!

!!! UNDER CONSTRUCTION !!!

!!! UNDER CONSTRUCTION !!!

!!! warning

    Auto-Verify has only been tested for Linux and will not work on MacOS and Windows.

## Getting Started

### Installing Auto-Verify

First of all, make install [Miniconda](TODO LINK). Miniconda is used to manage the environments of different verification tools, other environment managers will _not_ work.

!!! warning

    Anaconda can fail trying to install environments in some cases where Miniconda does not.

After Miniconda is installed, setup Auto-Verify by running the following commands:

```
> conda create -n python=3.10 auto-verify
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
