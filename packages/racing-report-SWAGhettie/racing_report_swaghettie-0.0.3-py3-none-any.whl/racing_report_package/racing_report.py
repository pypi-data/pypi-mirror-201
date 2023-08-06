from datetime import datetime, timedelta
from argparse import ArgumentParser, Namespace
from pathlib import Path
from operator import itemgetter

ABBR_FILE = 'abbreviations.txt'
START_LOG_FILE = 'start.log'
END_LOG_FILE = 'end.log'
PRINT_REPORT_DELIM = 15


def read_file(filepath: Path) -> list:
    """
    Reads the contents of the file at the given path and returns a list of strings.

    :param filepath: A path to the file to be read.
    :type filepath: Path
    :return: A list of strings representing the lines of the file.
    :rtype: list
    """
    with open(filepath) as raw_data:
        raw_data = raw_data.read().splitlines()
    return raw_data


def parse_log_data(raw_data: list) -> dict:
    """
    Parses a list of log data strings and returns a dict containing abbreviated names and times.

    :param raw_data: A list of strings representing log data.
    :type raw_data: list
    :return: A dict containing abbreviated names and times.
    :rtype: dict
    """
    parsed_data: dict = {}
    for row in raw_data:
        time_datetime = datetime.strptime(row[3:], '%Y-%m-%d_%H:%M:%S.%f')
        parsed_data[row[0:3]] = time_datetime

    return parsed_data


def parse_abbr_data(raw_data: list) -> dict:
    """
    Parses a list of abbreviated name data strings and returns a
    dictionary containing driver information.

    :param raw_data: A list of strings representing abbreviated name data.
    :type raw_data: list
    :return: A dictionary containing driver information.
    :rtype: dict
    """
    driver_info: dict = {}
    for row in raw_data:
        if '_' not in row:
            raise ValueError('Data row must be separated by "_".')
        keys = ('abbr', 'name', 'team')
        values = row.split('_')
        driver_info[values[0]] = dict(zip(keys, values))

    return driver_info


def build_score_list(abbr_data: list, end_log_data: list, start_log_data: list, driver: str = None,
                     order=False) -> list:
    """
    Returns a sorted list of lap times and driver information for all drivers.

    :param abbr_data: A list of strings representing abbreviated name data.
    :type abbr_data: list
    :param end_log_data: A list of strings representing end log data.
    :type end_log_data: list
    :param start_log_data: A list of strings representing start log data.
    :type start_log_data: list
    :param driver: A string representing the name of a specific driver to filter results.
    :type driver: str
    :param order: A boolean indicating if the list should be sorted in descending order.
    :type order: bool
    :return: A list of lists containing driver information and lap time in ascending order.
    :rtype: list
    """
    abbr_data_dict: dict = parse_abbr_data(abbr_data)
    end_data_dict: dict = parse_log_data(end_log_data)
    start_data_dict: dict = parse_log_data(start_log_data)

    score_list = []

    for abbr_key, abbr_info in abbr_data_dict.items():
        abbr, name, team = abbr_info.values()
        end_driver_time = end_data_dict.get(abbr_key)
        start_driver_time = start_data_dict.get(abbr_key)
        if start_driver_time > end_driver_time:
            continue
        lap_time = end_driver_time - start_driver_time
        if lap_time > timedelta(hours=0, minutes=0, seconds=0, milliseconds=0):  # append with list(not tuple),
            score_list.append([name, team, ''.join(list(str(lap_time)))[:-3]])  # to insert driver pos later

    score_list.sort(key=itemgetter(2))  # ascending sort scoreboard by lap time

    for index, item in enumerate(score_list):  # defining driver position
        item.insert(0, index + 1)

    if order:
        score_list.reverse()

    if driver:
        for driver_info in score_list:
            if driver in driver_info:
                return [driver_info]

    return score_list


def build_report(directory, driver=None, order=False) -> list:
    """
    Generates the scoreboard report based on the input directory path, driver name, and order.

    :param directory: A string representing the directory path of the folder containing the data files.
    :type directory: str
    :param driver: A string representing the driver's name whose information is to be displayed.
    :type driver: str
    :param order: A boolean representing the order of the scoreboard report. Set to True
    to sort the scores in descending order, otherwise, False to sort in ascending order.
    :type order: bool
    :return: A list of lists containing the scoreboard report.
    :rtype: list
    """
    root = Path(directory).resolve()

    abbr_filepath = root / ABBR_FILE
    start_log_filepath = root / START_LOG_FILE
    end_log_filepath = root / END_LOG_FILE

    abbr_data: list = read_file(abbr_filepath)
    start_log_data: list = read_file(start_log_filepath)
    end_log_data: list = read_file(end_log_filepath)

    order_arg = order
    driver_arg = driver

    score_list = build_score_list(abbr_data, end_log_data, start_log_data, driver=driver_arg, order=order_arg)

    return score_list


def print_report(data: list) -> None:
    """
    Prints the given list of strings representing the scoreboard report.

    :param data: A list of strings representing the scoreboard report.
    :type data: list
    :return: None
    """
    for index, item in enumerate(data):
        if index == PRINT_REPORT_DELIM:
            print('-' * 72)
            continue
        print(f"{item[0]}. {item[1]} | {item[2]} | {item[3]}")


def main():
    parser = ArgumentParser()
    parser.add_argument('--asc', action='store_true', help="Show first 15 results of scoreboard.")
    parser.add_argument('--desc', action='store_true', help="Set on <True> to reverse leaderboard.")
    parser.add_argument('--files', help='Path to Folder.')
    parser.add_argument('--driver', help='Show driver info.')
    args: Namespace = parser.parse_args()
    data = ''

    if args.files and not args.driver and not args.desc:
        data = build_report(args.files)
    if args.driver:
        data = build_report(args.files, driver=args.driver)
    if args.asc:
        data = build_report(args.files, order=False)
    if args.desc and not args.asc:
        data = build_report(args.files, order=True)

    return data


if __name__ == '__main__':
    print_report(main())
