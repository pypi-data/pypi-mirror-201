class Numbers:

    def isOdd(args):
        "Check if one or more numbers, entered in input, are odd."

        if isinstance(args, int):
            if args % 2 == 1:
                return True
            
            return False

        for arg in args:
            if not isinstance(arg, int) and not isinstance(arg, float):
                return None

            if arg % 2 == 1:
                continue
            else:
                return False
            
        return True


    def isEven(args):
        "Check if one or more numbers, entered in input, are even."

        if isinstance(args, int):
            if args % 2 == 0:
                return True
            
            return False

        for arg in args:

            if not isinstance(arg, int) and not isinstance(arg, float):
                return None

            if arg % 2 == 0:
                continue
            else:
                return False
            
        return True

    def listMultiplication(arg: list):
        "From a given list or tuple in input, calculate the multiplication of the numbers inside it"

        if isinstance(arg, int):
            return arg

        result = 1

        for i in arg:

            if not isinstance(i, int) and not isinstance(i, float):
                return None

            result *= int(i)

        return result

    def listSum(arg: list):
        "From a given list or tuple in input, calculate the addition of the numbers inside it"

        
        if isinstance(arg, int):
            return arg
        

        result = 0

        for i in arg:

            if not isinstance(i, int) and not isinstance(i, float):
                return None

            result += int(i)

        return result
    

class stopwatch:
    "Create as many stopwatch as you need."
    def start():
        "Start a stopwatch. \nNote: The stopwatch needs to be saved into a variable."
        import time
        return time.time()

    def stop(stopwatch):
        "Stop a given stopwatch, and prints out the execution time."
        import time
        elapsed = time.time() - stopwatch
        return elapsed