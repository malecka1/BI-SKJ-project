#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Program implements BI-SKJ LS2014/2015 semestral project. For more info read "README.txt" file. '''

__author__ = "Kamil Maleček"
__license__ = "MIT"
__version__ = "1.0"

import argparse, os, re, itertools, sys, signal, shutil, tempfile, urllib.request, subprocess, math

g_dirName = None # output directory, global because of cleanup
g_FinalInputFiles = None # prepared files for Gnuplot, global because of cleanup

class CGraph:
    ''' CGraph class represents data for graph. '''
    def __init__(self, TimeFormat, Xmax, Xmin, Ymax, Ymin, Speed, Time, FPS, CriticalValue, Legend, GnuplotParams, EffectParams, Name, InputFiles):
        ''' Constructor of the CGraph class. '''
        self.m_TimeFormat = TimeFormat
        self.m_Xmax = Xmax
        self.m_Xmin = Xmin
        self.m_Ymax = Ymax
        self.m_Ymin = Ymin
        self.m_Speed = Speed
        self.m_Time = Time
        self.m_FPS = FPS
        self.m_CriticalValue = CriticalValue
        self.m_Legend = Legend
        self.m_GnuplotParams = GnuplotParams
        self.m_EffectParams = EffectParams
        self.m_Name = Name
        self.m_InputFiles = InputFiles
    def printInstance(self):
        ''' Prints CGraph instance for debug purpose. '''
        print("----------- After input -----------") # stderr: file=sys.stderr
        print("TF: {0}\nXmax:Xmin: {1}:{2}\nYmax:Ymin {3}:{4}\nSPEED: {5}\nTime: {6} \nFPS: {7}\nCriticalValue: {8}\nLegend: {9}\nGnuplotP: {10}\nEffectP: {11}\nName: {12}\nInput Files: {13}\n-----------------------------------".format(self.m_TimeFormat, self.m_Xmax, self.m_Xmin, self.m_Ymax, self.m_Ymin, self.m_Speed, self.m_Time, self.m_FPS, self.m_CriticalValue, self.m_Legend, self.m_GnuplotParams, self.m_EffectParams, self.m_Name, self.m_InputFiles))

class UniqueStore(argparse.Action):
    ''' Class for multiple argument occurences error for argparse, source: 'http://stackoverflow.com/a/23032953'. '''
    def __call__(self, parser, namespace, values, option_string):
        if getattr(namespace, self.dest, self.default) is not None:
            parser.error(option_string + " appears several times")
        setattr(namespace, self.dest, values)

def cleanup():
    ''' Function deletes output folder with all files. '''
    shutil.rmtree(g_dirName, ignore_errors=True)
    if g_FinalInputFiles:
        for f in g_FinalInputFiles:
            os.remove(f)

def signalHandler(signum, frame):
    ''' Function catches signals and delete all files. Exit code '3' means signal received.'''
    cleanup()
    print("Recieved signal: {0}, cleaned up.".format(signum), file=sys.stderr)
    sys.exit(3) # return code 3 = signal

def isValid3c(parser, x):
    ''' Function checks timestamp format (implemented %[YymdHMS]). '''
    impl = "YymdHMS" # implemented symbols
    occ = [None]*7  # idicates multiple occurence of symbols
    pos = x.find('%', 0) # finds first %
    if pos != -1:
        i = 0
        while pos != -1:
            if pos+1 == len(x): # last char is %
                parser.error("argument -t: invalid value: \"{0}\"".format(x[pos:]))
            if x[pos+1] == impl[0]:
                if occ[0] != None:
                    parser.error("argument -t: multiple \'%Y\' occurence")
                else:
                    if occ[1] != None:
                        parser.error("argument -t: used \'%Y\' and \'%y\', use just one year specification")
                    occ[0] = 1
            elif x[pos+1] == impl[1]:
                if occ[1] != None:
                    parser.error("argument -t: multiple \'%y\' occurence")
                else:
                    if occ[0] != None:
                        parser.error("argument -t: used \'%Y\' and \'%y\', use just one year specification")
                    occ[1] = 1
            elif x[pos+1] == impl[2]:
                if occ[2] != None:
                    parser.error("argument -t: multiple \'%m\' occurence")
                else:
                    occ[2] = 1
            elif x[pos+1] == impl[3]:
                if occ[3] != None:
                    parser.error("argument -t: multiple \'%d\' occurence")
                else:
                    occ[3] = 1
            elif x[pos+1] == impl[4]:
                if occ[4] != None:
                    parser.error("argument -t: multiple \'%H\' occurence")
                else:
                    occ[4] = 1
            elif x[pos+1] == impl[5]:
                if occ[5] != None:
                    parser.error("argument -t: multiple \'%M\' occurence")
                else:
                    occ[5] = 1
            elif x[pos+1] == impl[6]:
                if occ[6] != None:
                    parser.error("argument -t: multiple \'%S\' occurence")
                else:
                    occ[6] = 1
            else:
                parser.error("argument -t: unsupported value: \"{0}\"".format('%'+x[pos+1]))
            i = pos + 2
            pos = x.find('%', i)
    else: # has to be at least one %x
        parser.error("argument -t: invalid value: \"{0}\"".format(x))
    return x

