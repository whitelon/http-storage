# HTTP storage daemon

## Start daemon
```
python3 storagedaemon.py
```

## Stop daemon
```
killall httpstorage
```

## Upload file
Perform POST HTTP request to `127.0.0.1:44184` with `file` field in body. 
Hash of the uploaded file will be returned in `file_hash` response body field 

## Download file
Perform GET HTTP request to `127.0.0.1:44184/{hash}` where `{hash}` is hash of the file

## Delete file
Perform DELETE HTTP request to `127.0.0.1:44184/{hash}` where `{hash}` is hash of the file
