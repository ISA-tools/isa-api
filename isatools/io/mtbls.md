Intended usage of mtbls.py functionality:

```python
from isatools.io import mtbls

my_study_as_isa_json = mtbls.load('MTBLS1')
factor_names = get_factor_names(my_study_as_isa_json)
# response:
# ['gender', 'age']

if 'gender' in factor_names:
    query = { "gender": "male" }
    samples_and_files = get_samples_and_files(my_study_as_isa_json, factor_query=query)
    # response:
    #  {
    #     “sample_1": [“data_uri_1", “data_uri_2", …],
    #      “sample_2": [“data_uri_1", “data_uri_2", …]
    #  }
    
    for sample, files_in_sample in samples_and_files.items():
        for file in files_in_sample:
            # do something with the file, should be an ftp URL.
```
The slicer needs to produce:

- A reduced ISA file after the slicing.
- The list of URLs for Raw data files/study files to be downloaded by another tool.
