''' Function Based Weather Man App '''


import os
import sys
from collections import namedtuple

# defined a named tuple for the columns in the data
weather_data = namedtuple(
        "weather_data",
        [
            "PKT",
            "MaxTemperatureC",
            "MeanTemperatureC",
            "MinTemperatureC",
            "DewPointC",
            "MeanDewPointC",
            "MinDewpointC",
            "MaxHumidity",
            "MeanHumidity",
            "MinHumidity",
            "MaxSeaLevelPressurehPa",
            "MeanSeaLevelPressurehPa",
            "MinSeaLevelPressurehPa",
            "MaxVisibilityKm",
            "MeanVisibilityKm",
            "MinVisibilitykM",
            "MaxWindSpeedKmh",
            "MeanWindSpeedKmh",
            "MaxGustSpeedKmh",
            "Precipitationmm",
            "CloudCover",
            "Events",
            "WindDirDegrees"
        ]
    )


''' function that takes command line arguments and processes the files and
folders for extracting data '''


def process_folder(arguments):

    data = []
    files = os.listdir(arguments[2])

    for file in files:
        if arguments[1] in file:
            with open(
                    arguments[2]
                    + "/"
                    + file
                    ) as file_object:
                for line in file_object:
                    temp_tuple = line.strip().split(",")
                    if not temp_tuple or "<" in temp_tuple[0]:
                        break
                    if temp_tuple[0].isalpha() or temp_tuple == [""]:
                        continue
                    data.append(weather_data._make(temp_tuple))

    return data


''' task 01 to extract values of highest temperature and day, lowest
temperature and day and highest humidity and day in an year '''


def yearly_value_temperatures_and_humidity(data):

    max_temp = float("-inf")
    min_temp = float("inf")
    max_humid = float("-inf")

    def resolve_date(date):
        date = date.split("-")
        date[1] = mapping_months(int(date[1]))
        date.pop(0)
        s = " "
        return s.join(date)

    for extracted_tuple in data:

        # finding maximum temperature
        if extracted_tuple.MaxTemperatureC != "" and max_temp < \
                int(extracted_tuple.MaxTemperatureC):
            max_temp = int(extracted_tuple.MaxTemperatureC)
            max_temp_day = resolve_date(extracted_tuple.PKT)

        # finding minimum temperature
        if extracted_tuple.MinTemperatureC != "" and min_temp > \
                int(extracted_tuple.MinTemperatureC):
            min_temp = int(extracted_tuple.MinTemperatureC)
            min_temp_day = resolve_date(extracted_tuple.PKT)

        # finding maximum humidity
        if extracted_tuple.MaxHumidity != "" and max_humid < \
                int(extracted_tuple.MaxHumidity):
            max_humid = int(extracted_tuple.MaxHumidity)
            max_humid_day = resolve_date(extracted_tuple.PKT)

    result = \
        [
            max_temp, max_temp_day,
            min_temp, min_temp_day,
            max_humid, max_humid_day
        ]

    return result


''' task 02 to extract values of highest average temperature, lowest average
temperature and average humidity in a month '''


def monthly_average_temperature_and_humidity(data):

    high_avg_temp = 0
    high_avg_temp_count = 0
    low_avg_temp = 0
    low_avg_temp_count = 0
    mean_avg_humid = 0
    mean_avg_humid_count = 0

    for extracted_tuple in data:

        # finding highest average temperature
        if extracted_tuple.MaxTemperatureC != "":
            high_avg_temp += int(extracted_tuple.MaxTemperatureC)
            high_avg_temp_count += 1

        # finding lowest average temperature
        if extracted_tuple.MinTemperatureC != "":
            low_avg_temp += int(extracted_tuple.MinTemperatureC)
            low_avg_temp_count += 1

        # finding mean average humidity
        if extracted_tuple.MeanHumidity != "":
            mean_avg_humid += int(extracted_tuple.MeanHumidity)
            mean_avg_humid_count += 1

    result = \
        [
            int(high_avg_temp / high_avg_temp_count),
            int(low_avg_temp / low_avg_temp_count),
            int(mean_avg_humid / mean_avg_humid_count)
        ]

    return result


''' task 03 to visualize a chart for highest temperature and lowest
temperature of each day in a month '''


def monthly_chart_temperature_and_humidity(data):

    chart = dict()
    chart = {"max_temp": [], "min_temp": []}

    for extracted_tuple in data:

        # finding highest average temperature
        if extracted_tuple.MaxTemperatureC != "":
            chart["max_temp"].append(extracted_tuple.MaxTemperatureC)

        # finding lowest average temperature
        if extracted_tuple.MinTemperatureC != "":
            chart["min_temp"].append(extracted_tuple.MinTemperatureC)

    return chart


''' a utility function for mapping month names against the month number '''


def mapping_months(month_number):

    month_name = \
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]

    return month_name[month_number - 1]


''' a utility function to parse the command line arguments into usable form '''


def command_line_parsing():

    arguments = []
    arg = sys.argv[1:]

    for x in arg:
        arguments.append(x)

    if "/" in arguments[1]:
        arguments[1] = arguments[1].split("/")
        arguments[1][1] = mapping_months(int(arguments[1][1]))
        s = "_"
        arguments[1] = s.join(arguments[1])

    return arguments


''' main function of the program where the execution takes place '''


if __name__ == "__main__":

    arguments = command_line_parsing()

    data = process_folder(arguments)

    if arguments[0] == "-e":
        result = yearly_value_temperatures_and_humidity(data)
        print("Highest:", result[0], "C on", result[1])
        print("Lowest:", result[2], "C on", result[3])
        print("Humid:", result[4], r"% on", result[5])

    elif arguments[0] == "-a":
        result = monthly_average_temperature_and_humidity(data)
        print("Highest Average:", result[0], "C")
        print("Lowest Average:", result[1], "C")
        print("Average Humidity:", result[2], "%")

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
