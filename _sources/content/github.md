# Downloading files stored in Github
==================================

## The ISA GitHub Adapter class


The GitHub API wrapper/adapter may be useful to retrieve ISA datasets
(as JSON or Tabs) or configuration files in XML format. The core class,
`IsaGitHubStorageAdapter` can be instantiated with or without
authorisation.

***

## Usage without authentication

If authentication is not required to access the required resource, you
can directly instantiate an adapter object and use it.

```python
from isatools.net.storage_adapter import IsaGitHubStorageAdapter
from zipfile import ZipFile
adapter = IsaGitHubStorageAdapter()
adapter.retrieve('tests/data/BII-I-1', 'test_out_dir', owner='ISA-tools', repository='isa-api')
# retrieving a directory (containg either an ISA-tab dataset or a set of configuration files,
# will return a file-like object containg the zipped content of the directory.
buf = adapter.retrieve('tests/data/BII-I-1', destination='test_out_dir', owner='ISA-tools',
                       repository='isa-api')
# Default owner is "ISA-tools' and default repo is 'isa-api' so they can actually be omitted.
# Default destination directory is 'isa-target'
zip_file = ZipFile(buf)
# get the list of the files retrieved from the directory
zip_file.namelist()
# an ISA JSON dataset is returned as a stardard JSON object
json_obj = adapter.retrieve('isatools/sampledata/BII-I-1.json', destination='test_out_dir',
                            owner='ISA-tools', repository='isa-api', validate_json=True)
# set write_to_file to False to avoid saving the resource to disk
json_obj = adapter.retrieve('isatools/sampledata/BII-I-1.json', write_to_file=False,
                            owner='ISA-tools', repository='isa-api', validate_json=True)
# retrieving a single configuration file returns an lxml ElementTree object:
xml_obj = adapter.retrieve('isaconfig-2013222/protein_expression_ge.xml',
                           repository='Configuration-Files')
# get root element for the configuration file
xml_obj.getroot()
```

***

## Usage with authentication

To access as authenticated user, the recommended way is to instantiate
the storage adapter in a with statement.

```python
with IsaGitHubStorageAdapter(username='yourusername', password='yourpw',
                             note='test_api') as adapter:
    adapter.is_authenticated # true
    # do stuff...
```

Otherwise you must explicitly call the `close()` method to delete the
current authorisation from the GitHub server

```python
adapter = IsaGitHubStorageAdapter(username='yourusername', password='youpw', note='test_api')
adapter.is_authenticated # True
# do stuff...
adapter.close()
```
