from fair_price_calculator import FairPriceCalculator
import sys
import json
from json.decoder import JSONDecodeError
import dicttoxml


def main():
    ''' Entry point of 'stockvaluation' program.
    
    Gets a json content from the standart input with params 'ticker' 
    and 'date', convert it to a list and uses as a calculator params. 
    Then write result ('active', 'price') in json format to the standart 
    output. 
    '''
    try:
        data = json.load(sys.stdin)
        ticker, date = data['ticker'], data['date']
    except JSONDecodeError:
        raise NameError('JSONDecodeError: wrong input json data, can not convert')

    calculator = FairPriceCalculator(ticker)
    
    result = calculator.calculate(date)
    xml = dicttoxml.dicttoxml(result, attr_type=False, item_func=lambda x: x[:-1])
    sys.stdout.buffer.write(xml)
    
if __name__ == '__main__':
    main()