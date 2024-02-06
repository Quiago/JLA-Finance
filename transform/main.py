import pandas as pd
import argparse

def _get_parser():
    parser = argparse.ArgumentParser(description='Clean the data extracted')    
    parser.add_argument('--cities',
                        default= '../data/cities_and_postal_codes.csv', 
                        help='The path of the csv with the cities and their postal codes', 
                        type=str
                        )   
    return parser

def _read_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

def _convert_to_list(string):
    new_string = []
    if ',' in string:
      for s_split in string.split(','):
        new_string.append(s_split)
      return new_string
    else:
      new_string.append(string)
      return new_string

def _only_numbers(string):
    new_strings = []
    numbers = [str(n) for n in range(0,11)]
    if len(string) == 1:
      string = string[0]
      new_string = ''
      for char in string:
        if char == '–':
          new_string += '+'
        elif char in numbers:
          new_string += char    
      new_strings.append(new_string)
      return new_strings    
    else:
      for element in string:
        new_string = ''
        for char in element:
          if char == '–':
           new_string += '+'
          elif char in numbers:
            new_string += char
        if new_string == '':
          continue
        new_strings.append(new_string)
      return new_strings    
def _delete_ranges(string):
    new_strings = []
    if len(string) == 1:
      string = string[0]
      if '+' in string:
        splitting_string = string.split('+')
        low_limit = int(splitting_string[0])
        high_limit = int(splitting_string[1]) + 1
        for n in range(low_limit, high_limit):
          number = str(n)
          if string.startswith('0'):
            number = '0' + number
          new_strings.append(number)
        return new_strings  
      else:
        new_strings.append(string)
        return new_strings  
    else:
      for element in string:
        if '+' in element:
          splitting_string = element.split('+')
          low_limit = int(splitting_string[0])
          high_limit = int(splitting_string[1]) + 1
          for n in range(low_limit, high_limit):
            number = str(n)
            if element.startswith('0'):
              number = '0' + number
            new_strings.append(number)  
        else:
          new_strings.append(element)   
      return new_strings


def _check_postal_code_len(string):
    new_strings = []
    if len(string) == 1:
      string = string[0]    
      if len(string) > 5:
        len_postal_code = 5 
        left = len(string) % len_postal_code    
        if left:
            string = string[:-left] 
        new_strings = [string[i:i+len_postal_code] for i in range(0, len(string), len_postal_code)] 
        return new_strings
      else:
        new_strings.append(string)
        return new_strings  
    else:   
      for element in string:
        if len(element) > 5:
          len_postal_code = 5   

          left = len(element) % len_postal_code 

          if left:
              element = element[:-left] 
          for i in range(0, len(element), len_postal_code):
            new_strings.append(element[i:i+len_postal_code])    
        else:
          new_strings.append(element)   
      return new_strings   


def _cleaning(csv_path):
    df = _read_data(csv_path)
    clean_rows = (df['postal_code']
               .apply(lambda string: string.replace('\n', ''))
               .apply(lambda string: _convert_to_list(string))
               .apply(lambda string: _only_numbers(string))
               .apply(lambda strings: _delete_ranges(strings))
               .apply(lambda strings: _check_postal_code_len(strings))
               .apply(lambda strings: ', '.join(str(string) for string in strings))
               )
    
    df['postal_code'] = clean_rows
    df.to_csv('../data/cities_postal_code_clean.csv', index=False)


if __name__ == '__main__':
    args = _get_parser().parse_args()
    _cleaning(args.cities)