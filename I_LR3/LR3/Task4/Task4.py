import separator

def Task():
    """Solve Task4"""
    str = "So she was considering in her own mind, " \
    "as well as she could, for the hot day made her " \
    "feel very sleepy and stupid, whether the pleasure " \
    "of making a daisy-chain would be worth the trouble of " \
    "getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    while True:
        ls = separator.sep_str(str)
        print("Count of words: ", len(ls))
        print("Words with an even number of letters: ", list(elem for elem in ls if len(elem) % 2 == 0))

        shortest_a_word = ""
        dc = {}
        for elem in ls:
            if dc.get(elem) is None: dc[elem] = 1
            else: dc[elem] += 1
            if ((len(elem) < len(shortest_a_word) or shortest_a_word == "") and elem.startswith("a")): shortest_a_word = elem    
        if(shortest_a_word != ""): print("Shotest word starts  with 'a': ", shortest_a_word)
        else: print("No word starts  with 'a'")

        print("Repeated words: ", end = "")
        for key, value in dc.items():
            if value > 1: print(key, end = " ")
        print("")

        while True:    
            c = input("Repeate?[Y/N]: ").upper()
            if c != "N" and c != "Y": print("Unknown command. Retry input")
            else: break
        if c == "N": break