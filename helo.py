#!/usr/bin/python3
import sys
import math
import tempfile
import pydot
from subprocess import check_call
 
def game_winner(game_result):
    winner = game_result[len(game_result) - 1][0]
    return winner

def log2(x):
    return math.log10(x) / math.log10(2)

def is_pow2(x):
    y = log2(x)
    return y == int(y)

def round_up_to_pow2(x):

    power = 1
    while power < x:
        power = power * 2

    return power

def main():

    if len(sys.argv) < 2:
        print("specify file")
        quit()
    fnam = sys.argv[1]
    file = open(fnam, encoding="utf-8", errors="ignore")

    members = file.read().splitlines()
    file.close()

    res = game(members, choose)
    winner = game_winner(res)
    print("Nyert:", winner)
    draw_graph(res)

def normalize(members):

    if is_pow2(len(members)):
        return members
    
    input_len = len(members)
    result_len = round_up_to_pow2(len(members))
    ext_len = result_len - input_len
    splitpoint = input_len - ext_len

    result = []
    for i in range(0, splitpoint):
        result.append(members[i])
    for i in range(splitpoint,input_len):
        result.append(members[i])
        result.append(None)

    return result

def game(actuals, chooser):

    assert(len(actuals) > 0)
    actuals = normalize(actuals)
    assert(is_pow2(len(actuals)))
    results = []

    while True:
        results.append(actuals)
        if len(actuals) == 1:
            break
        else:
            actuals = perform_round(actuals, chooser)

    return results

def choose(a, b):

    print("Melyik a jobb?")
    print("a:",a, "b:", b)

    while True:

        jobb = input()

        if jobb == "a":
            return a
        if jobb == "b":
            return b
        if jobb == "q":
            return None
        print("a vagy b")
    
def perform_round(parties, chooser):

    round_winners = []
    for match_num in range(int(len(parties) / 2)):

        p1 = parties[int(match_num * 2)]
        p2 = parties[int(match_num * 2 + 1)]
        if p2 is None:
            winner = p1
        else:    
            winner = chooser(p1, p2)

        if winner is None:

            print("Aborted")
            quit()

        round_winners.append(winner)
        
    return round_winners

def draw_graph(game_result):

    script = "digraph { a -> b }"
    fnam = create_graph_image(script)
    print(fnam)

def create_graph_image(script):

    script_name = "/tmp/graph.dot"
    image_name = "/tmp/graph.png"
    file = open(script_name, "w")
    file.write(script)
    file.close()

    check_call(["dot", '-Tpng', script_name, "-o", image_name])
    check_call(["eog", image_name])





if __name__ == "__main__": 
    main()