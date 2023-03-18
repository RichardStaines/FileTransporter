# FileTransporter
A tool that monitors a folder and will ftp/sftp any files there to a destination.

There is an internal timer which you control via the cfg. Interval, Start Time, Stop Time.
Set the Interval to 0 for a run once mode
For linux you can user via cron with Interval=0

Folder structure used:
C:\transporter
C:\transporter\send  - copy file in here to be transported
C:\transporter\done  - file gets moved into here after transported
C:\transporter\logs
C:\transporter\keys  - used for aws keys