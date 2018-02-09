# watermarker

```
usage: watermarker.py [-h] [-o OUT] [-t {tile}] [-s SPACE] [--show]
                      [--opacity OPACITY]
                      filepath watermarkpath

positional arguments:
  filepath              image file path or directory
  watermarkpath         watermark file path

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     image output directory
  -t {tile}, --type {tile}
                        type of add watermark. allowed [tile, ]
  -s SPACE, --space SPACE
                        space of tile watermark image
  --show                is show watermark result if set true.
  --opacity OPACITY     opacity of add watermark, default is 1.0
```


## scripts
a quick run bat demo for pyinstaller build `.exe` file
```bash
@echo off
cd /d %~dp0
for %%i in (%*) do %~dp0/watermarker/watermarker.exe %%i ./watermark.png
pause
```
