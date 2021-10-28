import re
import moz_sql_parser as msp
# import mo_sql_parsing as msp
# moz-sql-parsing has been archived, but a fork has been made for continued
# development under mo-sql-parser. However, I've had problems getting it to
# play nice with Atom + Hydrogen, so we'll stick with the old for now.

def clean_sql_string(sql_txt: str):
    '''
    Removes front matter (e.g. CREATE OR REPLACE...) and comments from \
    a query string for easier parsing.
    '''

    # Postgres syntax is weird sometimes.
    standardize_varchar_cast = re.sub(
        r'character\s+varying',
        'varchar',
        sql_txt,
        flags = re.I | re.M)

    remove_comments = re.sub(
    # Removes three comment signifiers: /* */, --, and //
        r'/\*[\w\s\n,.-]*\*/|--.*$|//.*$',
        '',
        standardize_varchar_cast,
        # Flags for Ignorecase and Multiline
        flags = re.I | re.M)

    remove_front_matter = re.sub(
        # Non-capture groups for front matter; non-greedy match anything
        # before `as with` | `as select`
        r'(?:create(?:\s+|\s+or\s+replace)\s+[\w\._\s\$"]+).*?as\s+(with|select)',
        # Back reference to first capture group (i.e. with / select)
        r'\1',
        remove_comments,
        flags = re.I | re.M | re.DOTALL)

    remove_semicolon = remove_front_matter.replace(';', '')

    strip_spaces = remove_semicolon.strip()

    return strip_spaces

def parse_sql_file(sql_file: str) -> dict:
    '''
    Reads a text file and parses the SQL within after some cleansing.
    '''

    with open(sql_file, 'r') as f:
        raw_text = f.read()
        clean_text = clean_sql_string(raw_text)
        return msp.parse(clean_text)

def list_tables_in_query(parsed_sql: dict) -> list:
    '''
    Takes dictionary object of parsed SQL and return list of all the tables
    in the query.
    '''
    results = []
    def recurse(data, target_list):
        # For some reason, UNION ALL is snake cased in the SQL parser.
        source_references = [
            'from', 'inner join', 'left join', 'right join', 'full outer join',
            'left outer join', 'right outer join', 'with', 'union_all', 'union']

        if type(data) == dict:
            for k in data.keys():
                if k in source_references:
                    recurse(data.get(k), target_list)
                elif k == 'value':
                    recurse(data.get(k), target_list)
        elif type(data) == list:
            for i in data:
                recurse(i, target_list)
        else:
            target_list.append(data)
    recurse(parsed_sql, results)
    return results