def isValidMinMax(parser, x, arg):
    ''' Function validates X and Y min/max values. '''
    if x == "auto":
        return x
    elif (arg == '-X' or arg == '-Y') and x == "max": # args with max
        return x
    elif (arg == '-x' or arg == '-y') and x == "min":
        return x
    elif arg == '-Y' or arg == '-y': # y values are always float
        try:
            return float(x) # check float
        except ValueError: # err mesg
            if arg == '-X' or arg == '-Y':
                parser.error("argument {0}: invalid choice: {1} (choose from \"auto\", \"max\", int/float)".format(arg,x))
            else:
                parser.error("argument {0}: invalid choice: {1} (choose from \"auto\", \"min\", int/float)".format(arg,x))
    else: # x values are not checked in the moment
        return x

def isValidSTP(parser, x, arg):
    ''' Function validates Speed, Time and FPS values. '''
    try:
        if float(x) <= 0:
            parser.error("argument {0}: negative or zero value: \'{1}\'".format(arg, x))
    except ValueError:
        parser.error("argument {0}: invalid value: \'{1}\'".format(arg, x))
    return float(x)

def isValidCrit(parser, x):
    ''' Function checks and parses critical values into list. '''
    i = 0
    y = [] # output list
    pos = x.find('y',0)
    pos2 = x.find('x', 0)
    if (pos2 < pos and pos2 != -1) or pos == -1: # what is first
        pos = pos2
    while pos != -1:
        j = pos+1 # j is start of the next item
        pos = x.find('y',j)
        pos2 = x.find('x',j)
        if (pos2 < pos and pos2 != -1) or pos == -1:
            pos = pos2
        if pos == -1: # last value
            break
        if re.search(r'^y=(-?0|-?[1-9][0-9]*)($|\.\d+$)', x[i:pos-1]) or re.search(r'^x=.*\d+.*$', x[i:pos-1]): # using regex
            y.append(x[i:pos-1])
        else:
            parser.error("argument -c: invalid value: \'{0}\'".format(x[i:pos+2]))
        i = pos
    if re.search(r'^y=(-?0|-?[1-9][0-9]*)($|\.\d+$)', x[i:]) or re.search(r'^x=.*\d+.*$', x[i:]):
        y.append(x[i:])
    else:
        parser.error("argument -c: invalid value: \'{0}\'".format(x[i:]))
    return y

def isValidEffect(parser, x):
    ''' Function validates effect parameter (integer). '''
    try:
        if int(x) < 0:
            parser.error("argument -e: negative value: \'{0}\'".format(x))
    except ValueError:
        parser.error("argument -e: invalid value: \'{0}\', must be an integer".format(x))
    return x

def isValidFile(parser, x):
    ''' Function checks path and readability of the configuration file. '''
    if not os.path.isfile(x):
        parser.error("File \"{0}\" does not exists.".format(x))
    elif not os.access(x, os.R_OK):
        parser.error("File \"{0}\" is not readable.".format(x))
    return x

def isValidNameDir(x):
    ''' Function finds correct name of dir for output. '''
    if os.path.exists(x):
        a = [f for f in os.listdir() if re.search(r'^'+x+r'_[1-9][0-9]*$', f)] # get list of current valid names
        if a:
            m = 0;
            for i in a:
                if int(i[len(x)+1:]) > m: # get int
                    m = int(i[len(x)+1:])
            x = x + '_' + str(m+1)
        else:
            x = x + "_1"
    return x

