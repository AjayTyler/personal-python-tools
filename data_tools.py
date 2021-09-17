import re
import pandas as pd

# -------------------------#
### DATAFRAME OPERATIONS ###
# -------------------------#

def lowercase_columns(df):
    '''Accepts a pandas dataframe and returns it with all column names lowercased.'''
    return df.rename(columns = {c: c.lower() for c in df.columns})

# ---------------------------- #
### END DATAFRAME OPERATIONS ###
# ---------------------------- #

# -------------------- #
### MISC. OPERATIONS ###
# -------------------- #

def convert_month_abb(month_text, year, end_of_month = True):
    '''Takes a 3-letter month abbreviation and translates it to a datetime object. \
    By default, it uses the last day of the month.'''

    clean_text = month_text.lower().strip()
    months = [
        [1, 'January'], [2, 'February'], [3, 'March'], [4, 'April'],
        [5, 'May'], [6, 'June'], [7, 'July'], [8, 'August'], [9, 'September'],
        [10, 'October'], [11, 'November'], [12, 'December']
    ]
    month_integer = [mnth for mnth in months if mnth[1][:3].lower() == clean_text][0][0]
    make_date = pd.to_datetime(f'{year}-{month_integer}-1')

    if end_of_month:
        make_eom = make_date + pd.offsets.MonthEnd(0)
        return make_eom
    else:
        return make_date

# ------------------------ #
### END MISC. OPERATIONS ###
# ------------------------ #

# --------------------- #
### SCRIPT COMPARISON ###
# --------------------- #

def read_local_scripts(script_path_list):
    '''Takes a list of filepaths and returns list of lists like \
    [[script_name, script_text], ...].'''

    results_list = []

    for script in script_path_list:
        with open(script) as f:
            script_text = f.read().strip()
            # I include the view path so that we can match it with the same
            # view in Snowflake. Since filenames can sometimes be wrong, I
            # pull the actual view path from the code.
            script_name = re.findall(
                r'view\s+([\w_\.]+)',
                script_text, flags = re.I | re.M)[0]
            results_list.append([script_name, script_text])
    return results_list

def normalize_query_text(txt):
    # Snowflake automatically adds a trailing space after the comment line
    # (a forever mystery to me on why that is). This controls for that.
    trim_internal_trailing_spaces = re.sub('\s$', '', txt, flags = re.M | re.I)

    # Semicolons aren't required per se, but we need to make sure both scripts
    # either use 'em or don't for the purposes of comparison.
    remove_semicolon = trim_internal_trailing_spaces.replace(';', '')

    return remove_semicolon.lower().strip()

def compare_scripts(script_list_a, script_list_b):
    """The SQL code in script_list_b are expected to match those in script_list_a. \
    In the event of mismatches, script_list_a is assumed to be correct.
    
    Each list is expected to be a list of lists like [[script_name, script_text], ...]"""

    mismatch_list = []

    for record_a in script_list_a:
        a_name = record_a[0]
        a_script = normalize_query_text(record_a[1])

        # Here, we grab the record in script_list_b with the same name as record_a
        b_record = [x for x in script_list_b if x[0] == a_name][0]
        b_script = normalize_query_text(b_record[1])

        scripts_match = a_script == b_script

        if not scripts_match:
            mismatch_list.append(record_a)

    return mismatch_list

def print_mismatches(mismatch_list, list_name = 'Mismatches'):
    if len(mismatch_list) > 0:
        print(f'\n{list_name}')
        [print(f'\t> {x[0]}') for x in mismatch_list]
    else:
        print('No mismatches found.')
    return

# ------------------------- #
### END SCRIPT COMPARISON ###
# ------------------------- #
