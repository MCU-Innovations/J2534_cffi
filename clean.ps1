Remove-Item build -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item dist -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item *.egg-info -Force -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Include src/*.c | Remove-Item -Recurse -Force -Confirm:$False
Get-ChildItem -Recurse -Include src/*.pyd | Remove-Item -Recurse -Force -Confirm:$False
Get-ChildItem -Recurse -Include src/*.pyc | Remove-Item -Recurse -Force -Confirm:$False
Get-ChildItem -Recurse -Directory -Include __pycache__ | Remove-Item -Recurse -Force -Confirm:$False
Remove-Item j2534_cffi/_version.py -Force -Recurse -ErrorAction SilentlyContinue