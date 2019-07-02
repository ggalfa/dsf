import csv
import argparse
from collections import OrderedDict

"""
this execute  the program in terminal:
python3 silver_lower_cust_plan.py -s slcsp.csv -p plans.csv -z zips.csv
"""

# this is parse function of data and reading

def parse_csv(file_path=None, silver_plan_flag=False):
    data = []
    with open(file_path, 'r') as file_object:
        reading = csv.DictReader(file_object)

        if silver_plan_flag:
            for row in reading:
                if row['metal_level'] == 'Silver':
                    data.append(row)
        else:
            for row in reading:
                data.append(row)
        next(reading, None)
    return data

# this is function of write in files

def write_csv(file_path=None, data_dict={}):
    with open(file_path, 'w') as f:
        writer = csv.DictWriter(f, ['zipcode', 'rate'], lineterminator='\n')
        writer.writeheader()

        for zipcode, rates in data_dict.items():
            if len (rates) > 1:
                rates.sort()
                writer.writerow({'zipcode': zipcode, 'rate': rates[1]})
            else:
                writer.writerow({'zipcode': zipcode, 'rate': str(rates)})


parser = argparse.ArgumentParser(
        description='calculate second lowest cost silver plan SLCSP')

parser.add_argument('-s', '--slcsp', 
    help='CSV containing zipcodes', required=True)

parser.add_argument('-p', '--plans', 
    help='CSV containing all  plans in the U.S.', required=True)

parser.add_argument('-z', '--zips', 
    help='a mapping of ZIP Code to county/counties & rate area(s)', required=True)

args = vars(parser.parse_args())

silver_lower_cust_plan = parse_csv(args['slcsp'], False)
plans_silver = parse_csv(args['plans'], True)
zips = parse_csv(args['zips'], False)

silver_rate_area_state = OrderedDict()
for silver_plans in silver_lower_cust_plan:
    silver_zip = silver_plans['zipcode']
    for zip in zips:
        if silver_zip == zip['zipcode']:
            if silver_zip in silver_rate_area_state:

                if silver_rate_area_state[silver_zip]['rate_area'] != zip['rate_area']:
                    silver_rate_area_state[silver_zip] = None
                break
            else:
                silver_rate_area_state[silver_zip] = {
                    'rate_area': zip['rate_area'], 
                    'state': zip['state']
                }

silver_plans = []
resp = OrderedDict()
for zipcode, rate_area_state in silver_rate_area_state.items():
    if not silver_rate_area_state[zipcode]:
        resp[zipcode] = ''
    else:
        for plan in silver_plans:
            if rate_area_state['rate_area'] == plan['rate_area'] and rate_area_state['state'] == plan['state']:
                if zipcode in resp:
                    resp[zipcode].append(plan['rate'])
                else:
                    resp[zipcode] = [plan['rate']]

    if zipcode not in resp:
        resp[zipcode] = ''

write_csv(args['slcsp'], resp)
