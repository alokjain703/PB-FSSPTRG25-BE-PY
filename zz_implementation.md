# FAST API
## Getting started
```bash
python3 --version 
``` 


### create and activate python virtual env at root level
python3 -m venv path/to/venv  
```bash
python3 -m venv .venv 
```
On MAC  
source path/to/venvbin/activate  
```bash
e.g. source .venv/bin/activate
```

### install FastAPI related stuff
pip3 install fastapi uvicorn

alternatively 

pip install "fastapi[all]"


### Running The App
```bash
$ uvicorn app.main:app  --reload   
``` 
Run on different port   
```bash
$ uvicorn app.main:app --port 8001 --reload
```

### switching the environment
environments allowed are "development", "testing" and "production"
export APP_ENV=testing 

### accessing the app and the docs
http://127.0.0.1:8001/

http://127.0.0.1:8001/docs


## Addvanced install
https://fastapi.tiangolo.com/advanced/settings/?h=environ

for Pydantic settings

pip3 install pydantic-settings

