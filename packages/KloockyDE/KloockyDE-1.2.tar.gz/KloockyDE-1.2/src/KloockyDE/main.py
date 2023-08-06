from KloockyDE.decode_ASCII import *
from KloockyDE.binarysearch import *
from KloockyDE.linearsearch import *
from KloockyDE.min_max_search import *
from KloockyDE.bubblesort import *
from KloockyDE.heapsort import *
from KloockyDE.max_min_sort import *
from KloockyDE.quicksort import *
from infinity import Infinity
import time
import sys
import os
import math


alphabet = "abcdefghijklmnopqrstuvwxyz"
ziffern = "0123456789"
sonderzeichen = " ,;.:-_#'+*~@€<>|^°" + '"§$%&/=?`´(){}[]'
escape_chars = "\\\n\t"
ascii_128 = ' !"#$%&' + "'()*+,-./" + ziffern + ":;<=>?@" + alphabet.upper() + "[\\]^_`" + alphabet + "{|}~"
ascii_128_alle = ['NUL', 'SOH', 'STX', 'ETX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'TAB', 'LF', 'VT', 'FF', 'CR', 'SO', 'SI', 'DLE', 'DC1', 'DC2', 'DC3', 'DC4', 'NAK', 'SYN', 'ETB', 'CAN', 'EM', 'SUB', 'ESC', 'FS', 'GS', 'RS', 'US']
ascii_128_alle = ascii_128_alle + list(ascii_128) + ["DEL"]


def calc_time(before, now, decimals=0):
    '''
    Calculate the time between before and now in seconds
        before and now are ints gathered by time.perf_counter_ns()
    :param before: int
    :param now: int
    :param decimals: int    : How many decimals do you want?
        default:    0
    :return: int or float
    '''
    if decimals <= 0:
        return int((now - before) / (10 ** 9))
    else:
        x = str((now - before) / (10 ** 9)).split(".")
        x = [int(x[0]), int(x[1][:decimals])]
        x = x[0] + (x[1] * (10 ** -decimals))
        return x


def t_print(before, now, decimals=0):
    '''
    Calculate the time between before and now in seconds
        before and now are ints gathered by time.perf_counter_ns()
        prints that time
    :param before: int
    :param now: int
    :param decimals: int    : How many decimals do you want?
        default:    0
    :return: int or float
    '''
    x = calc_time(before, now, decimals)
    print("Dauer:", x, "Sekunden")
    return x


def filename_increment(path_p):
    '''
    Takes file-path 'path_p' and returns next possible filename in its directory
        if path_p does not exist:   return path_p
        else:
            count upwards from 2 and try 'path_p w/o ending'_'number'.'ending' until file does not exist
            return that
    :param path_p: str  : path of file you want to increment
    :return: str : incremented filepath
    '''
    path = path_p[:-len("." + path_p.split(".")[-1])]
    ending = "." + path_p.split(".")[-1]
    f = lambda x: path + "_" + str(x) + ending
    try:
        file = open(path_p, "r")
        file.close()
        check = True
        i = 2
        while check:
            try:
                file = open(f(i), "r")
                file.close()
                i += 1
            except FileNotFoundError:
                return f(i)
    except FileNotFoundError:
        return path_p


def fi(path):
    '''
    Same as filename_increment but shorter name
    :param path: str  : path of file you want to increment
    :return: str : incremented filepath
    '''
    return filename_increment(path)


def fac(n):
    '''
    Calculates faculty of n with recursion
    :param n: int
    :return: int : faculty of n
    '''
    if n == 0:
        return 1
    elif n == 1:
        return n
    else:
        return n * fac(n - 1)


def timestamp():
    '''
    Returns timestamp of current time in this Syntax:
        dd-mm-yyyy_hh-mm-ss
        ~> day-month-year_hour-minute-second
    Good for filenaming
    :return: str    : as above
    '''
    x_ = time.localtime()[:6]
    x = [2, 1, 0, 3, 4, 5]
    ans = ''
    for i in range(6):
        tmp = str(x_[x[i]])
        if len(tmp) == 0:
            tmp = '00'
        elif len(tmp) == 1:
            tmp = '0' + tmp
        ans = ans + tmp
        if not (i+1) % 3 == 0:
            ans = ans + '-'
        elif i == 2:
            ans = ans + '_'
    return ans


def backup(path_dir, path_backup_dir, ausnahmen=[], backup_backups=False, only_txt=True, offset=True, sort=False):
    '''
    backs up files into a file named backup_(timestamp).txt
    :param path_dir:            str:    path of the directory of the files to backup
    :param path_backup_dir:     str:    path where the backup should appear
    :param ausnahmen:           list:   list of names of files, which should not be backed up (strings)
    :param backup_backups:      bool:   False:  backup files will not be backed up
    :param only_txt:            bool:   True:   Only '.txt' files will be backed up
    :param offset:              bool:   True:   an '\t' char will be added to each line of every file
    :param sort:                bool:   True:   List of files gets sorted. Made for sorting ITS/notizen
    :return:                    str:    path to backup file
    '''
    def sorter(l):
        index = {}
        for i in range(len(l)):
            index[int(l[i].split(' ')[1])] = l[i]
        values = quicksort_list_asc(list(index.keys()))
        for i in range(len(values)):
            values[i] = index[values[i]]
        return values
    filenames = [f for f in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))]
    remove = []
    for i in range(len(filenames)):
        if only_txt and not filenames[i][-4:] == '.txt':
            remove.append(i)
        elif not backup_backups and not filenames[i].find('backup') == -1:
            remove.append(i)
        elif filenames[i] in ausnahmen:
            remove.append(i)
    remove.reverse()
    for i in range(len(remove)):
        filenames.pop(remove[i])
    if sort:
        filenames = sorter(filenames)
    backup_name = path_backup_dir + '/backup_' + timestamp() + '.txt'
    backup_file = open(backup_name, 'w')
    for i in range(len(filenames)):
        backup_file.write('-----' + filenames[i] + '-----\n')
        file = open(path_dir + '/' + filenames[i], 'r')
        for line in file:
            if offset:
                backup_file.write('\t')
            backup_file.write(str(line))
        backup_file.write('\n')
        file.close()
    backup_file.close()
    print('BACKUP SUCCESSFUL RETURNING PATH TO BACKUP FILE')
    return backup_name


def log_line(type_p='INFO', message='DEFAULT LOG LINE'):
    '''
    Returns a line that is good for log-files
        date time type message
    :param type_p:  str :   What type of message? i.e. INFO, ERROR, ...
    :param message: str :   The message
    :return:    str :   line for log-file
    '''
    ans = timestamp().split('_')
    ans[1] = ans[1].replace('-', ':')
    return ans[0] + ' ' + ans[1] + '\t' + type_p + '\t' + message + '\n'


class Inf(Infinity, int):
    '''
    Objects of this class can be in calculations with int and act like infinity
    '''
    pass
