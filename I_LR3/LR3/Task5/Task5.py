def Task():
    """Solve Task5"""
    while True:
        ls = []
        max = 0
        sum = 0
        sum_index = 0

        while True:    
            try:
                number = int(input("Input size of list:"))
                break
            except ValueError:
                print("Input Error. Size is integer number")

        for i in range(number):
            while True:    
                try:
                    number = float(input("Input element of list:"))
                    break
                except ValueError:
                    print("Input Error. Elem is floating number")
            ls.append(number)
            if abs(number) > max: max = number
            if number > 0:
                while sum_index < i:
                    sum += ls[sum_index]
                    sum_index += 1

        print("List: ", ls)
        print("{:<20} {:<20}".format("max(abs)", "sum"))
        print("{:<20} {:<20}".format(max, sum))

        while True:    
            c = input("Repeate?[Y/N]: ").upper()
            if c != "N" and c != "Y": print("Unknown command. Retry input")
            else: break
        if c == "N": break