def parseFile(parser, args):
    ''' Function gets arguments from the configuration file (lower priority than cmd line args). '''
    val = [None]*11 # indicate arg in cmd line
    with open(args.f, mode='r', encoding='utf-8') as f: # properly closes file everytime
        l = 0 # nr of line
        for line in f: # iterate through lines
            l+=1
            found = line.find("#") # find first # from the end
            if found != -1: # cut off comment #.....
                line = line[:found]
            if not line.strip(): # ignore whitespace lines
                continue
            line = line.strip() # cut off whitespace inlcuding \n
            found = re.search(r'( |\t)', line) # find first ' ' or \t from left = delimiter
            if not found: # no delimiter between directive and value
                parser.error("config file error: no delimiter between directive and value on line {0}".format(l))
            substr = line[:found.start()] # directive
            substr = substr.lower() # case insensitive
            line = line[found.end():] # rest of the line = directive's value
            line = line.lstrip() # if there is more ' '\t as delimiter
            #print(substr, "|", line, "|") # debug output
            if substr == "timeformat": # validate config file values
                val[0] = isValid3c(parser, line)
            elif substr == "xmax":
                val[1] = isValidMinMax(parser, line, '-X')
            elif substr == "xmin":
                val[2] = isValidMinMax(parser, line, '-x')
            elif substr == "ymax":
                val[3] = isValidMinMax(parser, line, '-Y')
            elif substr == "ymin":
                val[4] = isValidMinMax(parser, line, '-y')
            elif substr == "speed":
                val[5] = isValidSTP(parser, line, '-S')
            elif substr == "time":
                val[6] = isValidSTP(parser, line, '-T')
            elif substr == "fps":
                val[7] = isValidSTP(parser, line, '-F')
            elif substr == "criticalvalue":
                if args.c == None:
                    args.c = []
                args.c.append(isValidCrit(parser, line))
            elif substr == "legend":
                val[8] = line
            elif substr == "gnuplotparams":
                if args.g == None:
                    args.g = []
                args.g.append(line)
            elif substr == "effectparams":
                val[9] = isValidEffect(parser, line)
            elif substr == "name":
                val[10] = isValidNameDir(line)
            else:
                parser.error("config file error: invalid directive on line {0}".format(l))
    if args.t == None: # use values from the file (or None) now if the argument wasn't specified
        args.t = val[0]
    if args.X == None:
        args.X = val[1]
    if args.x == None:
        args.x = val[2]
    if args.Y == None:
        args.Y = val[3]
    if args.y == None:
        args.y = val[4]
    if args.S == None:
        args.S = val[5]
    if args.T == None:
        args.T = val[6]
    if args.F == None:
        args.F = val[7]
    if args.l == None:
        args.l = val[8]
    if args.e == None:
        args.e = val[9]
    if args.n == None:
        args.n = val[10]

def checkX(t, x):
    ''' Function checks if x value has format according to argument t. Returns -1 for error. '''
    d1 = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31) # days
    prestupny = None
    den = None # indicates what has been already checked
    mesic = None
    rok = None
    a = 0 # position in t
    b = 0 # position in x
    #print ("|", t, "|", x, "|") # debug output with format and value to check
    while a < len(t): # go through -t image
        if b >= len(x): # x is shorter than has to be according -t spec
            return -1
        if t[a] == '%':
            try: # check valid value \d
                if t[a+1] != 'Y': # xx (two digits)
                    if b+2 > len(x): # x is shorter than has to be for -ymdHMS
                        return -1
                    if t[a+1] == 'y':
                        rok = int(x[b:b+2])
                    elif t[a+1] == 'H':
                        hod = int(x[b:b+2])
                        if hod < 0 or hod > 24: # according timefmt specs in Gnuplot
                            return -1
                    elif t[a+1] == 'M':
                        minu = int(x[b:b+2])
                        if minu < 0 or minu > 60:
                            return -1
                    elif t[a+1] == 'S':
                        sec = int(x[b:b+2])
                        if sec < 0 or sec > 60:
                            return -1
                    elif t[a+1] == 'm':
                        mon = int(x[b:b+2])
                        if mon < 1 or mon > 12:
                            return -1
                        mesic = mon
                    else: # days according to month and year later
                        day = int(x[b:b+2])
                        if day < 1 or day > 31:
                            return -1
                        den = day
                    b+=2
                else: # -Y -> xxxx (4 digits)
                    if b+4 > len(x): # x is shorter than has to be for -Y
                        return -1
                    rok = int(x[b:b+4])
                    b+=4
                a+=2 # jump over %x in time format (always 2 chars)
                continue
            except ValueError: # not integer
                return -1
        if t[a] is not x[b]: # some other symbol in -t spec
            return -1
        a+=1 # next iteration
        b+=1
    if b != len(x): # x is longer than has to be according t spec
        return -1
    if mesic is not None and den is not None: # it's time to check valid day
        if rok is None and den > d1[mesic-1]: # easiest - without year
            return -1
        else: # with year
            if rok % 4 == 0: # leap year?
                if rok % 100 == 0 and rok % 400 != 0:
                    prestupny = False
                else:
                    prestupny = True
            else:
                prestupny = False
            if not prestupny:
                if mesic == 2 and den > 28: # February in not leap year
                    return -1
                elif den > d1[mesic-1]: # other months
                    return -1
            elif day > d1[mesic-1]: # leap year
                return -1
    #print(prestupny, den, mesic, rok) # debug output

