#!/usr/bin/env/python3

"""
------------------------------------------------------------------------------------------------
 @authors       Nicola Lea Libera (117073), Laura Simon (116992), Chiranjeevi Janjanam()
------------------------------------------------------------------------------------------------
 Description: This script simply evaluates the pressure data from different levels
              to define a fitting pressure threshold for the game.
------------------------------------------------------------------------------------------------
"""

import json
from glob import glob


def main():
    num_of_entries = 0
    accumulated_sum = 0
    json_data = glob("data for threshold determination/*.json", recursive=True)
    for file in json_data:
        tmp = json.load(open(file))
        max_val = [0] * 20
        #print("New file: " + str(file))
        for key in tmp['pressure']:
            #print("key: " + str(key))
            for i in range(len(max_val)):
                if float(key) > max_val[i]:
                    max_val[i] = float(key)
                    max_val.sort()
                    break
            #print("New max vals: " + str(max_val))

        for entry in max_val:
            accumulated_sum += tmp['pressure'][str(entry)] * float(entry)
            num_of_entries += tmp['pressure'][str(entry)]
    threshold = accumulated_sum / float(num_of_entries)
    print("Threshold: " + str(threshold))


if __name__ == '__main__':
    main()
