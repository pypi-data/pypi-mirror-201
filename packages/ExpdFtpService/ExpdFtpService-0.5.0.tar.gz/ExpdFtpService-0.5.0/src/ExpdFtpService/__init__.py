from os import path, sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from loguru import logger
from ftplib import FTP


class ConnFtpServer:
    """
    The ConnFtpServer class is used for connecting to a FTP Server. The constructor accepts the following parameters with the indicated types:
        hostname (str): The hostname of the FTP server.
        username (str): The username to login to the FTP server.
        password (str): The password to login to the FTP server.
    """    
    def __init__(self, hostname, username, password):
        self.ftp = FTP()
        self.ftp.connect(host=hostname, port=21)
        self.ftp.sendcmd('OPTS UTF8 ON')
        self.ftp.set_pasv(True)
        self.ftp.login(user=username, passwd=password)
        # logger.debug(self.ftp.getwelcome())


class ExpdDownloadFtpServerFile(ConnFtpServer):
    def __init__(self, hostname, username, password, destfolder, savefolder, fstartwith=None, filendwith=None):
        super().__init__(hostname, username, password)
        self.destfolder = destfolder
        self.savefolder = savefolder
        self.fstartwith = fstartwith 
        self.filendwith = filendwith 
        
    @property
    def files(self):
        self.ftp.cwd(self.destfolder)
        if self.fstartwith is not None:
            files = [x for x in self.ftp.nlst() if x.startswith(self.fstartwith)]
        elif self.filendwith is not None:
            files = [x for x in self.ftp.nlst() if x.endswith(self.filendwith)]
        else:
            files = [x for x in self.ftp.nlst() if str(x).lower() != 'history']
        if len(files) == 0:
            logger.warning("No files to download, scripting will be exiting")
            sys.exit()
        else:
            logger.debug(f"server total files: [{len(files)}]")
        return files
    
    def archive(self, from_file, to_path, to_file):
        history = self.ftp.nlst(to_path)
        if to_file not in history:
            self.ftp.rename(f"{from_file}", f"{to_path}\{to_file}")
            # logger.debug(f"server file [ {from_file} ] archived to history folder successfully.")
        else:
            logger.warning(f"file exist in history folder, delete: {from_file}")
            self.ftp.delete(from_file)

    @logger.catch(reraise=True)
    def download(self, numbers):
        try:
            for count, file in enumerate(self.files, 1):
                with open(path.join(self.savefolder, f"{file}"), 'wb') as rd:
                    self.ftp.retrbinary('RETR %s' % file, rd.write)
                self.archive(file, "History", file)
                logger.debug(f"NO.{count}: file {file} download & archived successfully")
                if count == numbers:
                    break
        finally:
            self.ftp.quit()
    

class ExpdUploadFtpServerFile(ConnFtpServer):
    """Class is used for connecting to a FTP Server and upload files.
        The constructor accepts the following parameters with the indicated types:
            destfolder (str): The full path on the FTP server to upload the file from, create it automatically when the folder does not exists,.
            local_file (str): The local file on the computer to upload to server.
    """    
    def __init__(self, hostname, username, password, destfolder=None):
        super().__init__(hostname, username, password)
        self.destfolder = destfolder
        self.create_directory(self.destfolder)

    def create_directory(self, folder):
        if not self.directory_exists(folder):
            self.ftp.mkd(folder)

    def directory_exists(self, directory):
        parent = path.dirname(directory)
        pathes = self.ftp.nlst(parent)
        return True if directory in pathes else False
    
    @logger.catch(reraise=True)
    def upload_file_to_server(self, local_file):
        try:
            with open(local_file,'rb') as f:  
                self.ftp.cwd(self.destfolder)          
                self.ftp.storbinary(f'STOR {path.basename(local_file)}', f)
                logger.debug(f"{local_file} uploaded successfully")
        finally:
            self.ftp.quit()
    

if __name__ == '__main__':
    ExpdUploadFtpServerFile(
        hostname="sha-comm02.sha.ei",
        username="xxx",
        password="xxx",
        destfolder="/ftp/GEO/testpath这话",
    ).upload_file_to_server(r"D:\Solutions\edoc_upload_sourth_korea\server\data\History\E13I2100055\R4382481_PIE_E433594030.pdf") 