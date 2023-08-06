# Module Documentation: qualifying_report
The qualifying_report module provides functionality to read data from two log files 
containing start and end times for each driver's lap, calculates the lap times, sorts the results, 
and writes the output to a new file. 
It also provides functionality to print the leaderboard or driver's information from the generated report.

# Functions
build_report(folder_path: str = '') -> None
This function reads in data from two log files containing start and end times for each driver's lap, 
calculates the lap times, sorts the results, and writes the output to a new file.


print_report(folder_path: str = '', driver_name: str = '', desc: bool = False, asc: bool = False) -> None
This function prints the leaderboard or driver's information from the generated report.


main() -> None
This function parses command-line arguments, builds a report or prints driver information 
based on the provided arguments.

