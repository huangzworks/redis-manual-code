def base10_to_base36(number):
    alphabets = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    while number != 0 :
        number, i = divmod(number, 36)
        result = (alphabets[i] + result)

    return result or alphabets[0]
