# Timelapse_cam

```
TIMELAPSE.PY
usage: [your system path to python] Timelapse.py <command> [<args>]

These are common Timelapse script commands:
  launch      Start timelapse sequence   
  cameras     
  config      
  help        
  about       
```

```
LAUNCH
usage: Timelapse.py launch [<options>] [--]

```

```
CAMERAS
usage: Timelapse.py cameras [<options>] [--]
  -l, --list            List available cameras
  -i, --info <camera>   Show info on chosen camera
```

```
CONFIG
usage: Timelapse.py config [<options>] [--]
  -l, --list  <section>             List config keys and their values of chosen section,
                                    if not specified - sections are printed
  -i, --info  <section[.key]>       Show info on chosen section/key
  -c, --check <section>             
  -e, --edit  <section.key=value>   
  -r, --reset <section[.key]>
  
examples:
  > python Timelapse.py cameras -s

  > python Timelapse.py config --edit TIME.deltaunit=FPh
```
