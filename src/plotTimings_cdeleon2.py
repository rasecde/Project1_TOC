import time
import csv
import argparse
import matplotlib.pyplot as plt

#Same Knapsack solver function from solver script
def knapsack_solver(total_value, coins):
    coins.sort(reverse=True)
    dp = [False] * (total_value + 1)
    dp[0] = True 

    for coin in coins:
        for value in range(coin, total_value + 1):
            if dp[value - coin]:
                dp[value] = True

    if not dp[total_value]:
        return False, []

    coin_combination = []
    current_value = total_value

    while current_value > 0:
        for coin in coins:
            if current_value >= coin and dp[current_value - coin]:
                coin_combination.append(coin)
                current_value -= coin
                break

    return True, coin_combination

#same read test case from csv from solver script
def read_testcases_from_csv(filename):
    test_cases = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            case_type = row[0]
            total_value = int(row[1])
            coins = list(map(int, row[2:]))
            test_cases.append((case_type, total_value, coins))
    return test_cases

#Collect timings for each test case similar to the iteration in the main function of the solver script
def run_and_collect_timings(test_cases):
    timings = [] 

    for _, total_value, coins in test_cases:
        #Start timer
        start_time = time.perf_counter()

        knapsack_solver(total_value, coins)

        # End the timer
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1e6

        #Store the target value and execution time
        timings.append((total_value, execution_time))

    return timings

#plot
def plot_timings(timings):
    target_values = [size for size, _ in timings]  #X-axis: Target values used as size
    execution_times = [time for _, time in timings]  #Y-axis: Execution times used as times obvsly

    #create scatter plot
    plt.scatter(target_values, execution_times, color='blue', label="Execution Time")

    plt.xlabel("Problem Size (Target Value)")
    plt.ylabel("Execution Time (microseconds)")
    plt.title("Knapsack Solver Execution Time vs. Problem Size")
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Knapsack solver for CSV input files.")
    parser.add_argument("csvfile", type=str, help="The CSV file containing knapsack test cases.")
    args = parser.parse_args()

    #Read test cases and collect timings
    test_cases = read_testcases_from_csv(args.csvfile)
    timings = run_and_collect_timings(test_cases)

    #Plot the timings
    plot_timings(timings)

if __name__ == "__main__":
    main()
