import csv
import argparse
import time

def knapsack_solver(total_value, coins):
    #Sort coins in descending order to prioritize larger coins when backtracing
    coins.sort(reverse=True)

    #Create a DP array 
    dp = [False] * (total_value + 1)
    dp[0] = True  #Base case: value of 0 can always be achieved

    #create an array that stores whether each value is achievable
    for coin in coins:
        for value in range(coin, total_value + 1):
            if dp[value - coin]:
                dp[value] = True

    #if no solution, return false
    if not dp[total_value]:
        return False, []

    #Backtrack to find the combination of coins used prioritizing larger coins first...greedy backtracing
    coin_combination = []
    current_value = total_value

    while current_value > 0:
        for coin in coins:
            if current_value >= coin and dp[current_value - coin]:
                coin_combination.append(coin)
                current_value -= coin
                break

    return True, coin_combination

def read_testcases_from_csv(filename):
    test_cases = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            case_type = row[0]  #check for small, medium, or large
            total_value = int(row[1])  #value we want to match
            coins = list(map(int, row[2:]))  #coin denominations
            test_cases.append((case_type, total_value, coins))
    return test_cases

def main():
    #Using argparse to accept cmd line arguments
    parser = argparse.ArgumentParser(description="Knapsack solver for CSV input files.")
    parser.add_argument("csvfile", type=str, help="The CSV file containing knapsack test cases.")
    
    #Parse arguments
    args = parser.parse_args()

    #Read testcase from csv file specified in cmd line
    test_cases = read_testcases_from_csv(args.csvfile)

    #Iterate over test cases and solve
    for case_type, total_value, coins in test_cases:
        print(f"Solving knapsack for {case_type} case with total value: {total_value} and coins: {coins}")

        #Start a timer to measure how long each case takes
        start_time = time.perf_counter()
        
        solution_exists, coin_combination = knapsack_solver(total_value, coins)

        #End the timer
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1e6  # Convert time to microseconds

        if solution_exists:
            #formatting the testcases in a way that's easier for the verifier to parse
            print(f"A solution exists for the {case_type} case with total value: {total_value}")
            formatted_output = {"target": total_value, "combination": coin_combination}
            print(formatted_output)
            print(f"Execution time: {execution_time:.2f} microseconds")
        else:
            print(f"No solution exists for the {case_type} case with total value: {total_value}")
            print(f"Execution time: {execution_time:.2f} microseconds")
        print("---------------------------------------------------")

if __name__ == "__main__":
    main()




