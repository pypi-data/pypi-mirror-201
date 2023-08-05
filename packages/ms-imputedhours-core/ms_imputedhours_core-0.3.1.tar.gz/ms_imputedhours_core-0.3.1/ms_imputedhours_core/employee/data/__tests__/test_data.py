import unittest
from unittest.mock import Mock, patch
from datetime import datetime, date
from freezegun import freeze_time

from ms_imputedhours_core.employee.data import get_all_employee_data_by_range


DEFAULT_AGREEMENT_HOURS = {
    'totalHours': 142.0,
    'days': {
        '1-4': '0',
        '2-4': '0',
        '3-4': '8',
        '4-4': '5.5',
        '5-4': '0',
        '6-4': '0',
        '7-4': '8',
        '8-4': '8',
        '9-4': '0',
        '10-4': '8',
        '11-4': '5.5',
        '12-4': '0',
        '13-4': '0',
        '14-4': '8',
        '15-4': '8',
        '16-4': '8',
        '17-4': '8',
        '18-4': '5.5',
        '19-4': '0',
        '20-4': '0',
        '21-4': '8',
        '22-4': '8',
        '23-4': '8',
        '24-4': '8',
        '25-4': '5.5',
        '26-4': '0',
        '27-4': '0',
        '28-4': '8',
        '29-4': '8',
        '30-4': '8'
    }
}


