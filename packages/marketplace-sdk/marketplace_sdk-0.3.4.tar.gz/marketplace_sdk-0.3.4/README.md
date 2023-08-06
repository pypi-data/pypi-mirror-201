# MarketPlace SDK

Python Software Development Toolkit (SDK) to communicate with the Materials MarketPlace platform.

## Installation

To install the package, execute:

```console
pip install marketplace-sdk
```

## Usage
The [MarketPlace documentation](https://materials-marketplace.readthedocs.io/en/latest/) contains [a tutorial](https://materials-marketplace.readthedocs.io/en/latest/jupyter/sdk.html) on how to configure and use this package.

## Authors

* **Carl Simon Adorf (EPFL)** - [@csadorf](https://github.com/csadorf)
* **Pablo de Andres (Fraunhofer IWM)** - [@pablo-de-andres](https://github.com/pablo-de-andres)
* **Pranjali Singh (Fraunhofer IWM)** - [@singhpranjali](https://github.com/singhpranjali)

See also the list of [contributors](https://github.com/materials-marketplace/python-sdk/contributors).

## Contact
- simon.adorf@epfl.ch
- pablo.de.andres@iwm.fraunhofer.de
- pranjali.singh@iwm.fraunhofer.de

## For maintainers

To create a new release, clone the repository, install development dependencies with `pip install -e '.[dev]'`, and then execute `bumpver update --[major|minor|patch]`.
This will:

  1. Create a tagged release with bumped version and push it to the repository.
  2. Trigger a GitHub actions workflow that creates a GitHub release and publishes it on PyPI.

Additional notes:

  - The project follows semantic versioning.
  - Use the `--dry` option to preview the release change.
  - The release tag (e.g. a/b/rc) is determined from the last release.
    Use the `--tag` option to switch the release tag.

## MIT License

Copyright (c) 2021 Carl Simon Adorf (EPFL)

All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgements

This work is supported by the
[MARVEL National Centre for Competency in Research](<http://nccr-marvel.ch>) funded by the [Swiss National Science Foundation](<http://www.snf.ch/en>),
and the MarketPlace project funded by [Horizon 2020](https://ec.europa.eu/programmes/horizon2020/) under the H2020-NMBP-25-2017 call (Grant No. 760173).

<div style="text-align:center">
 <img src="logos/MARVEL.png" alt="MARVEL" height="75px">
 <img src="logos/MarketPlace.png" alt="MarketPlace" height="75px">
</div>
