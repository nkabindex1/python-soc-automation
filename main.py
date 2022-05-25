# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pip

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    stop=False
    while(not stop):
        try: # test if pandas can be imported
            import pandas as pd
            stop=True
        except:
            pip.main(["install", "--user", "--trusted-host", "pypi.org", "--trusted-host", "pypi.python.org", "--trusted-host",
                      "files.pythonhosted.org", "pandas==1.4.2"])


    
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Xolani')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
