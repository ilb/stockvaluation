from fair_price_calculator import FairPriceCalculator
from json.decoder import JSONDecodeError

import sys
import json
import dicttoxml
import argparse


def main():
    ''' Entry point of 'stockvaluation' program.
    
    Gets a json content from the standart input with params 'ticker' 
    and 'date', convert it to a list and uses as a calculator params. 
    Then write result ('active', 'price') in json format to the standart 
    output. 
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--response-representation', dest='resp_repr', 
                        action='store', default='application/json')

    args = parser.parse_args()
    resp_repr = args.resp_repr
    
    try:
        data = json.load(sys.stdin)
        ticker, date = data['ticker'], data['date']
    except JSONDecodeError:
        raise NameError('JSONDecodeError: wrong input json data, can not convert')

    calculator = FairPriceCalculator(ticker) 
    result = calculator.calculate(date)

    if resp_repr == 'application/json':
        sys.stdout.write(json.dumps(result)) 
    elif resp_repr == 'application/xml':
        xml = dicttoxml.dicttoxml(result, attr_type=False, item_func=lambda x: x[:-1])
        sys.stdout.buffer.write(xml)
    
if __name__ == '__main__':
    main()