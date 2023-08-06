import string

lowercase_letters = string.ascii_lowercase
LWS = '!@#$%^&:()?;>.<,|\+=_-~`/*'
DI = '1234567890'
base = ''

def EncodeToPhantom(data=str):
    global base
    base = ''
    for letter in data:
        if letter in lowercase_letters:
            RL = lowercase_letters.index(letter)
            RL = LWS[RL]
            base = base + RL
        elif letter in DI:
            base = base + lowercase_letters[DI.index(letter)]
        elif letter == ' ':
            base = base + '•'
           
    return(base)

def DecodeFromPhantom(data=str):
    global base
    base = ''
    data = data.lower()
    for letter in data:
        if letter in LWS:
            base = base + lowercase_letters[LWS.index(letter)]
        elif letter in lowercase_letters:
            base = base + DI[lowercase_letters.index(letter)]
        elif letter == '•':
            base = base + ' '
    return(base)


