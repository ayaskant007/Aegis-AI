# Aegis AI

Aegis AI is a Windows desktop assistant built with CustomTkinter, speech recognition, and Google Gemini.


## Run Locally

1. Activate the virtual environment.
2. Set `GOOGLE_API_KEY` and `NEWS_API_KEY` in your environment.
3. Run `python main.py`.

## Build a Single-File EXE

The app is packaged with PyInstaller in one-file mode.

```powershell
python -m PyInstaller --onefile --noconsole --name AegisAI main.py
```

The resulting executable is created under `dist\AegisAI.exe`.


