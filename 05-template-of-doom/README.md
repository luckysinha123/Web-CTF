# Template of Doom

Standalone Flask web CTF challenge.

- Difficulty: Hard
- Points: 500
- Local port: 5005

## Run on Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If activation is blocked, use `\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `\.venv\Scripts\python.exe app.py`.

Open http://127.0.0.1:5005. Stop with Ctrl+C.

**Safety:** intentionally vulnerable local training app. It binds to localhost only. Do not expose it to the internet or a shared network.
