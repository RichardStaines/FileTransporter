import sys
import os
import glob
import logging
import keyboard
import ftplib
import paramiko
from scp import SCPClient

from RepeatedTimer import RepeatedTimer
from ConfigFile import ConfigFile
# from aws_ec2 import AwsEc2Instance


# TO DO
# 1 cfg file - https://docs.python.org/3/library/configparser.html
# 2 log file


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


def process_files(config):
    mode = str.lower(config.read_setting('Mode'))
    src_folder = config.read_setting('Folder')
    done_folder = config.read_setting('DoneFolder')

    file_filter = config.read_setting('Filter')
    file_list = glob.glob(src_folder + f"\\{file_filter}")
    for full_filename in file_list:
        filename = full_filename.split('\\')[-1]
        if mode == 'sftp':
            sftp_file(full_filename, config)
        elif mode == 'ftp':
            ftp_file(full_filename, config)
        else:
            logging.critical(f'Transfer mode {mode} is not supported - please correct the config')
        full_done_filename = done_folder + '\\' + filename
        logging.info(f'Move {full_filename} to {full_done_filename}')
        os.rename(full_filename, full_done_filename)


def loop_till_quit(config):
    # key = input('Press q key to quit')
    quit_key = config.read_setting('QuitLoopKey')
    key = ''
    quit_loop = False
    if quit_key != '':
        print(f'Press {quit_key} key to quit')
    while not quit_loop:
        try:
            if quit_key != '':
                if keyboard.is_pressed(quit_key):
                    logging.info(f'{quit_key} pressed to Quit')
                    quit_loop = True
            # time.sleep(1)
        except Exception as e:
            logging.warning(e)
            quit_loop = True


def main(argv):
 #   aws = AwsEc2Instance()
 #   aws.start_aws_ec2_instance()
 #   aws.stop_aws_ec2_instance()

    cfg_reader = ConfigFile('FileTransporter.cfg')

    logging.info(f'Command Line args: {sys.argv}')

    folder_name = cfg_reader.read_setting('Folder')
    interval_secs = int(cfg_reader.read_setting('Interval'))

    logging.info(f'Monitor {folder_name} every {interval_secs} seconds')

    # interval is in seconds, 0 for run once - good for crontab
    if interval_secs > 0:
        start_time = cfg_reader.read_setting('StartTime')
        end_time = cfg_reader.read_setting('StopTime')
        logging.info(f'Between {start_time} and {end_time}')
        rpt_timer = RepeatedTimer(interval_secs, start_time, end_time, process_files, cfg_reader)
        rpt_timer.start()
        loop_till_quit(cfg_reader)
        rpt_timer.stop()
    else:
        process_files(cfg_reader)


if __name__ == '__main__':
    main(sys.argv)