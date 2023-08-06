import pytest
import argparse
import mock
from src.racing_report_package.racing_report import *


def test_read_file(tmp_path):
    test_file = tmp_path / 'test.txt'
    test_file.write_text('read file test text')

    assert read_file(test_file) == ['read file test text']


def test_parse_log_data():
    test_case = ['SVF2018-05-24_12:02:58.917',
                 'KRF2018-05-24_12:03:01.250']

    assert parse_log_data(test_case) == {'KRF': datetime.strptime('2018-05-24_12:03:01.250', '%Y-%m-%d_%H:%M:%S.%f'),
                                         'SVF': datetime.strptime('2018-05-24_12:02:58.917', '%Y-%m-%d_%H:%M:%S.%f')}


def test_parse_abbr_data():
    test_case = ['SPF_Sergio Perez_FORCE INDIA MERCEDES']

    assert parse_abbr_data(test_case) == {'SPF': {
        'abbr': 'SPF',
        'name': 'Sergio Perez',
        'team': 'FORCE INDIA MERCEDES'
    }}


def test_build_score_list(monkeypatch):
    abbr_data = ['SPF_Sergio Perez_FORCE INDIA MERCEDES']
    start_log_data = ['SPF2018-05-24_12:12:01.035']
    end_log_data = ['SPF2018-05-24_12:13:13.883']

    start_datetime = datetime.strptime(start_log_data[0][3:], '%Y-%m-%d_%H:%M:%S.%f')
    end_datetime = datetime.strptime(end_log_data[0][3:], '%Y-%m-%d_%H:%M:%S.%f')

    log_data_prepared_values = {
        start_log_data[0]: {'SPF': start_datetime},
        end_log_data[0]: {'SPF': end_datetime},
    }

    abbr_data_prepared_value = {'SPF': {'abbr': 'SPF',
                                        'name': 'Sergio Perez',
                                        'team': 'FORCE INDIA MERCEDES', }
                                }

    def mock_parse_log_data(arg):
        return log_data_prepared_values.get(arg[0])

    monkeypatch.setattr('src.racing_report_package.racing_report.parse_log_data', mock_parse_log_data)

    def mock_parse_abbr_data(arg):
        return abbr_data_prepared_value

    monkeypatch.setattr('src.racing_report_package.racing_report.parse_abbr_data', mock_parse_abbr_data)

    assert build_score_list(abbr_data, end_log_data, start_log_data) == \
           [[1, 'Sergio Perez', 'FORCE INDIA MERCEDES', '0:01:12.848']]


def test_build_score_list_driver(monkeypatch):
    abbr_data = ['SPF_Sergio Perez_FORCE INDIA MERCEDES', 'VBM_Valtteri Bottas_MERCEDES']
    start_log_data = ['SPF2018-05-24_12:12:01.035', 'VBM2018-05-24_12:00:00.000']
    end_log_data = ['SPF2018-05-24_12:13:13.883', 'VBM2018-05-24_12:01:12.434']

    log_data_prepared_values = {
        start_log_data[0]: {'SPF': datetime.strptime(start_log_data[0][3:], '%Y-%m-%d_%H:%M:%S.%f'),
                            'VBM': datetime.strptime(start_log_data[1][3:], '%Y-%m-%d_%H:%M:%S.%f')},
        end_log_data[0]: {'SPF': datetime.strptime(end_log_data[0][3:], '%Y-%m-%d_%H:%M:%S.%f'),
                          'VBM': datetime.strptime(end_log_data[1][3:], '%Y-%m-%d_%H:%M:%S.%f')},
    }

    abbr_data_prepared_value = {'SPF': {'abbr': 'SPF',
                                        'name': 'Sergio Perez',
                                        'team': 'FORCE INDIA MERCEDES', },
                                'VBM': {
                                    'abbr': 'VBM',
                                    'name': 'Valtteri Bottas',
                                    'team': 'MERCEDES'
                                }
                                }

    def mock_parse_log_data(arg):
        return log_data_prepared_values.get(arg[0])

    monkeypatch.setattr('src.racing_report_package.racing_report.parse_log_data', mock_parse_log_data)

    def mock_parse_abbr_data(arg):
        return abbr_data_prepared_value

    monkeypatch.setattr('src.racing_report_package.racing_report.parse_abbr_data', mock_parse_abbr_data)

    assert build_score_list(abbr_data, end_log_data, start_log_data, driver='Sergio Perez') == \
           [[2, 'Sergio Perez', 'FORCE INDIA MERCEDES', '0:01:12.848']]


def test_build_score_list_descending(monkeypatch):
    abbr_data = ['SPF_Sergio Perez_FORCE INDIA MERCEDES', 'VBM_Valtteri Bottas_MERCEDES']
    start_log_data = ['SPF2018-05-24_12:12:01.035', 'VBM2018-05-24_12:00:00.000']
    end_log_data = ['SPF2018-05-24_12:13:13.883', 'VBM2018-05-24_12:01:12.434']

    log_data_prepared_values = {
        start_log_data[0]: {'SPF': datetime.strptime(start_log_data[0][3:], '%Y-%m-%d_%H:%M:%S.%f'),
                            'VBM': datetime.strptime(start_log_data[1][3:], '%Y-%m-%d_%H:%M:%S.%f')},
        end_log_data[0]: {'SPF': datetime.strptime(end_log_data[0][3:], '%Y-%m-%d_%H:%M:%S.%f'),
                          'VBM': datetime.strptime(end_log_data[1][3:], '%Y-%m-%d_%H:%M:%S.%f')},
    }

    abbr_data_prepared_value = {'SPF': {'abbr': 'SPF',
                                        'name': 'Sergio Perez',
                                        'team': 'FORCE INDIA MERCEDES', },
                                'VBM': {
                                    'abbr': 'VBM',
                                    'name': 'Valtteri Bottas',
                                    'team': 'MERCEDES'
                                }
                                }

    def mock_parse_log_data(arg):
        return log_data_prepared_values.get(arg[0])

    monkeypatch.setattr('src.racing_report_package.racing_report.parse_log_data', mock_parse_log_data)

    def mock_parse_abbr_data(arg):
        return abbr_data_prepared_value

    monkeypatch.setattr('src.racing_report_package.racing_report.parse_abbr_data', mock_parse_abbr_data)

    assert build_score_list(abbr_data, end_log_data, start_log_data, order=True) == \
           [[2, 'Sergio Perez', 'FORCE INDIA MERCEDES', '0:01:12.848'],
            [1, 'Valtteri Bottas', 'MERCEDES', '0:01:12.434']]


def test_build_report(monkeypatch):
    def mock_build_score_list(*args, **kwargs):
        return [[1, 'Sergio Perez', 'FORCE INDIA MERCEDES', '0:01:12.848']]

    monkeypatch.setattr('src.racing_report_package.racing_report.read_file', lambda arg: None)
    monkeypatch.setattr('src.racing_report_package.racing_report.build_score_list', mock_build_score_list)

    assert build_report('some/path') == [[1, 'Sergio Perez', 'FORCE INDIA MERCEDES', '0:01:12.848']]


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(files='directory', driver=None, desc=None, asc=None))
def test_main(mock_args, monkeypatch):
    def mock_build_report(arg):
        return arg

    monkeypatch.setattr('src.racing_report_package.racing_report.build_report', mock_build_report)

    assert main() == 'directory'
