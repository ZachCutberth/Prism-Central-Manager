# Count or delete pcp_promotion records
# By Zach Cutberth

from subprocess import Popen, PIPE
import winreg
import os
import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return str(len(str_list)+1)

def resource_path(relative_path):
    try: 
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_mysql_path():
    try:
        prism_regkeys = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                "SOFTWARE\\WOW6432Node\\Retail Pro\\Prism\\Primary")
        mysql_path = winreg.QueryValueEx(prism_regkeys, "DBInstallPath")
        winreg.CloseKey(prism_regkeys)
        return mysql_path
    except:
        pass

def promo_count():
    sql = 'select count(*) from rpsods.pcp_promotion;'
    mysql_path = get_mysql_path()
    sql_file = open('query.sql', 'w')
    sql_file.write(sql)
    sql_file.close()
    path = os.getcwd()
    mysql_exe = '\"' + mysql_path[0] + '\\bin\\mysql.exe' + '\"' 
    result = Popen(mysql_exe + ' -u' + config.mysql_user + ' -p' + config.mysql_pass + ' rpsods < "' + path + '\\query.sql"', shell=True, stdout=PIPE).communicate()
    os.remove('query.sql')

    result = result[0].decode()
    return str(result.replace("count(*)\r\n", "").replace("/r/n", ""))

def update_spreedsheet(count):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    json_path = resource_path('Kanmo-d9b63bdaacf4.json')

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)

    gc = gspread.authorize(credentials)
    wks = gc.open('Kanmo').sheet1
    hostname = os.environ['COMPUTERNAME']
    try:
        cell = wks.find(hostname.lower())
        wks.update_acell('B' + str(cell.row), count)
    except:
        row = next_available_row(wks)
        wks.update_acell('A' + str(row), hostname.lower())
        wks.update_acell('B' + str(row), count)
    
def get_promo_count():
    count = promo_count()
    update_spreedsheet(count)

def del_promo():
    sql = '''set sql_safe_updates = 0;
             delete from rpsods.pcp_promotion;
             set sql_safe_updates = 1;'''
    mysql_path = get_mysql_path()
    sql_file = open('query.sql', 'w')
    sql_file.write(sql)
    sql_file.close()
    path = os.getcwd()
    mysql_exe = '\"' + mysql_path[0] + '\\bin\\mysql.exe' + '\"' 
    Popen(mysql_exe + ' -u' + config.mysql_user + ' -p' + config.mysql_pass + ' rpsods < "' + path + '\\query.sql"', shell=True, stdout=PIPE).communicate()
    os.remove('query.sql')

if sys.argv[1] == 'countpromo':
    get_promo_count()

if sys.argv[1] == 'delpromo':
    del_promo()
    get_promo_count()

