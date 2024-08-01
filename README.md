# Weather Man Function
This is a function based implementation of a test project for Python. This project can be run for multiple configurations.

### Different Datasets
- Dubai_weather
- lahore_weather
- Murree_weather

### Different Date formats
- year
- year/month

### Different identifiers
- **e**: Extract values of highest temperature and day, lowest
temperature and day and highest humidity and day in an year.
- **a**: Extract values of highest average temperature, lowest average
temperature and average humidity in a month.
- **c**: Visualize a chart seperately for highest temperature and lowest
temperature of each day in a month.
- **b**: Visualize a chart combined for highest temperature and lowest
temperature of each day in a month.

## Example runs
- python Weather.py -e 2008 Dubai_weather
- python Weather.py -a 2012/6 lahore_weather
- python Weather.py -c 2008/6 Dubai_weather
- python Weather.py -b 2010/8 Murree_weather
