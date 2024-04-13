# web-logs
## A simple webapp to retrieve the logs of apps

## Requirements

Have python installed

```bash
pip3 install flask
nano .env
```

Write the env vars

```bash
LOGS_VIEWER_PASSWORD="ABCDE"
LOGS_VIEWER_REDIRECT="https://example.com"
LOGS_VIEWER_PORT=10000
```

Edit the paths to the logs folders in `config.py`

```py
log_paths = {
    'An app with thousand users': '/home/success/awesomeapp/logs/admin_only',
    'My amazing bot !': '/home/discord/top-secret-bot/logs'
}
```

## Run

```bash
source .env && mkdir -p logs && nohup python3 app.py > logs/output.log 2>&1 &
```

## CLI Access

```bash
curl http://logs.server.url/admin?passwd=ABCDE
```

You'll get the links in the output. To download them :

```bash
curl -OJ "http://logs.server.url/logs/app/file.log?dl=1"
```

## Endpoints

- **`/`** : The entry page. You basically don't see it, as it directly prompts to enter the password. A wrong password redirects to `LOGS_VIEWER_REDIRECT`
- **`/admin?passwd=ABCDE`** : The main page. Displays the list of apps and the logs that their respective folders contains. The filename link will open the logs file in stream in another tab, while the Download link will... well download it
- **`/logs/app/file.log`** : Display the log of the `file.log` file of the application `app` in stream
- **`/logs/app/file.log?dl=1`** : Same as above but downloads the file

## Security

Only the `/admin` endpoint is protected by password. Meaning that anyone can get a `/logs` URL and see the file. But to get it in the first place, that person need to either get that URL from the `/admin` endpoint or through you, so never share a logs link publicly.  
Also the "password" protection is a simple `sha256`

## License

This project is licensed under the MIT License. Copyright (c) 2024 EDM115
