"""
    FileDigger
    A script to find all files with a specified extensions saved in a user's account.
    Results are outputted into results directory.
    This script was build on top of ImageFinder (https://github.com/acintr/ImageFinder)
"""
import os
import webbrowser
import sys

file_list = []      # List of paths of files that match the extension specified by user.
ext = ''            # Current target extension.

def find(ff_dir):
    """
    Search for files recursively
    :param ff_dir: str - Current directory
    :return: none
    """
    if not os.path.isdir(ff_dir):   # Check parameter if parameter is a directory
        return
    else:
        files = os.listdir(ff_dir) # List of contents in current directory
        if len(files) != 0:
            for f in files:
                if f.endswith(ext):
                    file_list.append(ff_dir + '/' + f)
            for f in files:
                find(ff_dir + '/' + f)     # Recursion
        return

# Validating arguments
if len(sys.argv)<=1:
    usr_in = input('No extensions specified in arguments.\
    \nPlease specify extensions you wish to look for separated by SPACE:\n')
    args = usr_in.split(' ')
else:
    args = sys.argv[1:]

try:
    user = os.getlogin()                # Get the user currently logged in the computer
    loc = os.getcwd()                   # Get the current working directory
    f_dir = (loc.split(user))[0]+user   # Generate the user directory (will be used as the starting directory)
    # f_dir = '/'

    for arg in args:
        # Extension validation
        if ('.' in arg and not arg.startswith('.')) or arg.count('.')>1:
            print(arg,'is an invalid extension.')
            continue
        elif '.' not in arg:
            ext = '.'+arg
        else:
            ext = arg

        # Begin search
        find(f_dir)

        print('\nFound ', len(file_list), 'files with', ext, 'extension.')
        if len(file_list) > 0:
            # Write results in output files .results
            if not os.path.exists('results'):
                os.mkdir('results')
            out_loc = 'results/'+ext.replace('.', '')+'_files.results'
            results = open(out_loc, 'w')
            for f in file_list:
                results.write(f+'\n')
            results.close()
            print('Results saved in',os.getcwd()+'/'+out_loc)
        file_list.clear()

except:
    err = sys.exc_info()[0]
    print('An error has occurred:', err)
