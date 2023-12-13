import re
import numpy as np


def extract_digits_line(input_string: str) -> int:
    pattern = r'^\D*(\d).*?(\d)\D*$'

    # Use re.match to find the first match in the string
    match = re.match(pattern, input_string)

    if match:
        # Extract the first and last digits from the captured groups
        first_digit = match.group(1)
        last_digit = match.group(2)
        return int(first_digit) * 10 + int(last_digit)
    else:
        digit_match = re.search(r"\d", input_string)
        if digit_match:
            digit = int(digit_match.group())
            print(f"Edge case for the string `{input_string}´: {digit}")
            return digit * 10 + digit
        else:
            print(f"The following string is not ordered corectly: {input_string}")
            return None


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    return np.sum([extract_digits_line(line.strip()) for line in datatable])



def find_one_digit(input_string, digits_str, digit_i):
    for digit_str_i, digit_str in enumerate(digits_str):
        if digit_str == input_string[digit_i:digit_i + len(digit_str)]:
            print(digit_str, digit_str_i, input_string)
            return int(digit_str_i)
    return None
def extract_digits_line2(input_string: str) -> int:
    digits_int = [str(i) for i in range(10)]
    digits_str = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    # go through the first digits
    for digit_i, digit in enumerate(input_string):
        if digit in digits_int:
            first_digit = int(digit)
            break
        digit_str = find_one_digit(input_string, digits_str, digit_i)
        if digit_str is not None:
            first_digit = digit_str
            break
        if digit_i == len(input_string) - 1:
            print(f"The following string is not ordered corectly: {input_string}")
            return None

    input_rever = input_string[::-1]
    digits_str_rev = [str_i[::-1] for str_i in digits_str]
    for digit_i, digit in enumerate(input_rever):
        if digit in digits_int:
            last_digit = int(digit)
            break
        digit_str = find_one_digit(input_rever, digits_str_rev, digit_i)
        if digit_str is not None:
            last_digit = digit_str
            break
        if digit_i == len(input_string) - 1:
            print(f"The following string is not ordered corectly: {input_string}")
            return None

    return int(first_digit) * 10 + int(last_digit)


def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    return np.sum([extract_digits_line2(line.strip()) for line in datatable])


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 1 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 77
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 54632
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 54019
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
