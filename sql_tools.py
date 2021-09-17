import re
import moz_sql_parser as msp
# moz-sql-parser has been archived, but a fork has been made for continued
# development under mo-sql-parser

def clean_sql_string(sql_txt):
    '''
    Removes front matter (e.g. CREATE OR REPLACE...) and comments from \
    a query string for easier parsing.
    '''

    remove_comments = re.sub(
    # Removes three comment signifiers: /* */, --, and //
        '(/\*.*\*/)|--.*$|//.*$',
        '',
        sql_txt,
        # Flags for Ignorecase and Multiline
        flags = re.I | re.M)
    remove_front_matter = re.sub(
        r'(create(?:\s+|\s+or\s+replace)\s+[\w\._\s\$"]+)(with|select)',
        # Back reference to second capture group
        r'\2',
        remove_comments,
        flags = re.I | re.M)
    return remove_front_matter

def parse_sql_file(sql_file):
    '''
    Reads a text file and parses the SQL within after some cleansing.
    '''

    with open(sql_file, 'r') as f:
        raw_text = f.read()
        clean_text = clean_sql_string(raw_text)
        return msp.parse(clean_text)
