# chrome_automation

## Usage

```bash
python main.py --url https://www.linkedin.com/in/{linkedin_username}
```
## Setup virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```
## Run the following commands to start chrome automation

### MacOS
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="$(echo $HOME)/Library/Application Support/Google/Chrome"
```

### Windows
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\<username>\AppData\Local\Google\Chrome\User Data"
```
