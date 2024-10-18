import argparse;
import random;
from datetime import datetime
import textwrap;

def main():
  # Handle arguments
  parser = argparse.ArgumentParser(
    prog='knapsackTestCaseGen',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Creates a given number each of small, medium, and large test cases for the knapsack problem.',
    epilog=textwrap.dedent('''
            Each case specifies the target value, coin types, and the quantity of each coin available.
            Format: "casetype, target_value, coin1_value, quantity1, coin2_value, quantity2, ..."
        '''))
  
  parser.add_argument("--file", "-f", required=True, type=argparse.FileType('w'),
                      help="File to print test cases to (Will overwrite data).")
  parser.add_argument("--size", "-s", required=True, type=int,
                      help="Number of test cases to generate.")
  
  args = parser.parse_args()

  # If something went wrong and the file cannot be opened, exit with error
  if (not args.file):
    print("Error opening file.")
    return
  
  # Otherwise, print test cases to file

  # Set ranges for target values and total coin quantities for each test case type
    # Format: [[min_target, max_target], [min_coins, max_coins]]
  testcaseSettings = [
    [[50, 200], [10, 20]],  # Small: target between 50-200, coin values between 10-20
    [[500, 2000], [30, 60]],  # Medium: target between 500-2000, coin values between 20-50
    [[5000, 20000], [300, 800]]  # Large: target between 5000-20000, coin values between 500-1000
]


  # Set the coin values that are not multiples of each other
  coin_values = [3, 7, 11, 13]

  # Set the case types
  testcaseTypes = ["Small", "Medium", "Large"]

  # Set randomization seed
  random.seed(datetime.now().timestamp())
  
  for testSize, (target_range, coin_quantity_range) in enumerate(testcaseSettings):
    for _ in range(args.size):
      target_value = random.randint(*target_range)
      args.file.write(f"{testcaseTypes[testSize]}, {target_value}")

      # Generate a random quantity for each coin type
      for coin_value in coin_values:
        quantity = random.randint(*coin_quantity_range)
        args.file.write(f", {coin_value}, {quantity}")

      args.file.write("\n")

  # Close the file once we are done
  args.file.close()

if __name__ == '__main__':
  main()