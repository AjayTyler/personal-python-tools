import os, functools, time
from typing import Union, Callable

#################################
# MISC. SCRIPT HELPER FUNCTIONS #
#################################

def get_script_directory():
    '''
    Returns the filepath for the currently executing script. This helps to \
    sidestep some of those pesky working directory problems that you can run \
    into when you invoke a script from an unexpected working directory.
    '''
    return os.path.dirname(os.path.realpath(__file__))

def get_filename(filepath: str):
    return os.path.basename(filepath)

def timer(func: Callable):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'Finished {func.__name__!r} in {run_time:.4f} seconds')
        return value
    return wrapper_timer

# This is included purely as an example of using the above-defined decorator.
@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])

####################
# INPUT VALIDATION #
####################

#-------------------------#
# VALIDATION FUNCTIONIONS #
#-------------------------#

# These functions are used in conjunction with the prompt functions
# to prompt users for input from a command line and then validate
# their input against a series of parameters.

def number_validation(
    include_range: range = None,
    exclude_range: range = None,
    min_value: Union[int, float] = None,
    max_value: Union[int, float] = None,
    num_type = None,
    verbose: bool = False) -> Callable:
    '''
    include_range = Python range object. Test fails if input outside of range.
    exclude_range = Python range object. Test fails if input inside of range.
    min_value = Any real number. Test fails if input lower than value.
    max_value = Any real number. Test fails if input higher than value.
    num_type = Any data type. Test failes if input type does not match num_type.
    verbose = Boolean. Changes output for troubleshooting purposes.
    '''
    def run_tests(i: Union[int, float]):
        # First, we check that we're actually working with a number of some kind.
        try:
            if num_type is not None:
                is_number = type(i) == num_type
            else:
                is_number = type(int(i)) == int
        except ValueError:
            expected_num_type = num_type if num_type is not None else 'Number'
            print(f'Expected {expected_num_type}, received {i} -- {type(i)}')
            return False

        # If we're not working with a number, we know our answer.
        if not is_number:
            return False

        # Convenience function so that we don't repeat ourselves as much.
        def append_message_if_failed(test_result: bool, result_list: list, message: str):
            if test_result == False:
                result_list.append(message)

        # This tracks our test results
        test_results = []

        # Begin tests
        if include_range is not None:
            test_result = i in include_range
            append_message_if_failed(test_result, test_results, f'{i} not in include range')

        if exclude_range is not None:
            test_result = i not in exclude_range
            append_message_if_failed(test_result, test_results, f'{i} in excluded range')

        if min_value is not None:
            test_result = i < min_value
            append_message_if_failed(test_result, test_results, f'{i} less than min value')

        if max_value is not None:
            test_result = i > max_value
            append_message_if_failed(test_result, test_results, f'{i} more than max value')
        # End tests

        # If any test failed, it'll be in our test_result list. So, if it's length
        # is 0, we know nothing failed. If we didn't run any specific tests, then
        # we just need to know if our input is a number.
        valid_input = True if len(test_results) == 0 or is_number else False

        # If the verbose flag is true, we'll return an object that includes the
        # test results. Strictly-speaking, probably not great to return different
        # data types, buuuut I wanted the option anyway.
        if verbose:
            return {'valid': valid_input, 'errors': test_results}
        else:
            return valid_input

    # We're going to run this function in an interesting context: inside another
    # function. So, we need to return a function instead of a regular value.
    return run_tests

def string_validation(valid_inputs: list[str] = None):
    '''
    Evaluates whether a given input is a string. Specify `valid_inputs` as \
    a list to specify valid inputs.
    '''
    def run_tests(s: str):
        is_string = type(s) == str

        if valid_inputs is not None and is_string:
            return s in valid_inputs
        else:
            return is_string
    return run_tests

#------------------#
# PROMPT FUNCTIONS #
#------------------#

def prompt_user(input_message: str, test_function: Callable):
    while True:
        # Ask the user for input.
        user_input = input(input_message).strip()
        # Run the test function on the input to see if it passes.
        test_result: bool = test_function(user_input)
        # If the test is True, then break the loop.
        if test_result:
            break
        # Otherwise, loop around again.
        else:
            continue
    # If the test passes, return the input.
    return user_input

def yes_no_validation(input_message: str):
    user_input = prompt_user(
        input_message,
        string_validation(['yes', 'no', 'y', 'n']))
    if user_input.lower().strip() in ['yes', 'y']:
        return True
    else:
        return False
