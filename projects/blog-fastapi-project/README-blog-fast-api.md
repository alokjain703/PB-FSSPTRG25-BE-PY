source ../../.venv/bin/activate
uvicorn src.main:app --reload

Run on different port   
```bash
$ uvicorn src.main:app --port 8001 --reload
```

http://localhost:8000/docs
