# Summary
Tips, tools, and snippets that are useful for common tasks.

# Using this Repo
## Requirements
You will need the following packages:

* pandas
* moz-sql-parser

## Importing the Modules
To import the modules within this repo, the easiest way is probably to add it to your Python session's path variable. The example below shows an example of using a full path to the repo, but you can use relative paths as well.

```Python
import os, sys
# We prefix our string with an 'r' to make it a raw string, so we don't have
# to escape our backslashes.
aap_tools = os.path.abspath(r'C:\Users\user.name\DevLocal\advanced-analytics-python-tools')
# We append the directory to our system's path variables so that it knows to
# look in that directory.
sys.path.append(aap_tools)

# We import 'data_tools' from our module and alias it as 'dat'.
import data_tools as dat
```

An example use case:

```Python
import os, sys
aap_tools = os.path.abspath('../../advanced-analytics-python-tools')
sys.path.append(aap_tools)

import data_tools as dat
import pandas as pd

# Read .csv into a dataframe and then lowercase the columns for convenience
df = (
    pd.read_csv('some_csv_path.csv')
    .pipe(dat.lowercase_columns))
```

# Notes
Here are a few things that you may find useful for the Git / Python side of things.

## I Need to Undo a Commit
I feel ya. Let me introduce you to this lifesaver of a blog article: [How to Undo Almost Anything with Git](https://github.blog/2015-06-08-how-to-undo-almost-anything-with-git/). I've used it many times myself. Just scan the headings until you find the description that matches your situation.

## Using a Virtual Environment with Python and pipenv
Sometimes, you may have libraries with conflicting dependencies--tools that require specific versions of other libraries to function. Or, a library that you use might not yet work with the most recent version of Python that you have installed. In these cases, you can save yourself a lot of time and headaches by using virtual environments to encapsulate different sets of tools.

We'll assume that you've installed Python and can invoke pip from a command line session. For our example, we'll use a tool called [pipenv](https://pipenv.pypa.io/en/latest/)--a Python package that makes the process of creating a virtual environment pretty easy.

Open a terminal session. I'll assume PowerShell for our examples, but the process is the same via cmd.exe or Bash / Zsh / whatever shell you prefer to use. Then, enter:

```PowerShell
pip install pipenv
```

Next, navigate to or create a directory for where we want to organize our virtual environment's scripts and package list. In our example, let's say that you have all your Git repos in `C:\Users\user.name\DevLocal`; we'll go ahead and create a folder here to keep all our code in one general area. Let's call our new folder 'Sandbox' since we'll use this as a generic environment.

If you created a folder, navigate to it in PowerShell (e.g. `cd "C:\Users\user.name\DevLocal\Sandbox"`) and enter the following to install a package:

```PowerShell
pipenv install pandas
```

The first time that you use pipenv in a directory to install a package, it will create a virtual environment named after the directory. It will also generate a pipfile--a plaintext list of the packages you've installed in the virtual environment.

From here on out, you can use `pipenv` much like you would `pip`, but just be sure to run it in the directory that you created to keep track of your virtual environment's packages. Otherwise, you'll end up with a loooooot of unnecessary virtual environments.

While we've got this open, we might as well add a few other useful packages.

```PowerShell
pipenv install numpy
pipenv install requests
pipenv install jupyterlab
```

## Using Python with Atom Text Editor + Hydrogen
If you'd like a convenient, flexible, and configurable REPL for Python, I'd recommend using Atom and installing the Hydrogen package. This is a two-part process: setting up Atom, and then connecting your virutal environment to it.

### Atom + Hydrogen Setup
1. Download and install [Atom](https://atom.io/)
2. Open it up and go to File > Settings (or just use Ctrl + Comma)
3. (Optional) Disable the wrap-guide
    - Do you like the vertical line in the editor? No? Then do this:
    - Go to Packages, search 'Installed Packages' for 'guide' and disable the wrap-guide package.
4. Click Install, and search for 'Hydrogen' and install it (it's usually the top featured package, so you might just see it without a need to search for it).
5. (Alternate, but likely) Manually install Hydrogen from the command line
    - Due to Argo security things, you might not be able to install Hydrogen via Atom's built-in package browser
    - To install the package, open up PowerShell and enter `apm install hydrogen`
    - In the event that you need to update the package, you can run `apm update hydrogen`
6. (Optional) Specify kernel directory
    - I often prefer to set my Hydrogen kernel to start in the current directory of the file
    - This mostly effects how you specify the paths in your script
    - To make this change:
        - Open up your Atom settings, go to Packages, search for 'Hydrogen', and select settings from the result
        - Pick 'Current directory of the file' from the dropdown under 'Directory to start kernel in'

### Python Setup
On the Python side of things, I'm assuming that you are using a virtual environment as described above. As we did in that example, open a PowerShell session and navigate to the folder that contains the pipfile for the virtual environment and run the following commands:

* `pipenv install ipykernel` (if you've not already installed it)
* `pipenv shell` (this opens a terminal session inside your virtual environment)
* `py -m ipykernel install --user --name=Sandbox` (this installs the IPython kernel for your virtual environment and labels it 'Sandbox')

Now, Hydrogen can see your virtual environment's Python and packages.

### Run Code Inline Using Atom
In Atom, when you are editing a .py file, you can hit `Ctrl + Enter` or `Shift + Enter` and Hydrogen will run the code. When you first run something, it will prompt you to pick a kernel. Select the one that has the packages that you want to run (assuming 'Sandbox' in our case). If you don't see your virtual environment, you may need to tell Hydrogen to refresh its kernels (`Ctrl + Shift + P` to open the command palette and then type `Hydrogen` and find the option that refreshes the kernels).

## Running Scripts from the Command Line in a Virtual Environment on Windows
It can be handy to alias your virtual environment activation so that you can easily access it from anywhere on your system. What follows is an example for Powershell (so, assuming a Windows machine here) activating a virtual environment generated by pipenv. Obviously, you'll replace the username (`bobby.mcferrin` in our example) and virtual environment's directory (`sandbox-7sUbloXC`) with your username and environment.

```PowerShell
Set-Alias -Name Sandbox -Value C:\Users\bobby.mcferrin\.virtualenvs\sandbox-7sUbloXC\Scripts\activate.ps1
```

Now, to activate the environment (so that your script will run), just type `Sandbox`. To deactivate the virtual environment, just type `deactivate`.

But who wants to look up the path to a script that activates your virtual environment to set up this alias every time? What we can do, instead, is create a PowerShell profile that will automatically do this for you each time you start a PowerShell session.

The quickest way to do this is to open up PowerShell and type:

```PowerShell
New-Item -Path $profile -ItemType File -Force
```

This will create a file under your user's `Documents\WindowsPowerShell` called `Microsoft.PowerShell_profile.ps1`. Open this up with a text editor and add the `Set-Alias` command that we defined above. Save the file, and all your **future** PowerShell sessions should now let you invoke `Sandbox` to activate your virtual environment without having to re-define the alias. (You'll need to close and re-open PowerShell if you did this while you had a session open.)

Once you activate your virtual environment, you can invoke Python scripts like you normally would. For example, if you've written a script called `fetch_data.py`, opening PowerShell, activating your virtual environment, and running the script might look like this:

```PowerShell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\bobby.mcferrin> Sandbox
(sandbox) PS C:\Users\bobby.mcferrin> py fetch_data.py
```

## Virtual Environments on Linux / Mac
To create an alias to activate a virtual environment on a Linux / Max, we'll need to edit your `.bashrc` file. You can find it in your home folder as a hidden file, and you can edit it with a text editor of your choice. You can also edit it from the terminal directly:

```Bash
nano ~/.bashrc
```

Then you can enter a comment (line starts with a `#`) so that future-you knows what the line of code does, followed by the actual code on the next line. Remember that the path text is case-sensitive.

```Bash
# Alias that activates Sandbox virtual environment
alias Sandbox="source ~/path/to/sandbox-7sSAdbXr/bin/activate"
```

Now, all your **future** terminal sessions should allow you to use your alias to activate the virtual environment that you specified. So, you'll need to start a new terminal session to use the alias that you created.
