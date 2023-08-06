def word_to_number(word):
    # Define a dictionary to map words to their numerical values
    word_to_digit = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
    }

    # Define multipliers for larger numbers
    multipliers = {"thousand": 1000, "million": 1000000, "billion": 1000000000}

    # Replace hyphens with spaces and split the input string into words
    words = word.replace("-", " ").split()

    # Initialize variables to store the current and total values
    current_value = 0
    total_value = 0
    decimal_value = 0
    decimal_places = 0
    is_decimal = False

    # Iterate over each word in the input string
    for word in words:
        # If the word is "and" or "&," ignore it and continue to the next word
        if word in ["and", "&"]:
            continue
        # If the word is "point," set the is_decimal flag and continue to the next word
        elif word == "point":
            is_decimal = True
            continue
        # If the word is in the word_to_digit dictionary and we are in the decimal part,
        # add its value to the decimal value and increment the decimal places
        elif word in word_to_digit and is_decimal:
            decimal_value = decimal_value * 10 + word_to_digit[word]
            decimal_places += 1
        # If the word is in the word_to_digit dictionary, add its value to the current value
        elif word in word_to_digit:
            current_value += word_to_digit[word]
        # If the word is "hundred," multiply the current value by 100
        elif word == "hundred":
            current_value *= 100
        # If the word is in the multipliers dictionary, multiply the current value by the multiplier
        # and add it to the total value, then reset the current value
        elif word in multipliers:
            current_value *= multipliers[word]
            total_value += current_value
            current_value = 0

    # Add the current value to the total value to get the final result
    total_value += current_value

    # If there is a decimal part, add it to the total value
    if is_decimal:
        total_value += decimal_value * 10 ** (-decimal_places)

    return total_value
