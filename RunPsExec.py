import subprocess
import csv
import sys

command = sys.argv[1]

try:
    arg = sys.argv[2]
except:
    arg = ''

try:
    debug = sys.argv[3]
except:
    debug = 'no'

if debug == 'debug':
    with open('stores.txt') as f:
        stores = csv.reader(f, skipinitialspace=True)

        for store in stores:
            print(store[0])

            result = subprocess.Popen('PsExec.exe \\\\' + store[0] + ' -u ' + store[1] + ' -p ' + store[2] + ' "c:\\rpsupport\\PrismCentralManager\\' + command + '" ' + arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = result.communicate()
            errcode = result.returncode
            print(out)
            print(err)
            print(errcode)

        #PsExec.exe \\zc-mysql4-1 -u sysadmin -p sysadmin "c:\rpsupport\PrismCentralManager\sftp"

if debug == 'no':
    with open('stores.txt') as f:
        stores = csv.reader(f, skipinitialspace=True)

        for store in stores:
            print(store[0])

            subprocess.Popen('PsExec.exe \\\\' + store[0] + ' -u ' + store[1] + ' -p ' + store[2] + ' "c:\\rpsupport\\PrismCentralManager\\' + command + '" ' + arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #out, err = result.communicate()
            #errcode = result.returncode
            #print(out)
            #print(err)
            #print(errcode)
