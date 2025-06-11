To Configure this project, create an environment using the follow command:
- on Windows: Download python in official website [click here](https://www.python.org/downloads/)
- if you on MacOS:
```bash
  brew install python
```
- on Linux (Debian distribution):
```bash
  sudo apt update
  sudo apt install python3 python3-pip 
  sudo apt install python3-tk
```
( or `sudo apt install python3.10-venv`)
- Clone this project by following command:
```bash
  git init
  git clone https://github.com/Tholde/workflow-instaloader.git
```
- Configure the virtual environment:
```bash
  python3 -m venv .env # Windows: python -m venv .env
  source .env/bin/activate # Windows: .env\Scripts\activate
  pip install -r requirements.txt
 ```
or
```bash
  pip install instaloader
  instaloader "#desbravadore" --fast-update --no-pictures --no-videos --no-captions
```
if have an error in requirements installation. To run this project :
```bash
  python main.py # or python main.py --hashtag makeupartistbeligium --max 10 
```
Instaloader official documentation [click here](https://instaloader.github.io/)