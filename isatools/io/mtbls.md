Intended usage of mtbls.py functionality:

```python
from isatools.io import mtbls

my_study_as_isa_json = mtbls.load('MTBLS1')
factor_names = get_factor_names(my_study_as_isa_json)

if 'gender' in factor_names:
    query = { "gender": "male" }
    samples_and_files = get_samples_and_files(my_study_as_isa_json, factor_query=query)
    
    for sample, files_in_sample in samples_and_files.items():
        for file in files_in_sample:
            # do something with the file, should be an ftp URL.
