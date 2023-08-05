import ftplib
import os

def upload(local_path, remote_dir='', ftp=None):
    if not ftp:
        ftp = ftplib.FTP('192.168.3.220')
        ftp.login('xinyu100', 'xinyu100.com')

    remote_path = '1TB01/data/mecord/' + remote_dir
    try:
        ftp.cwd(remote_path)
    except ftplib.error_perm as e:
        if e.args[0].startswith('550'):
            # 如果远程目录不存在，则创建它
            ftp.mkd(remote_path)
            ftp.cwd(remote_path)

    if os.path.isfile(local_path):
        with open(local_path, 'rb', encoding='UTF-8') as file:
            ftp.storbinary(f'STOR {os.path.basename(local_path)}', file)
    elif os.path.isdir(local_path):
        for filename in os.listdir(local_path):
            local_file = os.path.join(local_path, filename)
            if os.path.isfile(local_file):
                with open(local_file, 'rb', encoding='UTF-8') as file:
                    ftp.storbinary(f'STOR {filename}', file)
            elif os.path.isdir(local_file):
                subdir = os.path.join(remote_dir, filename)
                upload(local_file, subdir, ftp)
    ftp.quit()
