EMPTY_FTE = '0'


def transform_successfactor_data(bigquery_successfactor):
    data_json = {
        'office_name': 'Madrid - Ing',
        'FTE': 1,
    }

    for data in bigquery_successfactor:
        data_json['office_name'] = data.get('office', '')
        data_json['FTE'] = data.get('fte', 0)

    return data_json


def transform_successfactor_all_data(bigquery_successfactor):
    data_json = {}

    for data in bigquery_successfactor:
        email = data.get('email', '')
        hiringdate = data.get('hiringdate', '')
        enddate = data.get('internshipdate', '')

        if email not in data_json.keys():
            data_json[email] = {}

        fte = data.get('fte', EMPTY_FTE) or EMPTY_FTE  # For null values
        data_json[email]['supervisor'] = data.get('supervisor', '')
        data_json[email]['office_name'] = data.get('office', '')
        data_json[email]['FTE'] = float(fte.replace(',', '.'))
        data_json[email]['hiring_date'] = hiringdate
        data_json[email]['enddate'] = enddate
        data_json[email]['name'] = "{} {}".format(
            data.get('name', ''), data.get('lastname', ''))

    return data_json


def transform_all_capacities(capacities):
    data_json = {}

    for data in capacities:
        email = data.get('email')
        if email not in data_json:
            data_json[email] = {
                'fte': data.get('fte')
            }

    return data_json


def group_task_by_email(month_data, group_by_full_date=False):
    data_by_email = {}
    for task in month_data:
        taskTimeSpent = task.get('timeSpent', 0)
        taskEmail = task.get('authorEmail')
        taskStarted = task.get('started')
        grouped_date = taskStarted.strftime(
            '%Y-%m-%d') if group_by_full_date else taskStarted.day
        if taskEmail not in data_by_email.keys():
            data_by_email[taskEmail] = {'totalHours': 0, 'days': {}}

        if grouped_date not in data_by_email[taskEmail]['days']:
            data_by_email[taskEmail]['days'][grouped_date] = 0

        data_by_email[taskEmail]['totalHours'] += taskTimeSpent
        data_by_email[taskEmail]['days'][grouped_date] += taskTimeSpent

    return data_by_email


def group_task_by_outdated(month_data):
    data_by_email = {}
    for task in month_data:
        taskTimeSpent = task.get('timeSpent', 0)
        taskEmail = task.get('authorEmail')
        taskStarted = task.get('started').strftime('%Y-%m-%d')
        taskCreated = task.get('created').strftime('%Y-%m-%d')
        taskIssueKey = task.get('issueKey')

        if taskEmail not in data_by_email.keys():
            data_by_email[taskEmail] = {'totalHours': 0, 'days': {}}

        if taskCreated not in data_by_email[taskEmail]['days']:
            data_by_email[taskEmail]['days'][taskCreated] = {
                'total': 0,
                'tasks': {}}

        if taskIssueKey not in data_by_email[taskEmail]['days'][taskCreated]['tasks']:  # noqa: E501
            data_by_email[taskEmail]['days'][taskCreated]['tasks'][taskIssueKey] = {}  # noqa: E501

        if taskStarted not in data_by_email[taskEmail]['days'][taskCreated]['tasks'][taskIssueKey]:  # noqa: E501
            data_by_email[taskEmail]['days'][taskCreated]['tasks'][taskIssueKey][taskStarted] = 0  # noqa: E501

        data_by_email[taskEmail]['totalHours'] += taskTimeSpent
        data_by_email[taskEmail]['days'][taskCreated]['total'] += taskTimeSpent
        data_by_email[taskEmail]['days'][taskCreated]['tasks'][taskIssueKey][taskStarted] += taskTimeSpent  # noqa: E501

    return data_by_email