class TestSuite(unittest.TestCase):
    def _create_Agreements_mock(self, Agreements):
        get_hours_by_range_mock = Mock()
        get_hours_by_range_mock.get_hours_by_range.return_value = DEFAULT_AGREEMENT_HOURS  # noqa: E501

        Agreements.return_value = get_hours_by_range_mock
        return Agreements

    def _create_successfactor_all_data_mock(self, get_successfactor_all_data):
        get_successfactor_all_data.return_value = [
            {
                'email': 'employee1@makingscience.com',
                'hiringdate': date(2021, 4, 1),
                'internshipdate': None,
                'fte': '100',
                'supervisor': 'employee2@makingscience.com',
                'office': 'Madrid - Ing',
                'name': 'Employee1',
                'lastname': 'Doe',
            },
            {
                'email': 'employee2@makingscience.com',
                'hiringdate': date(2021, 4, 1),
                'internshipdate': None,
                'fte': '50',
                'supervisor': 'employee20@makingscience.com',
                'office': 'Madrid - Ing',
                'name': 'Employee2',
                'lastname': 'Doe',
            },
            {
                'email': 'employee3@makingscience.com',
                'hiringdate': date(2021, 4, 1),
                'internshipdate': date(2021, 12, 27),
                'fte': '100',
                'supervisor': 'employee2@makingscience.com',
                'office': 'Madrid - Ing',
                'name': 'Employee1',
                'lastname': 'Doe',
            },
            {
                'email': 'employee4@makingscience.com',
                'hiringdate': date(2022, 4, 1),
                'internshipdate': None,
                'fte': '50',
                'supervisor': 'employee2@makingscience.com',
                'office': 'Madrid - Ing',
                'name': 'Employee4',
                'lastname': 'Doe',
            }
        ]
        return get_successfactor_all_data

    def _create_get_all_data_by_dates_mock(self, get_all_data_by_dates):
        get_all_data_by_dates.return_value = [
            {
                'timeSpent': 28800,
                'authorEmail': 'employee1@makingscience.com',
                'started': date(2022, 4, 15),
            },
            {
                'timeSpent': 28800,
                'authorEmail': 'employee1@makingscience.com',
                'started': date(2022, 4, 16),
            },
            {
                'timeSpent': 28800,
                'authorEmail': 'employee4@makingscience.com',
                'started': date(2022, 4, 15),
            },
            {
                'timeSpent': 28800,
                'authorEmail': 'employee4@makingscience.com',
                'started': date(2022, 4, 16),
            },
        ]

        return get_all_data_by_dates

    def _create_get_all_employee_capacity_mock(self, get_all_employee_capacity):  # noqa: E501
        get_all_employee_capacity.return_value = [
            {
                'email': 'employee1@makingscience.com',
                'fte': 1.0,
            },
            {
                'email': 'employee2@makingscience.com',
                'fte': 1.0,
            },
            {
                'email': 'employee4@makingscience.com',
                'fte': 0.5,
            },
        ]
        return get_all_employee_capacity

    @freeze_time("2022-4-11")
    @patch('ms_imputedhours_core.employee.data.get_all_employee_capacity')
    @patch('ms_imputedhours_core.employee.data.get_all_data_by_dates')
    @patch('ms_imputedhours_core.employee.data.get_successfactor_all_data')
    @patch('ms_imputedhours_core.employee.data.Agreements')
    def test_get_all_employee_data_by_range_return_employee_full_capacity(
        self,
        Agreements,
        get_successfactor_all_data,
        get_all_data_by_dates,
        get_all_employee_capacity,
    ):
        Agreements = self._create_Agreements_mock(Agreements)
        get_successfactor_all_data = self._create_successfactor_all_data_mock(
            get_successfactor_all_data)
        get_all_data_by_dates = self._create_get_all_data_by_dates_mock(
            get_all_data_by_dates)
        get_all_employee_capacity = self._create_get_all_employee_capacity_mock(  # noqa: E501
            get_all_employee_capacity)

        from_date = datetime.strptime('2022-04-1', '%Y-%m-%d').date()
        to_date = datetime.strptime('2022-04-2', '%Y-%m-%d').date()
        office_name = 'Madrid - ing'
        expected_result = {
            'employee1@makingscience.com': {
                'real_capacity': 0.0,
                'current_capacity': 16.0,
                'current_percentage_hours_imputed': 100,
                'supervisor': 'employee2@makingscience.com',
                'name': 'Employee1 Doe'
            },
            'employee2@makingscience.com': {
                'real_capacity': 0.0,
                'current_capacity': 0.0,
                'current_percentage_hours_imputed': 100,
                'supervisor': 'employee20@makingscience.com',
                'name': 'Employee2 Doe'
            },
            'employee4@makingscience.com': {
                'real_capacity': 0.0,
                'current_capacity': 16.0,
                'current_percentage_hours_imputed': 100,
                'supervisor': 'employee2@makingscience.com',
                'name': 'Employee4 Doe'
            }
        }
        result = get_all_employee_data_by_range(
            from_date,
            to_date,
            office_name,
        )

        self.assertDictEqual(result, expected_result)

    @freeze_time("2022-4-15")
    @patch('ms_imputedhours_core.employee.data.get_all_employee_capacity')
    @patch('ms_imputedhours_core.employee.data.get_all_data_by_dates')
    @patch('ms_imputedhours_core.employee.data.get_successfactor_all_data')
    @patch('ms_imputedhours_core.employee.data.Agreements')
    def test_get_all_employee_data_by_range_return_employee_correct_data_for_day_15(  # noqa: E501
        self,
        Agreements,
        get_successfactor_all_data,
        get_all_data_by_dates,
        get_all_employee_capacity,
    ):
        Agreements = self._create_Agreements_mock(Agreements)
        get_successfactor_all_data = self._create_successfactor_all_data_mock(
            get_successfactor_all_data)
        get_all_data_by_dates = self._create_get_all_data_by_dates_mock(
            get_all_data_by_dates)
        get_all_employee_capacity = self._create_get_all_employee_capacity_mock(  # noqa: E501
            get_all_employee_capacity)
        from_date = datetime.strptime('2022-04-1', '%Y-%m-%d').date()
        to_date = datetime.strptime('2022-04-15', '%Y-%m-%d').date()
        office_name = 'Madrid - ing'
        expected_result = {
            'employee1@makingscience.com': {
                'real_capacity': 59.0,
                'current_capacity': 16.0,
                'current_percentage_hours_imputed': 27.12,
                'supervisor': 'employee2@makingscience.com',
                'name': 'Employee1 Doe'
            },
            'employee2@makingscience.com': {
                'real_capacity': 59.0,
                'current_capacity': 0.0,
                'current_percentage_hours_imputed': 0.0,
                'supervisor': 'employee20@makingscience.com',
                'name': 'Employee2 Doe'
            },
            'employee4@makingscience.com': {
                'real_capacity': 29.5,
                'current_capacity': 16.0,
                'current_percentage_hours_imputed': 54.24,
                'supervisor': 'employee2@makingscience.com',
                'name': 'Employee4 Doe'
            }
        }
        result = get_all_employee_data_by_range(
            from_date,
            to_date,
            office_name,
        )

        self.assertDictEqual(result, expected_result)
