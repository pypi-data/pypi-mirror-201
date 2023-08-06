"""
pretty print
"""

from termcolor import colored

def print_message(message, type):
    if type == 'SUCCESS':
        print('[' + colored('SUCCESS', 'green') +  '] ' + message)
    elif type == 'INFO':
        print('[' + colored('INFO', 'blue') +  '] ' + message)
    elif type == 'WARNING':
        print('[' + colored('WARNING', 'yellow') +  '] ' + message)
    elif type == 'ALERT':
        print('[' + colored('ALERT', 'yellow') +  '] ' + message)
    elif type == 'ERROR':
        print('[' + colored('ERROR', 'red') +  '] ' + message)