def myCompare(x1, x2, t):
    ''' Compare function for Insertion sort, values stored at [1] index. Returns -1 if x1 is lower than x2, 0 for equal items and otherwise returns 1. '''
    #print(x1, x2, t) # debug output
    if x1 == x2: # same x values
        return 0
    # t is time format, priority: %Y %y %m %d %H %M %S
    pos = t.find('%Y')
    posOfY = None # remmember this position, because it has 2 more chars!
    if pos is not -1:
        posOfY = pos
        sub1 = x1[1][pos:pos+4]
        sub2 = x2[1][pos:pos+4]
        if sub1 < sub2:
            return -1
        elif sub1 > sub2:
            return 1
    pos = t.find('%y') # can't be %Y and %y (handled in isValid3c)
    if pos is not -1:
        sub1 = x1[1][pos:pos+2]
        sub2 = x2[1][pos:pos+2]
        if sub1 < sub2:
            return -1
        elif sub1 > sub2:
            return 1
    pos = t.find('%m') # from now check if %Y was before
    if pos is not -1:
        if posOfY and pos > posOfY: # if %Y was before
            sub1 = x1[1][pos+2:pos+4]
            sub2 = x2[1][pos+2:pos+4]
        else: # if %Y wasn't before or wasn't at all
            sub1 = x1[1][pos:pos+2]
            sub2 = x2[1][pos:pos+2]
        if sub1 < sub2:
            return -1
        elif sub1 > sub2:
            return 1
    pos = t.find('%d')
    if pos is not -1:
        if posOfY and pos > posOfY:
            sub1 = x1[1][pos+2:pos+4]
            sub2 = x2[1][pos+2:pos+4]
        else:
            sub1 = x1[1][pos:pos+2]
            sub2 = x2[1][pos:pos+2]
        if sub1 < sub2:
            return -1
        elif sub1 > sub2:
            return 1
    pos = t.find('%H')
    if pos is not -1:
        if posOfY and pos > posOfY:
            sub1 = x1[1][pos+2:pos+4]
            sub2 = x2[1][pos+2:pos+4]
        else:
            sub1 = x1[1][pos:pos+2]
            sub2 = x2[1][pos:pos+2]
        if sub1 < sub2:
            return -1
        elif sub1 > sub2:
            return 1
    pos = t.find('%M')
    if pos is not -1:
        if posOfY and pos > posOfY:
            sub1 = x1[1][pos+2:pos+4]
            sub2 = x2[1][pos+2:pos+4]
        else:
            sub1 = x1[1][pos:pos+2]
            sub2 = x2[1][pos:pos+2]
        if sub1 < sub2:
            return -1
        elif sub1 > sub2:
            return 1
    pos = t.find('%S')
    if pos is not -1:
        if posOfY and pos > posOfY:
            sub1 = x1[1][pos+2:pos+4]
            sub2 = x2[1][pos+2:pos+4]
        else:
            sub1 = x1[1][pos:pos+2]
            sub2 = x2[1][pos:pos+2]
        if sub1 < sub2:
            return -1
        elif sub1 > sub2:
            return 1
    return 0

def InsSort(lines, t):
    ''' Function implements Insertion sort for list of (originalIndex, timeValue) and returns new index order. '''
    for i in range(1,len(lines)): # take item from the left to the right and find his correct position and swap
        key = lines[i]
        j = i
        tmp = myCompare(lines[j-1], key, t)
        if tmp == 0: # same values
            return None
        while j > 0 and tmp == 1:
            lines[j] = lines[j-1]
            j-=1
            lines[j] = key
            tmp = myCompare(lines[j-1], key, t)
            if tmp == 0:
                return None
    return lines

def formatCrit(parser, args):
    ''' Function checks -c values (especially axe x's) and prepares them. '''
    x = [] # list for x values
    y = [] # list for y values
    for i in itertools.chain.from_iterable(args.c):
        if i[0] == 'y':
            y.append(float(i[2:]))
        else: # x values
            if checkX(args.t, i[2:]) == -1:
                parser.error("argument -c: invalid x format: \"{0}\"".format(i[2:]))
            x.append(i[2:])
    x = list(set(x)) # remove duplicates, random order
    tmpList = []
    for i in range(0, len(x)): # list for x-sort (index, x value)
        tmpList.append((i, x[i]))
    tmpList = InsSort(tmpList, args.t) # insertion sort
    i = 0
    x = []
    while i < len(tmpList): # [i][1] values are sorted original x values
        x.append(tmpList[i][1])
        i+=1
    #print("-c x sorted:", x) # debug output, shows sorted x values
    args.c = (x, sorted(list(set(y)))) # tuple due to guaranteed order (x, y)

def defaultsAndCheck(parser, args):
    ''' Function makes another arguments check and sets default values (after all possible inputs). '''
    if args.t is None:
        args.t = "[%Y-%m-%d %H:%M:%S]"
    if args.X is None:
        args.X = "max"
    if args.x is None:
        args.x = "min"
    if args.X != "max" and args.X != "auto":
        if checkX(args.t, args.X) == -1:
            parser.error("argument -X: invalid Xmax format: \"{0}\"".format(args.X))
    if args.x != "min" and args.x != "auto":
        if checkX(args.t, args.x) == -1:
            parser.error("argument -x: invalid Xmin format: \"{0}\"".format(args.x))
        if args.X != "max" and args.X != "auto":
            a = myCompare((0, args.X), (0, args.x), args.t)
            if a == -1 or a == 0:
                parser.error("value of Xmax is not higher than xmin")
    if args.Y is None:
        args.Y = "auto"
    if args.y is None:
        args.y = "auto"
    if type(args.Y) is float and type(args.y) is float and args.Y <= args.y:
        parser.error("value of Ymax is not higher than ymin")
    if args.c is not None: # check format and organize -c values
        formatCrit(parser, args)
    if args.e is None:
        args.e = 0
    if args.n is None: # set default name
        args.n = isValidNameDir(parser.prog)

