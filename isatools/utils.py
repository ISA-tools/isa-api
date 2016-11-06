def format_report_csv(report):
    """Format JSON validation report as CSV string

    :param report: JSON report output from validator
    :return: string representing csv formatted report
    """
    output = str()
    if report['validation_finished']:
        output = "Validation=success\n"
    for warning in report['warnings']:
        output += str("{},{},{}\n").format(warning['code'], warning['message'], warning['supplemental'])
    for error in report['errors']:
        output += str("{},{},{}\n").format(error['code'], error['message'], error['supplemental'])
    return output