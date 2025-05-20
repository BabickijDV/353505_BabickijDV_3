import generator
import UserInput

def Task():
    """Solve Task2"""
    while True:
        ls = []
        while True:    
            c = input("Generate numbers?[Y/N]").upper()
            if c != "N" and c != "Y": print("Unknown command. Retry input")
            else: break
        if c == "Y":
            ls = list(generator.gen_list())
            print("Generated list: ",ls)
        else:
            UserInput.user_input(ls)
            print("List: ",ls)
        sum = 0
        count_positive = 0
        for number in ls:
            if number > 0:
                count_positive += 1
            sum += number
        print("{:<10} {:<10}".format("sum", "count of positive numbers"))
        print("{:<10} {:<10}".format(sum, count_positive))
        


        while True:    
            c = input("Repeate?[Y/N]: ").upper()
            if c != "N" and c != "Y": print("Unknown command. Retry input")
            else: break
        if c == "N": break    