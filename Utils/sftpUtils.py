import logging
import ftplib
import paramiko
from scp import SCPClient


def sftp_file(full_filename, config):

    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()

        user = config.read_setting('User')
        tgt_url = config.read_setting('Host')
        private_key = config.read_setting('PrivateKey')
        tgt_folder = config.read_setting('TargetPath')
        filename = full_filename.split('\\')[-1]
        full_tgt_filename = tgt_folder + '/' + filename

        ssh.connect(hostname=tgt_url, username=user, key_filename=private_key, port=22)

        with SCPClient(ssh.get_transport()) as scp:
            scp.put(full_filename, full_tgt_filename)
            logging.info(f'sftp put {full_filename}  {full_tgt_filename}')

        ssh.close()  # Close connection
    except Exception as e:
        logging.critical(e)


def ftp_file(full_filename, config):
    '''
    ftp the file specified file
    :param full_filename: the name of the filename we want to ftp
    :param config: the config file object tht contains the ftp params
    :return:
    '''
    try:
        user = config.read_setting('User')
        tgt_url = config.read_setting('Host')
        password = config.read_setting('Password')
        tgt_path = config.read_setting('TargetPath')
        filename = full_filename.split('\\')[-1]
        session = ftplib.FTP(tgt_url, user, password)
        file = open(full_filename, 'rb')  # file to send
        session.cwd(tgt_path)
        logging.info('pwd is' + session.pwd())
        session.storbinary(f'STOR {filename}', file)  # send the file
        file.close()  # close file and FTP
        session.quit()
    except Exception as e:
        logging.critical(e)
