def build_html_data_files_list(data_files_list: list) -> str:
    data_files_table = '<table>'
    data_files_table += '<tr><th>Sample Name</th><th>Data File Names</th></tr>'
    for data_file in data_files_list:
        sample_name = data_file['sample']
        data_files = ', '.join(data_file['data_files'])
        data_files_table += '<tr><td>%s</td><td>%s</td>' % (sample_name, data_files)
    data_files_table += '</table>'
    html_data_files_list = """
<html>
<head> <title>ISA-Tab Factors Summary</title> </head>
<body> %s </body>
</html>
    """ % data_files_table
    return html_data_files_list


def build_html_summary(summary: list) -> str:
    study_groups = {}
    for item in summary:
        sample_name = item['sample_name']
        study_factors = []
        for item in [x for x in item.items() if x[0] != "sample_name"]:
            study_factors.append(': '.join([item[0], item[1]]))
        study_group = ', '.join(study_factors)
        if study_group not in study_groups.keys():
            study_groups[study_group] = []
        study_groups[study_group].append(sample_name)
    summary_table = '<table>'
    summary_table += '<tr><th>Study group</th><th>Number of samples</th></tr>'
    for item in study_groups.items():
        study_group = item[0]
        num_samples = len(item[1])
        summary_table += '<tr><td>{study_group}</td><td>{num_samples}</td>' \
            .format(study_group=study_group, num_samples=num_samples)
    summary_table += '</table>'
    html_summary = """
<html>
<head>
<title>ISA-Tab Factors Summary</title>
</head>
<body>
{summary_table}
</body>
</html>
""".format(summary_table=summary_table)
    return html_summary
