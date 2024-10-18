import csv
import argparse
import time
import matplotlib.pyplot as plt

def knapsack_solver(total_value, coin_data):
    """
    Knapsack solver for the given total value and coins with counts.
    coin_data is a list of tuples where each tuple is (coin_value, coin_count).
    """
    dp = [False] * (total_value + 1)
    dp[0] = True  # Base case: a value of 0 can always be achieved

    used_coins = [{} for _ in range(total_value + 1)]  # Track coins used

    for coin_value, max_count in coin_data:
        for value in range(total_value, coin_value - 1, -1):
            for count in range(1, max_count + 1):
                prev_value = value - coin_value * count
                if prev_value >= 0 and dp[prev_value]:
                    dp[value] = True
                    used_coins[value] = used_coins[prev_value].copy()
                    used_coins[value][coin_value] = (
                        used_coins[value].get(coin_value, 0) + count
                    )

    if not dp[total_value]:
        return False, {}

    solution = used_coins[total_value]
    return True, solution

def read_testcases_from_csv(filename):
    """
    Read test cases from a CSV file.
    Format: case_type, total_value, coin1_value, coin1_count, ...
    """
    test_cases = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            case_type = row[0]
            total_value = int(row[1])
            coin_data = [(int(row[i]), int(row[i + 1])) for i in range(2, len(row), 2)]
            test_cases.append((case_type, total_value, coin_data))
    return test_cases

def main():
    parser = argparse.ArgumentParser(description="Knapsack solver and plotter for CSV input files.")
    parser.add_argument("csvfile", type=str, help="The CSV file containing knapsack test cases.")
    args = parser.parse_args()

    test_cases = read_testcases_from_csv(args.csvfile)

    total_coins_list = []  #X-axis data
    execution_times = []   #Y-axis data
    colors = []            #Color for solution found or not

    for case_type, total_value, coin_data in test_cases:
        total_coins = sum(count for _, count in coin_data)  #Total coins available

        start_time = time.perf_counter()
        solution_exists, _ = knapsack_solver(total_value, coin_data)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1e6  #Convert to ms

        total_coins_list.append(total_coins)
        execution_times.append(execution_time)

        if solution_exists:
            colors.append('green')  # Solution found
        else:
            colors.append('red')  # No solution found

    #Plot results
    plt.scatter(total_coins_list, execution_times, c=colors)
    plt.xlabel("Total Number of Coins")
    plt.ylabel("Execution Time (microseconds)")
    plt.title("Knapsack Solver Execution Time vs Total Coins")
    plt.legend(["Solution Found", "No Solution"], loc="upper right")
    plt.show()

if __name__ == "__main__":
    main()
