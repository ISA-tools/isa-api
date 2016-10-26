Intended usage of mtbls.py functionality:

```python
from isatools.io import mtbls

study_id = 'MTBLS1'

factor_names = mtbls.get_factor_names(study_id)
# response:
# {'Gender', 'Age'}

if 'Gender' in factor_names:
    factor_values = mtbls.get_factor_values(study_id, 'Gender')
    # response:
    # {'Male', 'Female'}

    query = { "Gender": "Male" }
    samples_and_files = mtbls.get_data_files(study_id, factor_query=query)
    # response:
    #  [
    #     {
    #        'sample': 'ADG10003u_007'},
    #        'data_files': ['ADG10003u_007.zip'],
    #        'query_used': {'Gender': 'Male'}
    #     }, ...
    #  ]
    
    for sample_and_files in samples_and_files:
        sample_name = sample_and_files['sample']
        data_files = sample_and_files['data_files']
        for data_file in data_files:
            # do something with the file name, e.g. make it an ftp URL.
```
The slicer produces:
- The list of URLs for Raw data files/study files to be downloaded by another tool.

The slicer needs to produce:
- A reduced ISA file after the slicing.