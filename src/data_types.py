import re
from datetime import datetime
from typing import Union

def adding_integers(a:int,b:int)->int:
    """
    Adding two integers.

    a,b are arguments, a->first integer of type int and b->second integer of type int
    """
    return a+b # returns the sum of integers a,b

def subtracting_integers(a:int,b:int)->int:
    """
    Subtracting two integers.

    a,b are arguments, a->first integer of type int and b->second integer of type int
    """
    return a-b # returns the subtraction of integers a,b

def multiplication_floats(a:float,b:float)->float:
    """
    Multiplying two float values.
    a->first float
    b->second float
    """
    return a*b # returns the multiplication

def division_floats(a:float,b:float)->Union[float,str]:
    """
    Dividing two float values.
    a->first float
    b->second float
    """
    if b == 0:
        return "Division by zero is not allowed"  # Handle division by zero
    return a/b  # returns the division of floats a,b

def concatenation_of_strings(string1:str,string2:str)->str:
    """
    Contenating two strings.
    string1 ,string2 are two differnet string
    """
    return string1+string2

def capitalize_string(string:str)->str:
    """
    Capitalizing the first letter of a string.
    string is a string to be capitalized
    """
    return string.capitalize()  # returns the string with first letter capitalized

def boolean_values(value1:bool,value2:bool)->bool:
    """
    logical AND operation on boolean values.
    value1,value2 are two boolean values
    """
    return value1 and value2

def converting_currency_to_float(currency_str:str)->float:
    """
    Converting curency that formated string to float

    Arguments:
        currency_str(str): Currency string (e.g., "$1,234.56")

    returns float representation value (e.g., 1234.56)
    """
    afterConversion=currency_str.replace("$", "").replace(",","")
    return float(afterConversion)

def validate_date_strings_in_multiple_formats(date_str:str)->bool:
    """
    validates date string in formats: 'YYYY-MM-DD', 'MM/DD/YYYY', 'DD-MM-YYYY'.

    Arguments:
        date_str (str): Date string to validate

    Returns True if valid, otherwise False
    """
    formats=["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y"]
    for format in formats:
        try:
            datetime.strptime(date_str,format)
            return True
        except ValueError:
            continue
    return False

def percentage_calculations(part_value:float,whole_value:float)->float:
    """
    Calculates the percentage of part value over whole value.

    Args:
        part_value (float): The part value.
        whole_value (float): The whole value.

    Returns:
        float: Percentage result (e.g., 25.0 for 25%).
    """
    if whole_value==0:
        return 0.0
    return float(part_value/whole_value)*100

def difference_in_percentage(old_value:float,new_value:float)->float:
    """Calculates the percentage change from old value to new value.

    Args:
        old_value (float): Original/Old value.
        new_value (float): New value.

    Returns:
        float: Percentage difference.
    """
    if old_value == 0:
        return float('inf') if new_value != 0 else 0.0
    return ((new_value-old_value)/abs(old_value))*100

# Example usage (for development/testing only)
if __name__ == "__main__":
    print(adding_integers(10, 20))
    print(subtracting_integers(30, 15))
    print(multiplication_floats(2.5, 4.0))
    print(division_floats(10.0, 2.0))
    print(concatenation_of_strings("Hello ", "World"))
    print(capitalize_string("hello world"))
    print(boolean_values(True, False))
    print(converting_currency_to_float("$1,234.56"))
    print(validate_date_strings_in_multiple_formats("2025-08-01"))
    print(validate_date_strings_in_multiple_formats("08/01/2025"))
    print(validate_date_strings_in_multiple_formats("01-08-2025"))
    print(percentage_calculations(30, 200))
    print(difference_in_percentage(100, 120))
        

    