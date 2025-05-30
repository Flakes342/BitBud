import subprocess

def open_app(app_name):
    commands = {
        "spotify": "spotify",
        "vscode": "code",
        "youtube": "firefox https://youtube.com",
        "netflix": "firefox https://netflix.com",
        "chrome": "google-chrome",
        "terminal": "gnome-terminal",
    }
    cmd = commands.get(app_name.lower())
    if cmd:
        try:
            subprocess.Popen(cmd.split())
            return f"Opening {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"
    return f"App '{app_name}' not recognized."