def getArgsAndRetInstance():
    ''' Function parses arguments and returns new CGraph instance. Exit code '2' means invalid command line arguments or directives in the configuration file. '''
    parser = argparse.ArgumentParser(description='This script creates animation in Gnuplot according to command-line arguments or configuration file.')
    # command-line params have priority over the configuration file
    parser.add_argument('-t', type=lambda x: isValid3c(parser, x), metavar="%{YymdHMS}", action=UniqueStore, help="timestamp format")
    parser.add_argument('-X', type=lambda x: isValidMinMax(parser, x, '-X'), metavar="{\"auto\",\"max\",int/float}", action=UniqueStore, help="x-max")
    parser.add_argument('-x', type=lambda x: isValidMinMax(parser, x, '-x'), metavar="{\"auto\",\"min\",int/float}", action=UniqueStore, help="x-min")
    parser.add_argument('-Y', type=lambda x: isValidMinMax(parser, x, '-Y'), metavar="{\"auto\",\"max\",int/float}", action=UniqueStore, help="y-max")
    parser.add_argument('-y', type=lambda x: isValidMinMax(parser, x, '-y'), metavar="{\"auto\",\"min\",int/float}", action=UniqueStore, help="y-min")
    parser.add_argument('-S', type=lambda x: isValidSTP(parser, x, '-S'), metavar="int/float", action=UniqueStore, help="speed")
    parser.add_argument('-T', type=lambda x: isValidSTP(parser, x, '-T'), metavar="int/float", action=UniqueStore,  help="time (duration)")
    parser.add_argument('-F', type=lambda x: isValidSTP(parser, x, '-F'), metavar="int/float", action=UniqueStore,help="fps")
    parser.add_argument('-c', type=lambda x: isValidCrit(parser, x), metavar="x/y=int/float", action="append", help="critical values, separate by \':\'")
    parser.add_argument('-l', type=str, metavar="text", action=UniqueStore, help="legend")
    parser.add_argument('-g', metavar="parameter", action="append", help="Gnuplot parameter")
    parser.add_argument('-e', type=lambda x: isValidEffect(parser, x), metavar="int", action=UniqueStore, help="count of animated points")
    parser.add_argument('-f', type=lambda x: isValidFile(parser, x), metavar="pathname", action=UniqueStore, help="config file")
    parser.add_argument('-n', type=lambda x: isValidNameDir(x), metavar="text", action=UniqueStore, help="name")
    parser.add_argument("file", metavar="FILE", nargs='+', help="input file or url")
    args = parser.parse_args() # get values of args
    if args.f is not None: # file - lower priority
        parseFile(parser, args)
    defaultsAndCheck(parser, args) # another input control (except input files) and setting defaults
    y = [] # input file list
    [y.append(x) for x in args.file if not x in y] # remove duplicities from input files list and keep the order!
    args.file = y
    return CGraph(args.t, args.X, args.x, args.Y, args.y, args.S, args.T, args.F, args.c, args.l, args.g, args.e, args.n, args.file)

