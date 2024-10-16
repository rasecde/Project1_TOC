import ast
import argparse
import sys

def verify_solution(target_value, coin_combination):
    #calculate sum of list of coin combination
    total_sum = sum(coin_combination)
    
    #check if sum is equal to target
    return total_sum == target_value

def main():
    #use argparse to accept optional filename argument
    parser = argparse.ArgumentParser(description="Verifier for Knapsack solver output.")
    parser.add_argument("filename", nargs="?", help="The file containing solver output (optional).")
    args = parser.parse_args()

    #If filename is provided, read from the file, otherwise, read from sys.stdin
    if args.filename:
        with open(args.filename, 'rb') as file:
            #Read the file in binary mode to filter out null bytes, and then decode to text. Was running into problems earlier with reading in the txt file regularly
            file_content = file.read().replace(b'\x00', b'').decode('utf-8', 'ignore')
            solver_output = file_content.splitlines()
    else:
        solver_output = sys.stdin.readlines()

    # Remove any empty lines or extra newlines from the solver_output
    solver_output = [line.strip() for line in solver_output if line.strip()]

    #process the output from solver linebyline
    i = 0
    while i < len(solver_output):
        #check for a "No solution" case
        if "No solution exists" in solver_output[i + 1]:
            print(f"Skipping case: {solver_output[i].strip()}")
            execution_time_str = solver_output[i + 2].strip() #3rd line has exec time
            print(execution_time_str)
            i += 4  #Skip this block of code (4 lines: description of case, no solution line, exec time, ---- seperator)
        else:
            #Process the case in which there IS a solution
            try:
                output_str = solver_output[i + 2].strip()  #3rd line has dictionary we want to process
                execution_time_str = solver_output[i + 3].strip() #4th line has exec time

                #Convert string to dict using ast library
                output_dict = ast.literal_eval(output_str)
                
                target = output_dict["target"]
                combination = output_dict["combination"]
                
                #call helpfer function to verify
                is_correct = verify_solution(target, combination)
                
                #Modify the output of combination if it's longer than 15. This deals with combinations that are super long
                if len(combination) > 15:
                    combination_str = f"{combination[:15]}..."  #Show first 15 values followed by "..."
                else:
                    combination_str = str(combination)  #Show full combination if it's 15 or less
                
                if is_correct:
                    print(f"Correct solution for target {target} with combination {combination_str}")
                else:
                    print(f"Incorrect solution for target {target} with combination {combination_str}")
                print(execution_time_str)
            except (IndexError, ValueError) as e:
                print(f"Error processing the solver output: {e}")
            
            i += 5  #Move to next block of code (4 lines: description of case, solution line, dictionary, exec time, ---- separator)

if __name__ == "__main__":
    main()


