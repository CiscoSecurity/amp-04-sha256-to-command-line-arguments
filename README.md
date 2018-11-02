### AMP for Endpoints SHA256 to command line arguments

Takes a SHA256 as input and queries the environment extracting command line arguments used by processes associated with the SHA256.

### Before using you must update the following:
The authentictaion parameters are set in the ```api.cfg``` :
- client_id 
- api_key

### Usage
Provide a SHA256 as a command line argument
```
sha256_to_command_line_arguments.py 935c1861df1f4018d698e8b65abfa02d7e9037d8f68ca3c2065b6ca165d44ad2
```

### Example script output:  
```
Computers found: 1
Querying: Demo_Command_Line_Arguments_Meterpreter - d2721a44-3795-4138-a73a-f36e6d8b0201

Process names observed for the SHA256:
   cmd.exe

Command line parameters observed:
   C:\WINDOWS\system32\cmd.exe /C start C:\WINDOWS\system32\cmd.exe /C \WINDOWS\Temp\FKUTjPgkVklDJrbi.bat
   cmd.exe /c echo smzhqd > \\.\pipe\smzhqd
   cmd
   C:\WINDOWS\system32\cmd.exe /C echo net user  R3@dy12345 /add
   C:\Windows\System32\cmd.exe
   C:\WINDOWS\system32\cmd.exe

This SHA256 was also the parent of 3 processes
ping.exe
   ping so-hgnpp72
   ping so-hgn9972
   ping so-4dnqp72
   ping so-59npp72
net.exe
   net user  /delete
   net user
   net user  R3@dy12345 /add
cmd.exe
   C:\WINDOWS\system32\cmd.exe /C start C:\WINDOWS\system32\cmd.exe /C \WINDOWS\Temp\FKUTjPgkVklDJrbi.bat
```
