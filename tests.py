#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Tento jednoduchý testovací skript předpokládá, že je uložen v rootu adresáře a odtud také volán pomocí "python3 malecka1.py", kde malecka1 je můj login na ČVUT. Tento skript nic nekontroluje, předpokládá nově rozbalenou složku semestrální práce a testovací data uložená v adresáři "data". Testy a jejich výstupy budou pro přehlednost uloženy do souboru "output.txt". """

import datetime, subprocess

with open("output.txt", mode='w', encoding='utf-8') as out:
    out.write("Výstup provedených testů (" + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "):\n")
    i = 1
    u = True

    # (1) testy parametru a jejich hodnot, predevsim nevalidni vstupy -> ukazka meznich hodnot
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-n", "malecka1.py", "-X", "auto"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data1/data", "-t", "%y/%m/%d", "-X", "-e", "9"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data1/data", "-t", "%y/%m/%d", "-e", "9", "-e", "1"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d/%Y"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d/%S"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 1:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-X", "min"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-y", "40", "-n", "SKJ", "-x", "40"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-Y", "400", "-y", "40", "-n", "SKJ", "-x", "40/09/09", "-e", "animace"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-Y", "420", "-y", "40", "-n", "SKJ", "-x", "40/09/e9"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")    
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-Y", "140", "-y", "40", "-n", "SKJ", "-x", "40/09/09", "-l", "666", "-c", "y=90:x=80/08/10", "-c", "x=70/01/01:x=04/02/29:x=05/02/29"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")    
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-f", "neexistuje", "-Y", "240", "-y", "40", "-n", "SKJ", "-x", "40/09/09"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "[::]", "-f", "neexistuje", "-Y", "240", "-y", "40", "-n", "SKJ", "-x", "40/09/09"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-Y", "240", "-y", "40", "-n", "SKJ", "-x", "40/09/09", "-X", "40/09/01"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "-t", "%y/%m/%d", "-Y", "240", "-y", "40", "-n", "SKJ", "-g", "grid xtics", "-g", "no parameter for Gnuplot"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 4:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/data1", "data/zz", "-t", "%y/%m/%d", "-Y", "240", "-y", "40", "-n", "SKJ", "-g", "grid xtics", "-g", "no label"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 1:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i)) # spatna kombinace S F T
    args = ["python3", "malecka1.py", "data/data1", "-f", "data/config3", "-F", "24", "-S", "6", "-T", "1"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 4:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i)) # posledni vyskyt v config souboru + spravna kombinace S F T
    args = ["python3", "malecka1.py", "data/data1", "-f", "data/config3", "-F", "24", "-S", "1", "-T", "1"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i)) # chybna direktiva v config souboru
    args = ["python3", "malecka1.py", "data/data1", "-f", "data/config2"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i)) # staci spatna hodnota v config souboru ikdyz preferovana na radce -> error
    args = ["python3", "malecka1.py", "data/data1", "-f", "data/config1", "-F", "79"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 2:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1

    # (2) testy vstupnich souboru (lokalne ulozene), predevsim velke validni vstupy -> dobre ukazky vystupu
    out.write("\nTest {0} (vyžaduje připojení k Internetu): ".format(i)) # vic hodnot pro stejne x
    args = ["python3", "malecka1.py", "http://goo.gl/sqOCK", "-t", "%H:%M:%S", "-g", "style line 1 lt 4 lc rgb \'red\' lw 3", "-g", "style line 2 lt 5 lc rgb \'yellow\' lw 5"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 1:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0} (vyžaduje připojení k Internetu): ".format(i)) # real sin day
    args = ["python3", "malecka1.py", "https://pastebin.com/raw.php?i=4h14Kbt0", "-S", "15", "-T", "30", "-e", "1000", "-t", "[%Y/%m/%d %H:%M:%S]", "-g", "style line 1 lt 4 lc rgb \'red\' lw 3", "-g", "style line 1 lt 10 lc rgb \'yellow\' lw 5", "-X", "[2009/05/12 22:30:00]", "-y", "-2", "-Y", "1.5", "-c", "y=0.8:y=0.4:y=0"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0} (vyžaduje připojení k Internetu): ".format(i)) # real + int sin day
    args = ["python3", "malecka1.py", "https://pastebin.com/raw.php?i=4h14Kbt0", "http://pastebin.com/raw.php?i=vQu8cpJ6", "-S", "40", "-T", "20", "-e", "200", "-t", "[%Y/%m/%d %H:%M:%S]", "-g", "style line 1 lt 4 lc rgb \'red\' lw 3", "-g", "style line 2 lt 5 lc rgb \'blue\' lw 2", "-X", "auto", "-c", "x=[2009/05/12 00:00:00]", "-g", "xlabel \'Python jede\'"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0} (vyžaduje připojení k Internetu): ".format(i)) # invalid url
    args = ["python3", "malecka1.py", "http://pastebin.com/raw.php?i=4h14Kbt0", "http://pastebin.com/raw.php?i=vQu8000000", "-S", "50", "-T", "30", "-e", "250", "-t", "[%Y/%m/%d %H:%M:%S]", "-g", "style line 1 lt 4 lc rgb \'red\' lw 3", "-g", "style line 2 lt 5 lc rgb \'yellow\' lw 5"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 1:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0} (vyžaduje připojení k Internetu): ".format(i)) # week real without anim
    args = ["python3", "malecka1.py", "http://pastebin.com/raw.php?i=CJbStLQg", "-F", "55", "-T", "5", "-t", "[%Y/%m/%d %H:%M:%S]", "-g", "style line 1 lt 9 lc rgb \'blue\' lw 2", "-g", "style line 2 lt 7", "-c", "y=-0.6"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0} (vyžaduje připojení k Internetu): ".format(i)) # week part
    args = ["python3", "malecka1.py", "http://pastebin.com/raw.php?i=0H8V8Ykd", "-S", "1", "-F", "28", "-e", "250", "-t", "[%Y/%m/%d %H:%M:%S]", "-g", "grid xtics ytics", "-g", "style line 2 lt 5 lc rgb \'yellow\' lw 5"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0} (vyžaduje připojení k Internetu): ".format(i)) # 3 soubory
    args = ["python3", "malecka1.py", "http://pastebin.com/raw.php?i=xVXCKjef", "http://pastebin.com/raw.php?i=5G00Nsw1", "http://pastebin.com/raw.php?i=f5kCxW4q", "-F", "25", "-e", "100", "-t", "[%Y/%m/%d %H:%M:%S]", "-g", "ylabel \'Values\'"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/1501rows.data", "-F", "25", "-e", "100", "-t", "[%Y/%m/%d %H:%M:%S]", "-y", "-10.0", "-Y", "auto"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/emptyFile", "-y", "auto"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 1:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/incorrectYValues.data", "-F", "250", "-e", "10000", "-t", "[%Y/%m/%d %H:%M:%S]"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 1:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/specialFormat.data", "-f", "data/config4"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/bad_order_sdi_1_4.data", "data/bad_order_sdi_2_1.data", "data/bad_order_sdi_3_2.data", "data/bad_order_sdi_4_3.data", "-f", "data/config5", "-t", "[%Y/%m/%d %H:%M:%S]"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    out.write("\nTest {0}: ".format(i))
    args = ["python3", "malecka1.py", "data/big.data", "-f", "data/config6"]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        out.write("OK\n")
    else:
        u = False
        out.write("failed\n")
    out.write(" ".join(p.args) + "\n")
    out.write(error.decode('utf-8'))
    i+=1
    # konec testu
    if u:
        out.write("\nVšechny testy probehly úspěšně!")
    else:
        out.write("\nNěkteré testy se nezdařily.")
