# Hana Batio
# email: hbatio@hey.com

import csv
import unittest
import random

# part 1: returns the station_id and date pair that reported the
#  lowest temperature. If a tie occurs, returns one pair at random
def findMinTemp(weather_file):
    minPair = None
    minTemp = float('inf')

    for row in weather_file:
        temp = float(row['temperature_c'])
        if temp == minTemp:
            # randomly decide whether we should replace in case of tie
            minTemp += random.randrange(2)
        if temp < minTemp:
            minTemp = temp
            minPair = (row['station_id'], row['date'])

    return minPair

# part 2: returns the station_id that experienced the most amount
#  of temperature fluctuation across all dates that it reported temperatures for
def findMaxChange(weather_file):
    # observation: dataset in order by station and date; 
    # additional sorting would need to take place for an unordered csv
    prevStation = None
    prevTemp = 0
    tempDiffSum = float('-inf')

    maxChange = float('-inf')
    maxStation = None

    for row in weather_file:
        temp = float(row['temperature_c'])
        currStation = row['station_id']

        if currStation != prevStation:
            if tempDiffSum > maxChange:
                maxStation = prevStation
                maxChange = tempDiffSum

            prevStation = currStation
            tempDiffSum = 0
            prevTemp = temp
        
        else:
            tempDiffSum += abs(prevTemp - temp)
            prevTemp=temp

    # have to check the last station before returning
    if tempDiffSum > maxChange:
                maxStation = prevStation
                maxChange = tempDiffSum

    return maxStation

# part 3: returns the station_id that experienced the most amount of temperature fluctuation
#  for any given range of dates
def findMaxChangeInRange(weather_file, startDate, endDate):
    # observation: dataset in order by station and date; 
    # additional sorting would need to take place for an unordered csv
    prevStation = None
    prevTemp = 0
    tempDiffSum = float('-inf')

    maxChange = float('-inf')
    maxStation = None

    for row in weather_file:
        # following 3 lines are the only change from part 2
        # verify that date is in range before calculating fluctuation
        date = float(row['date'])
        if startDate > date or endDate < date:
            continue

        temp = float(row['temperature_c'])
        currStation = row['station_id']

        if currStation != prevStation:
            if tempDiffSum > maxChange:
                maxStation = prevStation
                maxChange = tempDiffSum

            prevStation = currStation
            tempDiffSum = 0
            prevTemp = temp
        
        else:
            tempDiffSum += abs(prevTemp - temp)
            prevTemp=temp

    # have to check the last station before returning
    if tempDiffSum > maxChange:
                maxStation = prevStation
                maxChange = tempDiffSum

    return maxStation


# T E S T S

class TestTemperatureDataAnalysisMethods(unittest.TestCase):
    def test_findMinTemp(self):
        print("Running tests on part 1: findMinTemp")

        # case 1
        test1Data = [{'station_id' : '1', 'date':'2000.375', 'temperature_c':'10.500'},
        {'station_id' : '2', 'date':'2000.542', 'temperature_c':'5.400'},
        {'station_id' : '3', 'date':'2000.958', 'temperature_c':'23.000'}]
        self.assertEqual(findMinTemp(test1Data), ('2','2000.542'))

        # case 2
        test2Data = [{'station_id' : '1', 'date':'2000.375', 'temperature_c':'10.500'},
        {'station_id' : '2', 'date':'2000.542', 'temperature_c':'5.400'},
        {'station_id' : '3', 'date':'2000.958', 'temperature_c':'5.400'}]
        self.assertTrue((findMinTemp(test2Data) == ('2','2000.542')) or (findMinTemp(test2Data) == ('3','2000.958')))

    def test_findMaxChange(self):
        print("Running tests on part 2: findMaxChange")

        # case 1
        test1Data = [{'station_id' : '1', 'date':'2000.375', 'temperature_c':'10.500'},
        {'station_id' : '1', 'date':'2000.542', 'temperature_c':'5.400'},
        {'station_id' : '2', 'date':'2000.958', 'temperature_c':'23.000'}]
        self.assertEqual(findMaxChange(test1Data), '1')

        # case 2
        test2Data = [{'station_id' : '1', 'date':'2000.375', 'temperature_c':'10.500'},
        {'station_id' : '1', 'date':'2000.542', 'temperature_c':'5.400'},
        {'station_id' : '2', 'date':'2000.423', 'temperature_c':'23.000'},
        {'station_id' : '2', 'date':'2000.958', 'temperature_c':'-23.000'}]
        self.assertEqual(findMaxChange(test2Data), '2')

        # case 3
        test3Data = [{'station_id' : '1', 'date':'2000.375', 'temperature_c':'5.400'},
        {'station_id' : '1', 'date':'2000.542', 'temperature_c':'10.500'},
        {'station_id' : '2', 'date':'2000.423', 'temperature_c':'23.000'},
        {'station_id' : '2', 'date':'2000.958', 'temperature_c':'-23.000'}]
        self.assertEqual(findMaxChange(test3Data), '2')

    def test_findMaxChangeInRange(self):
        print("Running tests on part 3: findMaxChangeInRange")

        # case 1
        test1Data = [{'station_id' : '1', 'date':'2000.375', 'temperature_c':'10.500'},
        {'station_id' : '1', 'date':'2000.542', 'temperature_c':'5.400'},
        {'station_id' : '2', 'date':'2000.423', 'temperature_c':'23.000'},
        {'station_id' : '2', 'date':'2000.958', 'temperature_c':'-23.000'},
        {'station_id' : '3', 'date':'2005.135', 'temperature_c':'5.400'},
        {'station_id' : '3', 'date':'2005.563', 'temperature_c':'10.500'}]
        self.assertEqual(findMaxChangeInRange(test1Data,2005,2006), '3')

        # case 2
        test2Data = [{'station_id' : '1', 'date':'2000.375', 'temperature_c':'10.500'},
        {'station_id' : '1', 'date':'2000.542', 'temperature_c':'5.400'},
        {'station_id' : '2', 'date':'2000.423', 'temperature_c':'23.000'},
        {'station_id' : '2', 'date':'2000.958', 'temperature_c':'-23.000'},
        {'station_id' : '3', 'date':'2005.135', 'temperature_c':'5.400'},
        {'station_id' : '3', 'date':'2005.563', 'temperature_c':'10.500'}]
        self.assertEqual(findMaxChangeInRange(test2Data,2000,2006), '2')

        # case 3
        test3Data = [{'station_id' : '1', 'date':'2000.375', 'temperature_c':'5.400'},
        {'station_id' : '1', 'date':'2000.542', 'temperature_c':'23.000'},
        {'station_id' : '2', 'date':'2000.423', 'temperature_c':'23.000'},
        {'station_id' : '2', 'date':'2000.958', 'temperature_c':'-23.000'},
        {'station_id' : '3', 'date':'2005.135', 'temperature_c':'5.400'},
        {'station_id' : '3', 'date':'2005.563', 'temperature_c':'10.500'}]
        self.assertEqual(findMaxChangeInRange(test3Data,2000,2006), '2')

def main():
    # read weather data in as a dict per row
    weather_file = csv.DictReader(open("data.csv"))

    print(findMinTemp(weather_file))

    print(findMaxChange(weather_file))

if __name__ == '__main__':
    unittest.main()