def prepareInputFiles(self):
    ''' Function downloads (http(s)), checks, organizes input files. Error code '1' means input file error. '''
    global g_FinalInputFiles # global -> local
    g_FinalInputFiles = [] # new list for prepared, sorted input files (= references to temp files)
    xmax = None # get values from files
    xmin = None
    ymax = None
    ymin = None
    for f in self.m_InputFiles:
        if re.search(r'^http(s)?://.*', f) != None: # download file from url
            fpT = tempfile.NamedTemporaryFile() # temporary file with name for download
            try:
                with urllib.request.urlopen(f) as stream: # download file to tmp
                    fpT.write(stream.read())
            except urllib.error.HTTPError as e: # not responding
                print("Input file error: \"{0}\", error code:".format(f), e.code, file=sys.stderr)
                cleanup()
                sys.exit(1) # return code 1 = error with input files
            except urllib.error.URLError as e: # server not available
                print("Input file error: \"{0}\", reason:".format(f), e.reason, file=sys.stderr)
                cleanup()
                sys.exit(1)
            f2 = fpT.name # get name of the local tmp file '/tmp/xxxx'
        else: # local file
            if not os.path.isfile(f):
                print("Input file error: file \"{0}\" does not exist".format(f), file=sys.stderr)
                cleanup()
                sys.exit(1)
            elif not os.access(f, os.R_OK): # readability
                print("Input file error: file \'{0}\" is not readable".format(f), file=sys.stderr)
                cleanup()
                sys.exit(1)
            elif os.stat(f).st_size == 0: # empty file
                print("Input file error: file \"{0}\" is empty".format(f), file=sys.stderr)
                cleanup()
                sys.exit(1)
            f2 = f
        try:
            with open(f2, encoding='utf-8') as soubor:
                i = 0 # nr of line
                forSort = []
                for line in soubor: # check lines' format (1)
                    i+=1
                    line = line.strip() # cut off whitespace including \n
                    found = re.search(r'( |\t)', line[::-1]) # find delimiter in inversed line = last ' '\t is delimiter
                    if not found: # no delimiter = just one column
                        print("Input file error: file \"{0}\", line {1} does not have two columns".format(f, i), file=sys.stderr)
                        cleanup()
                        sys.exit(1)
                    substr = line[:-found.end()] # x value
                    substr = substr.rstrip() # more ' '\t as delimiter
                    line = line[-found.end()+1:] # y value
                    try: # y value has to be int/float
                        if ymin:
                            if float(line) < ymin: # get y max/min
                                ymin = float(line)
                        else:
                            ymin = float(line)
                        if ymax:
                            if float(line) > ymax:
                                ymax = float(line)
                        else:
                            ymax = float(line)
                    except ValueError:
                        print("Input file error: file \"{0}\", line {1}: y value is not int/float".format(f, i), file=sys.stderr)
                        cleanup()
                        sys.exit(1)
                    #print(i, ":", substr, ":", line, ":") # debug output...parsed line of file
                    if checkX(self.m_TimeFormat, substr) == -1: # x value timeformat check
                        print("Input file error: file \"{0}\", line {1}: incorrect format".format(f, i), file=sys.stderr)
                        cleanup()
                        sys.exit(1)
                    forSort.append((i-1, substr)) # (line's index, x value)
                linesPos = InsSort(forSort, self.m_TimeFormat) # insertion sort for lines, return new index order at [i][0] (2)
                if not linesPos: # more values with the same time doesn't make sense -> error
                    print("Input file error: file \"{0}\": same x values in one file does not make sense".format(f), file=sys.stderr)
                    cleanup()
                    sys.exit(1)
                soubor.seek(0) # reset read pointer's position
                lines = soubor.readlines() # read all lines into list
                fp = tempfile.NamedTemporaryFile(delete=False) # final tmp file, default r+w, delete prevention!!
                i = 0
                while i < len(linesPos): # write lines in accordance with the new order (index [linesPos[i][0])
                    line = lines[linesPos[i][0]]
                    line = line.lstrip() # get rid of init spaces (because of Gnuplot)
                    fp.write(line.encode('utf-8')) # important encode!!
                    i+=1
                fp.close() # important
                g_FinalInputFiles.append(fp.name) # remember final input file
                #print("prepared file:", f, "->", fp.name) # debug output ordered files
        except UnicodeDecodeError:
            print("Input file error: cannot decode file (from) \"{0}\"".format(f), file=sys.stderr) # file from url
            cleanup()
            sys.exit(1)
    i = 0 # merge input files in case of continuation (3)
    while i < len(g_FinalInputFiles)-1: # index of file
        with open(g_FinalInputFiles[i], mode='r+', encoding='utf-8') as f: # first file (also final file)
            aline = f.readlines()
            lline = aline[-1].strip() # get last line timestamp
            found = re.search(r'( |\t)', lline[::-1]) # get last x
            lline = lline[:-found.end()]
            with open(g_FinalInputFiles[i+1], encoding='utf-8') as f2:
                fline = f2.readline().strip()
                found = re.search(r'( |\t)', fline[::-1]) # get first x
                fline = fline[:-found.end()]
                if myCompare((0, lline), (0, fline), self.m_TimeFormat) != -1: # no data to move
                    i+=1 # next two files
                    # get x max/min value from aline[0/-1] = final input file
                    fline = aline[0].strip() # first line
                    found = re.search(r'( |\t)', fline[::-1])
                    fline = fline[:-found.end()]
                    lline = aline[-1].strip() # last line
                    found = re.search(r'( |\t)', lline[::-1])
                    lline = lline[:-found.end()]
                    if xmax:
                        if myCompare((0, xmax), (0, lline), self.m_TimeFormat) == -1:
                            xmax = lline
                    else:
                        xmax = lline
                    if xmin:
                        if myCompare((0, xmin), (0, fline), self.m_TimeFormat) == 1:
                            xmin = fline
                    else:
                        xmin = fline
                    continue # next two files
                else: # move data (merge) -> jump to the 2nd file's begin
                    f2.seek(0)
                f.write(f2.read()) # write all data from f2's pointer
        #print("file merge:", g_FinalInputFiles[i+1], "->", g_FinalInputFiles[i]) # debug output
        os.remove(g_FinalInputFiles[i+1]) # remove old file f2
        g_FinalInputFiles.pop(i+1) # remove item from file list
    # x max/min values from the last file
    with open(g_FinalInputFiles[-1], mode='r', encoding='utf-8') as f:                
        aline = f.readlines()
        fline = aline[0].strip() # first line
        found = re.search(r'( |\t)', fline[::-1])
        fline = fline[:-found.end()]
        lline = aline[-1].strip()
        found = re.search(r'( |\t)', lline[::-1])
        lline = lline[:-found.end()]
        if xmax:
            if myCompare((0, xmax), (0, lline), self.m_TimeFormat) == -1:
                xmax = lline
        else:
            xmax = lline
        if xmin:
            if myCompare((0, xmin), (0, fline), self.m_TimeFormat) == 1:
                xmin = fline
        else:
            xmin = fline
    if self.m_Xmax == "max": # save float values
        self.m_Xmax = xmax
    if self.m_Xmin == "min":
        self.m_Xmin = xmin
    if self.m_Ymax == "max":
        self.m_Ymax = ymax
    if self.m_Ymin == "min":
        self.m_Ymin = ymin
    #print("xmax:", self.m_Xmax, "xmin:", self.m_Xmin, "ymax:", self.m_Ymax, "ymin:", self.m_Ymin) # debug output

