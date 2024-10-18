import csv
import argparse
import time

def knapsack_solver(total_value, coin_data):
    """
    Knapsack solver for the given total value and coins with counts
    coin_data is a list of tuples where each tuple is (coin_value, coin_count)
    """

    #Use a DP array
    dp = [False] * (total_value + 1)
    dp[0] = True  #Base case: a value of 0 can always be achieved

    #Track which coins are used at each step
    used_coins = [{} for _ in range(total_value + 1)] 

    #DP for loop to update achievable values
    for coin_value, max_count in coin_data:
        for value in range(total_value, coin_value - 1, -1):
            for count in range(1, max_count + 1):
                prev_value = value - coin_value * count
                if prev_value >= 0 and dp[prev_value]:
                    dp[value] = True
                    #Update used coins count
                    used_coins[value] = used_coins[prev_value].copy()
                    used_coins[value][coin_value] = (
                        used_coins[value].get(coin_value, 0) + count
                    )

    #check that solutione exists
    if not dp[total_value]:
        return False, {} 

    #retrive coin counts
    solution = used_coins[total_value]

    return True, solution  

def read_testcases_from_csv(filename):
    """
    Read test cases from a CSV file
    Remember the Format: case_type, total_value, coin1_value, coin1_count, coin2_value, coin2_count, ...
    """
    test_cases = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            case_type = row[0]  #Check for small, medium, large
            total_value = int(row[1])  #target value

            #Parse coin-value and coin-count pairs
            coin_data = [(int(row[i]), int(row[i + 1])) for i in range(2, len(row), 2)]
            test_cases.append((case_type, total_value, coin_data))

    return test_cases

def main():
    #Use argparse to accept cmd line args
    parser = argparse.ArgumentParser(description="Knapsack solver for CSV input files.")
    parser.add_argument("csvfile", type=str, help="The CSV file containing knapsack test cases.")
    
    args = parser.parse_args()

    #read in testcase
    test_cases = read_testcases_from_csv(args.csvfile)

    #Iterate over test cases and solve
    for case_type, total_value, coin_data in test_cases:
        print(f"Solving knapsack for {case_type} case with total value: {total_value} and coins: {coin_data}")

        #start timer to calculate complexity
        start_time = time.perf_counter()
        
        solution_exists, coin_combination = knapsack_solver(total_value, coin_data)

        #End timer
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1e6  #Convert time to ms

        if solution_exists:
            #Formatting the test cases in a way that's easier for the verifier to parse
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




