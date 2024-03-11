import sys

class ArgReader:
    args = {} 

    def __init__(self, filename):
        with open(f"{filename}", "r") as file:
            # Remove comments, newlines, and spaces. Now each equality is an entry in the list.
            arg_list = [f.strip().replace(" ", "") for f in file.readlines() if not f.startswith('#')]
            
            for arg_line in arg_list:
                arg, value = arg_line.split("=")
                
                try:
                    # All values are casted to ints except probabilites.
                    if arg in ["prob_crossover", "prob_mutation"]:
                        self.args[arg] = float(value)
                    else:
                        self.args[arg] = int(value)
                except:
                    print("ERROR: could not cast value. Check your arguments file.")
                    sys.exit(1)

    def set(self, arg, value):
        self.args[arg] = value

    def get(self, arg):
        return self.args[arg]
    
    def get_all(self):
        return self.args