def createAnim(self):
    ''' Function creates final output. Error code '4' means Gnuplot error. '''
    # X/Y max/min, length of animation, legend are already known
    lines = 0 # sum of all lines
    linesN = [] # list of sums per files
    for f in g_FinalInputFiles:
        with open(f, mode='r', encoding='utf-8') as file:
            linesN.append(sum(1 for line in file))
            lines+=linesN[-1]
    nrY = self.m_TimeFormat.count(' ') + 2 # nr of y column is at least '2'
    # Time, Speed, FPS -> delay (1/100 s), speed (ceil), number of gif frames
    framesNr = 0
    delay = 0
    if self.m_Speed and self.m_Speed > lines:
        framesNr = 1
        delay = 0
    elif self.m_Time: # comb of all params goes here, Time
        if self.m_FPS: # ceil + high FPS + not many lines -> not simple solution, Barinka said that ceil is enought
            framesNr = math.ceil(self.m_Time * self.m_FPS)
            if self.m_Speed and math.ceil(lines/framesNr) != int(self.m_Speed):
                print("Gnuplot error: invalid combination of all Speed, FPS and Time arguments", file=sys.stderr)
                cleanup()
                sys.exit(4)
            self.m_Speed = math.ceil(lines / framesNr)
            delay = math.ceil(self.m_Time * 100 / (framesNr-1))
        else: # Time + speed
            if not self.m_Speed:
                self.m_Speed = 1
            self.m_Speed = math.ceil(self.m_Speed)
            framesNr = math.ceil(lines / self.m_Speed)
            delay = math.ceil(self.m_Time * 100 / (framesNr-1))
    elif self.m_Speed: # Speed
        self.m_Speed = math.ceil(self.m_Speed)
        if not self.m_FPS:
            self.m_FPS = 25
        framesNr = math.ceil(lines / self.m_Speed)
        delay = math.ceil(framesNr * 100 / self.m_FPS / (framesNr-1))
    elif self.m_FPS: # FPS
        self.m_Speed = 1
        framesNr = lines
        delay = math.ceil(framesNr * 100 / self.m_FPS / (framesNr-1))
    else: # 3x None -> defaults: Speed + FPS
        self.m_Speed = 1
        framesNr = lines
        delay = math.ceil(framesNr * 100 / 25 / (framesNr-1))
    gfile = tempfile.NamedTemporaryFile() # file for Gnuplot, temp -> removes itself
    #print("Gnuplot file:", gfile.name, "\nframes:", framesNr, "delay:", delay, "speed:", self.m_Speed) # debug output
    with open(gfile.name, mode='w', encoding='utf-8') as f:
        f.write("reset\nset timefmt \""+str(self.m_TimeFormat)+"\"\nset xdata time\nframes="+str(framesNr)+"\nj="+str(self.m_Speed)+" # = speed\ni=1\n") # common settings
        if self.m_GnuplotParams: # Gnuplot params
            for param in self.m_GnuplotParams:
                f.write("set " + str(param) + '\n')
        if self.m_Legend: # legend = graph title
            f.write("set title \"" + str(self.m_Legend) + "\"\n")
        if self.m_Xmax == "auto": # x autoscale
            f.write("set xrange [:*]\n") # autoscale xmax
        else: # custom xmax xrange
            f.write("set xrange [:\"" + str(self.m_Xmax) + "\"]\n")
        if self.m_Xmin == "auto":
            f.write("set xrange [*:]\n")
        else:
            f.write("set xrange [\"" + str(self.m_Xmin) + "\":]\n")
        if self.m_Ymax == "auto": # y autoscale
            f.write("set yrange [:*]\n")
        else: # custom ymax yrange
            f.write("set yrange [:\"" + str(self.m_Ymax) + "\"]\n")
        if self.m_Ymin == "auto":
            f.write("set yrange [*:]\n")
        else:
            f.write("set yrange [\"" + str(self.m_Ymin) + "\":]\n")
        f.write("set terminal unknown # disable showing upcomming test-plot\nplot")
        s = 0
        for i in g_FinalInputFiles: # test plot to unknown output, then set correct output term & dir
            f.write(" '"+str(i)+"' using 1:($0+"+str(s)+" < j ? $"+str(nrY)+" : 1/0) notitle,")
            s+=linesN[g_FinalInputFiles.index(i)]
        f.write("\ntmpY=GPVAL_Y_MIN # plot first line and get Ymin for first frame\ntmpS=GPVAL_DATA_X_MIN # start for -c lines at axe x\nset term gif animate delay "+str(delay)+"\nset output \""+str(self.m_Name)+"/animation.gif\"\nwhile (i < frames) {\n")
        if self.m_CriticalValue: # -c as arrows before plot command
            l=1
            for xc in self.m_CriticalValue[0]: # x critical values
                f.write("set arrow "+str(l)+" from \""+str(xc)+"\",GPVAL_Y_MIN to \""+str(xc)+"\",GPVAL_Y_MAX nohead lw 1 lc rgb 'gold'\n")
                l+=1
            for yc in self.m_CriticalValue[1]: # y critical values
                f.write("set arrow "+str(l)+" from tmpS,"+str(yc)+" to GPVAL_X_MAX,"+str(yc)+" nohead lw 1 lc rgb 'skyblue'\n")
                l+=1
        f.write("plot") # just one plot command
        s = 0 # sum of lines of all previous files
        k = 1 # linestyle number for -g params like "style line 1 lt 2 lc rgb \"red\" lw 3"
        for i in g_FinalInputFiles: # two graphs per file, second is animation, using GPVAL_Y_MIN variable to get current ymin for correct animation steps
            f.write(" '"+str(i)+"' using 1:($0+"+str(s)+" < j ? $"+str(nrY)+" : 1/0) notitle linestyle "+str(k)+", '"+str(i)+"' using 1:($0+"+str(s)+" >= j && $0+"+str(s)+" < j+"+str(self.m_EffectParams)+" ? (($"+str(nrY)+"-tmpY)*(1-1.0/"+str(self.m_EffectParams)+"*($0+"+str(s)+"+1-j))+tmpY) : 1/0) notitle linestyle "+str(k)+",")
            s+=linesN[g_FinalInputFiles.index(i)]
            k+=1
        f.write("\nif (GPVAL_Y_MIN < tmpY) { # for valid animation lowest value\ntmpY=GPVAL_Y_MIN\n}\ni=i+1\nj=j+"+str(self.m_Speed)+"\n}\n") # for next iteration
        if self.m_CriticalValue: # -c before final frame
            l=1
            for xc in self.m_CriticalValue[0]: # x critical values
                f.write("set arrow "+str(l)+" from \""+str(xc)+"\",GPVAL_Y_MIN to \""+str(xc)+"\",GPVAL_Y_MAX nohead lw 1 lc rgb 'gold'\n")
                l+=1
            for yc in self.m_CriticalValue[1]: # y critical values
                f.write("set arrow "+str(l)+" from tmpS,"+str(yc)+" to GPVAL_X_MAX,"+str(yc)+" nohead lw 1 lc rgb 'skyblue'\n")
                l+=1
        f.write("plot")
        k = 1 # linestyle number for -g params like "style line 1 lt 2 lc rgb \"red\" lw 3"
        for i in g_FinalInputFiles: # final frame
            f.write(" '"+str(i)+"' using 1:"+str(nrY)+" notitle linestyle "+str(k)+", sqrt(-1) notitle,") # pair with empty graph to get correct color
            k+=1
        f.write("\nset output\n") # closes gnuplot file
    #while input("------------- Quit ----------------\nGnuplot and input files accessible, press \'q\' to quit: ") != 'q': # debug output - all input files
    #    pass
    try: # execute gnuplot and create animation
        p = subprocess.Popen(["gnuplot", gfile.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError: # can't find Gnuplot
        print("Gnuplot error: cannot execute Gnuplot", file=sys.stderr)
        cleanup()
        sys.exit(4) # err code 4 = Gnuplot error
    output, error = p.communicate() # at the end calls wait(), DO NOT DELETE
    #print("----------- Gnuplot ---------------\nreturn code:", p.returncode, "\nstdout:", output, "\nstderr:", error) # debug output of Gnuplot
    if p.returncode != 0: # gnuplot wasn't successful
        print("Gnuplot error:", error.decode('utf-8'), end='', file=sys.stderr)
        cleanup()
        sys.exit(4)

def main():
    ''' Main function of the script. '''
    signal.signal(signal.SIGINT, signalHandler) # ctrl+c
    signal.signal(signal.SIGTERM, signalHandler) # kill PID
    g = getArgsAndRetInstance() # get valid instance
    #g.printInstance() # debug output after input
    os.makedirs(g.m_Name) # create output dir, from now use cleanup() in case of error
    global g_dirName # use global variable as local
    g_dirName = g.m_Name
    CGraph.prepareInputFiles = prepareInputFiles
    g.prepareInputFiles() # check and prepare input files
    CGraph.createAnim = createAnim
    g.createAnim() # finally create animation
    for f in g_FinalInputFiles: # delete tmp input files!
        os.remove(f)

if __name__ == "__main__": # call main
    main()
