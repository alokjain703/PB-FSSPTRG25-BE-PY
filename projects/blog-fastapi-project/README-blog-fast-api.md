source ../../.venv/bin/activate
uvicorn src.main:app --reload

Run on different port   
```bash
$ uvicorn src.main:app --port 8001 --reload
```

http://localhost:8000/docs

## how to run the tests
install pytest and pytest-asyncio if not already installed
pip3 install pytest pytest-asyncio
pytest tests/test_user.py --asyncio-mode=auto --maxfail=1 --disable-warnings -q
pytest tests/test_user.py --asyncio-mode=auto -v
