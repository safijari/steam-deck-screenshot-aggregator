#!/bin/python3

from pathlib import Path
import json
import os
import subprocess
import sys
import shutil


def main():
    do_copy = False
    if len(sys.argv) > 1 and sys.argv[1] == "copy":
        do_copy = True
    path = Path.home() / ".local/share/Steam/userdata"
    files = list(path.glob("**/screenshots/*.jpg"))

    subprocess.run(
        "curl https://api.steampowered.com/ISteamApps/GetAppList/v2/ > /tmp/appidmap.json",
        shell=True,
        check=True,
        capture_output=True,
    )

    id_map = {
        i["appid"]: i["name"]
        for i in json.load(open("/tmp/appidmap.json"))["applist"]["apps"]
    }

    dump_folder = Path.home() / "Pictures" / "Screenshots"

    for f in files:
        appid = int(f.parent.parent.name)
        name = id_map.get(appid, appid)
        final_path = dump_folder / name / f.name
        final_path.parent.mkdir(parents=True, exist_ok=True)
        if not do_copy:
            if not final_path.exists():
                os.symlink(f, final_path)
        else:
            if final_path.is_symlink():
                final_path.unlink()
            shutil.copy(f, final_path, follow_symlinks=False)


if __name__ == "__main__":
    main()
