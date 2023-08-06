#%%
import requests
from wtti import __version__ as VERSION
import re

NEW_VERSION_TIP = """
──────────────────────────────────────────────────────
New version available \033[31m{version}\033[0m → \033[32m{new_version}\033[0m
Run \033[33mpip install --upgrade MTTI\033[0m to update!
"""

#%%
def check_new_version():
    try:
        url = "https://pypi.org/simple/wtti/"
        resp = requests.get(url, timeout=3)
        html = resp.text

        last_stable_version = re.findall(r"WTTI-([\d.]*?).tar.gz", html)[-1]
        now_version = VERSION


        if now_version < last_stable_version:
            new_version = f"MTTI=={last_stable_version}"
            if new_version:
                version = f"MTTI=={VERSION.replace('-beta', 'b')}"
                tip = NEW_VERSION_TIP.format(version=version, new_version=new_version)
                print(tip)
    except Exception as e:
        pass
