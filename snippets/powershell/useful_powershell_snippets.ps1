#########
# ABOUT #
#########

# The following snippets are provided for reference. They are meant for
# general reference and not specific application. But, they should provide
# some idea of how you might use them.



#################################
# SEARCH FOR FILES BY EXTENSION #
#################################

# Search current directory and all subdirectories for files ending with .py
Get-ChildItem -Recurse -Filter "*.py"

# Same as above, but searching a specified path instead
Get-ChildItem -Path "C:\users\user.name\Documents" -Recurse -Filter "*.py"

# Basically the same, but no path specified, and only outputs paths.
# Abbreviated version: ls -r -inc "*.py" | % { $_.FullName }
Get-ChildItem -Recurse -Include "*.py" | ForEach-Object { $_.FullName }

#####################################
# END SEARCH FOR FILES BY EXTENSION #
#####################################



###################
# READ TEXT FILES #
###################

# Read the first five lines of a text file.
Get-Content .\tst.txt -TotalCount 5

# Read the last five lines of a text file.
Get-Content .\tst.txt Tail 5

# Find all occurrences of "numpy" in text files w/ a .py extension
# in the current working directory
Select-String -Path .\*.py -Pattern 'numpy'

# Find a string in subdirectories
Get-ChildItem -Path C:\Windows\System32\*.txt -Recurse | Select-String -Pattern 'Microsoft' -CaseSensitive

#######################
# END READ TEXT FILES #
#######################
