import os

VERSION = "v0.0.9"

CONFIG_HOME = os.path.join("~", ".pyclavis")
PROVIDER_SEP = "/"

fnam = os.path.expanduser(CONFIG_HOME)
if os.path.exists(fnam) and os.path.isfile(fnam):
    with open(fnam) as f:
        nam = f.read()
        nam = nam.strip()
        nam = os.path.expanduser(nam)
        nam = os.path.expanduser(nam)
        CONFIG_HOME = nam

DOWNLOAD_HOME = os.path.join(CONFIG_HOME, "downloads")
