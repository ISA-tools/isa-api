# -*- coding: utf-8 -*-
"""isatools meta-module for importing various submodules.

This module allows users to import submodules without having to use fully
qualified import indices by exposing all submodules on the same level
entry point.

Example:

    Instead of importing the isatab2json converter directly::

        $ from isatools.convert import isatab2json

    We can import the same module without specifying the .convert package::

        $ from isatools import isatab2json
"""
from __future__ import absolute_import

from isatools.convert import (
    isatab2cedar as isatab2cedar_module,
    isatab2json as isatab2json_module,
    isatab2sampletab as isatab2sampletab_module,
    isatab2sra as isatab2sra_module,
    isatab2w4m as isatab2w4m_module,
    json2isatab as json2isatab_module,
    json2magetab as json2magetab_module,
    json2sampletab as json2sampletab_module,
    json2sra as json2sra_module,
    magetab2isatab as magetab2isatab_module,
    magetab2json as magetab2json_module,
    mzml2isa as mzml2isa_module,
    sampletab2isatab as sampletab2isatab_module,
    sampletab2json as sampletab2json_module,
)
from isatools.net import (
    biocrates2isatab as biocrates2isatab_module,
    mtbls as mtbls_module,
    mw2isa as mw2isa_module,
    ols as ols_module,
    pubmed as pubmed_module,
    sra2isatab as sra2isatab_module,
)


# isatools.convert packages
isatab2cedar = isatab2cedar_module
isatab2json = isatab2json_module
isatab2sampletab = isatab2sampletab_module
isatab2sra = isatab2sra_module
isatab2w4m = isatab2w4m_module
json2isatab = json2isatab_module
json2magetab = json2magetab_module
json2sampletab = json2sampletab_module
json2sra = json2sra_module
magetab2isatab = magetab2isatab_module
magetab2json = magetab2json_module
mzml2isa = mzml2isa_module
sampletab2isatab = sampletab2isatab_module
sampletab2json = sampletab2json_module

# isatools.net packages
biocrates2isatab = biocrates2isatab_module
mtbls = mtbls_module
mw2isa = mw2isa_module
ols = ols_module
pubmed = pubmed_module
sra2isatab = sra2isatab_module
