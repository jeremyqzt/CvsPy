import math  

def geometric(num):
    ret,i = 0, 1
    runningSum = 0
    while runningSum < num:
        runningSum += i
        i *=2
        ret += 1
    return ret if runningSum <= num else ret-1

def fib(num):
    # start with [1,1]
    runningTotal = 2

    window = [1,1]
    ret = 2 # Already paying 2

    while runningTotal < num:
        nextSum = window[0] + window[1]
        window[0], window[1] = window[1], nextSum
        runningTotal += nextSum
        ret += 1

    return ret if runningTotal <= num else ret-1

def solution(total_lambs):
    if total_lambs < 2: return 0

    g_pay = geometric(total_lambs)
    s_pay = fib(total_lambs)
    return s_pay - g_pay

print(solution(3))

