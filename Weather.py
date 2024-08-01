# Function based weather man app

import os
import sys
from collections import namedtuple

# defined a named tuple for the columns in the data
weather_data = namedtuple(
        "weather_data",
        [
            "time_zone",
            "max_temperature",
            "min_temperature",
            "max_humidity",
            "mean_humidity",
        ]
    )

# defined a dictionary for mapping months
month_dict = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}


def process_folder(arguments):

    ''' function that takes command line arguments and processes the files and
folders for extracting data '''

    data = []
    files = os.listdir(arguments[2])
    flag = True

    file_paths = \
        [f"{arguments[2]}/{file}" for file in files if arguments[1] in file]

    for file_path in file_paths:
        flag = False
        with open(file_path) as file_object:
            for line in file_object:
                temp_tuple = line.strip().split(",")
                if not temp_tuple or "<" in temp_tuple[0]:
                    break
                if temp_tuple[0].isalpha() or temp_tuple == [""]:
                    continue
                temp_tuple = [temp_tuple[x] for x in sorted(
                    [0, 1, 3, 7, 8])]
                data.append(weather_data._make(temp_tuple))
    if flag:
        return False

    return data


def yearly_value_temperatures_and_humidity(data):

    ''' task 01 to extract values of highest temperature and day, lowest
temperature and day and highest humidity and day in an year '''

    max_temp = float("-inf")
    min_temp = float("inf")
    max_humid = float("-inf")

    def resolve_date(date):
        date = date.split("-")
        date[1] = month_dict.get(int(date[1]), "Invalid month number")
        date.pop(0)
        s = " "
        return s.join(date)

    for extracted_tuple in data:

        # finding maximum temperature
        if extracted_tuple.max_temperature != "" and max_temp < \
                float(extracted_tuple.max_temperature):
            max_temp = float(extracted_tuple.max_temperature)
            max_temp_day = resolve_date(extracted_tuple.time_zone)

        # finding minimum temperature
        if extracted_tuple.min_temperature != "" and min_temp > \
                float(extracted_tuple.min_temperature):
            min_temp = float(extracted_tuple.min_temperature)
            min_temp_day = resolve_date(extracted_tuple.time_zone)

        # finding maximum humidity
        if extracted_tuple.max_humidity != "" and max_humid < \
                float(extracted_tuple.max_humidity):
            max_humid = float(extracted_tuple.max_humidity)
            max_humid_day = resolve_date(extracted_tuple.time_zone)

    result = \
        [
            max_temp, max_temp_day,
            min_temp, min_temp_day,
            max_humid, max_humid_day,
        ]

    return result


def monthly_average_temperature_and_humidity(data):

    ''' task 02 to extract values of highest average temperature, lowest
average temperature and average humidity in a month '''

    high_avg_temp = 0
    high_avg_temp_count = 0
    low_avg_temp = 0
    low_avg_temp_count = 0
    mean_avg_humid = 0
    mean_avg_humid_count = 0

    for extracted_tuple in data:

        # finding highest average temperature
        if extracted_tuple.max_temperature != "":
            high_avg_temp += float(extracted_tuple.max_temperature)
            high_avg_temp_count += 1

        # finding lowest average temperature
        if extracted_tuple.min_temperature != "":
            low_avg_temp += float(extracted_tuple.min_temperature)
            low_avg_temp_count += 1

        # finding mean average humidity
        if extracted_tuple.mean_humidity != "":
            mean_avg_humid += float(extracted_tuple.mean_humidity)
            mean_avg_humid_count += 1

    result = \
        [
            float(high_avg_temp / high_avg_temp_count),
            float(low_avg_temp / low_avg_temp_count),
            float(mean_avg_humid / mean_avg_humid_count),
        ]

    return result


def monthly_chart_temperature_and_humidity(data):

    ''' task 03 to visualize a chart for highest temperature and lowest
temperature of each day in a month '''

    chart = dict()
    chart = {"max_temp": [], "min_temp": []}

    for extracted_tuple in data:

        # finding highest average temperature
        if extracted_tuple.max_temperature != "":
            chart["max_temp"].append(extracted_tuple.max_temperature)

        # finding lowest average temperature
        if extracted_tuple.min_temperature != "":
            chart["min_temp"].append(extracted_tuple.min_temperature)

    return chart


def command_line_parsing():

    ''' a utility function to parse the command line arguments into usable
form '''

    folder_choices = ["Dubai_weather", "lahore_weather", "Murree_weather"]
    arguments = []
    arg = sys.argv[1:]

    for x in arg:
        arguments.append(x)

    temp = arguments[2].split("/")
    if temp[-1] not in folder_choices:
        return False

    if "/" in arguments[1]:
        arguments[1] = arguments[1].split("/")
        arguments[1][1] = month_dict.get(int(arguments[1][1]),
                                         "Invalid month number")
        s = "_"
        arguments[1] = s.join(arguments[1])

    return arguments


def main():

    ''' main function of the program where the execution takes place '''

    arguments = command_line_parsing()

    if arguments:

        data = process_folder(arguments)

        if data:

            if arguments[0] == "-e":
                result = yearly_value_temperatures_and_humidity(data)
                print(f"Highest: {result[0]} C on {result[1]}\n" +
                      f"Lowest: {result[2]} C on {result[3]}\n" +
                      f"Humid: {result[4]}% on {result[5]}")

            elif arguments[0] == "-a":
                result = monthly_average_temperature_and_humidity(data)
                print(f"Highest Average: {result[0]:.2f} C\n" +
                      f"Lowest Average: {result[1]:.2f} C\n" +
                      f"Average Humidity: {result[2]:.2f} %")

            elif arguments[0] == "-c":
                result = monthly_chart_temperature_and_humidity(data)
                print(arguments[2])
                for x in range(len(result["max_temp"])):
                    print(
                        x + 1,
                        " ",
                        "\033[1;32;40m*" * int(result["max_temp"][x]),
                        "\033[1;37;40m",
                        result["max_temp"][x],
                        "C"
                        )
                    print(
                        x + 1,
                        " ",
                        "\033[1;34;40m*" * int(result["min_temp"][x]),
                        "\033[1;37;40m",
                        result["min_temp"][x],
                        "C"
                        )

            elif arguments[0] == "-b":
                result = monthly_chart_temperature_and_humidity(data)
                print(arguments[2])
                for x in range(len(result["max_temp"])):
                    print(
                        x + 1,
                        " ",
                        "\033[1;32;40m*" * int(result["max_temp"][x]),
                        "\033[1;34;40m*" * int(result["min_temp"][x]),
                        "\033[1;37;40m",
                        result["max_temp"][x],
                        "C -",
                        result["min_temp"][x],
                        "C"
                        )
            else:
                print("Enter valid arguments")
        else:
            print("Enter valid arguments")
    else:
        print("Enter valid arguments")


if __name__ == "__main__":

    ''' caller with __name__ '''

    main()
