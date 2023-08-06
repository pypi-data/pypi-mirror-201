## Getting started
This is a Python package that provides a client class, RnaGet, to access RNAget data. RNAget is an API standard implemented by the GA4GH that provides uniform access to large-scale RNAseq expression data across different studies and sources.

## Usage

To use this package, you need to import the RnaGet class:

```py
from rnaget_client import RnaGet

gtex = RnaGet(host='gtex') # gtex instance
encode = RnaGet(host='encode') # encode instance
another_host = RnaGet(host='ANOTHER_URL', token='ACCESS_TOKEN')

```

The host parameter should be set to the URL of the RNAget server that you want to access. You can also pass an optional token parameter to set an access token to access protected data.

## Available Methods:

The RnaGet class provides the following methods to retrieve data from the RNAget server:

    get_filters(type, params=None): Get model filters, accepted values are: projects, studies, expressions, or continuous.

    get_projects(version=None): Get the project list.

    get_project(id): Get project by ID.

    get_studies(version=None): Get the study list.

    get_study(id): Get study by ID.

    get_expression_list(format, download=False, **kwargs): Get the expression list.

    get_expression(id, download=False, **kwargs): Get the expression object.

    get_expression_formats(): Get data formats.

    get_expression_units(): Get units.

    get_continuous_list(format, download=False, **kwargs): Get the continuous list.


For more information about the usage and parameters of these methods, please refer to the [RNAget specs](https://ga4gh-rnaseq.github.io/schema/docs/index.html).

You can [get `rnaget-client` from PyPI](https://pypi.org/project/rnaget-client),

```bash
python -m pip install rnaget-client
```
