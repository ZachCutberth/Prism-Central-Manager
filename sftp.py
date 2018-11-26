# Connect to transfer.retailpro.com and download PrismCentralManager executables
# By Zach Cutberth

import pysftp
import config

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

srv = pysftp.Connection(host='transfer.retailpro.com', username=config.sftp_user, password=config.sftp_pass, cnopts=cnopts)

srv.get_d('/Kanmo/PrismCentralManager', 'c:\\rpsupport\\PrismCentralManager\\', True)

srv.close()

