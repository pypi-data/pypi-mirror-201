# ExpdFtpConn

Python wrapper library for upload & download file on Expeditros Ftp Server.


How to install:

    pip install ExpdFtpService


How to use with download methods:

    from ExpdFtpService.download import ExpdDownloadFtpServerFile
    ExpdDownloadFtpServerFile(hostname, username, password, destfolder, savefolder, fstartwith).download(numbers)
    

How to use with upload methods:

    from ExpdFtpService.upload import ExpdUploadFtpServerFile
    ExpdUploadFtpServerFile(hostname, username, password, destfolder).upload_file_to_serve(r"D:\Solutions\2431295471_PIE_E433593539.pdf")

