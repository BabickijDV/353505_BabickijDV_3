import hexnumbercheck
import decorator

def Task():
    """Solve Task3"""
    dec_check = decorator.decorator(hexnumbercheck.check)
    while True:
        if(dec_check(input("Input str: ").upper())):
            print("Your str is hexadecimal number")
        else:
            print("Your str isn't hexadecimal number")

            

        while True:    
            c = input("Repeate?[Y/N]: ").upper()
            if c != "N" and c != "Y": print("Unknown command. Retry input")
            else: break
        if c == "N": break