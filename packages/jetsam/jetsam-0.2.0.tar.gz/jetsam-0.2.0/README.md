# Jetsam
- True daemonizer using native C calls  
- Currently only compatible with `*nix` file systems 
- <u>Extra Paranoid Edition</u> uses that **double fork magic!** 
> jetsam definition: floating debris ejected from a ship 

## C Extension 
To showcase a C library being used as a _native python module_

## Example 
```python
import time
import logging
import jetsam
from jetsam import daemon

# jetsam will log pids and errors from daemons 
# to a single log file. It will also update the file
# with the current status of the daemon  
#  
#   function_name:pid:status
#
jetsam.set_logfile("user_daemon.log")  # defaults to /tmp/jetsam.log

@daemon
def func1():
    logging.basicConfig(
        filename="func1.log", 
        level=logging.DEBUG, 
        filemode="w"
    )
    while True:
        time.sleep(1)
        logging.debug("Truly daemonized!")

def func2():
    logging.basicConfig(
        filename="func2.log", 
        level=logging.DEBUG, 
        filemode="w"
    )
    while True:
        time.sleep(1)
        logging.debug("I can do this all day...")


func1()  # detachs from current interpreter
daemon(func2)  # each function immediately returns 

time.sleep(3)  # a long running process...

jetsam.end_daemon(func1)
jetsam.end_daemon(func2)

print("Jettison functions with jetsam!")
```
