import pytest
import math


def to_decimal(snafu):
    decimal = 0
    rank = len(snafu) - 1
    for char in snafu:
        if char == '-':
            decimal += math.pow(5, rank) * -1
        elif char == '=':
            decimal += math.pow(5, rank) * -2
        else:
            decimal += math.pow(5, rank) * int(char)
        rank -= 1
    return decimal


def to_snafu(decimal):
    # Check if the number is 0, in which case the binary representation is simply 0
    if decimal == 0:
        return "0"

    # Initialize an empty list to store the binary digits (bits)
    bits = []

    # Divide the decimal by 5 repeatedly, storing the remainder (modulo operator) at each step
    while decimal > 0:
        bits.append(int(decimal % 5))
        decimal = decimal // 5

    # Loop over checking on too high nr's until everything is ok
    while 3 in bits or 4 in bits:
        for i, bit in enumerate(bits):
            if bit >= 3:
                bits[i] -= 5
                if i == len(bits) - 1:
                    bits.append(1)
                else:
                    bits[i+1] += 1

    # Reverse the list of bits, as we want the most significant bit (MSB) to be the leftmost digit
    bits.reverse()

    # Print the bits
    return "".join([str(x).replace('-1', '-').replace('-2', '=') for x in bits])



# Part 1
with open('data/input25_1.txt', 'r') as f:
    snafu_numbers = f.readlines()
total = 0
for snafu_number in snafu_numbers:
    total += to_decimal(snafu_number.strip())
print(to_snafu(total))


@pytest.mark.parametrize(
    "test_input,expected",
    [(1, "1"), (2, "2"), (3, "1="), (4, "1-"), (5, "10"),
     (10, "20"), (15, "1=0"), (20, "1-0"), (2022, "1=11-2"),
     (12345, "1-0---0"), (314159265, "1121-1110-1=0"),
     (1747, "1=-0-2"), (906, "12111"), (198, "2=0=")])
def test_snafu_1(test_input, expected):
    assert to_snafu(test_input) == expected
