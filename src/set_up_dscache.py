""" Main entry point for dscache (well, really just the vacuum). """
import set_sys_path
from keys import KEY
from dscache.main import main as dscache_main

def main():
    dscache_main()

if __name__ == '__main__':
    if KEY.IS_LOCAL_DEV:
        set_sys_path.set_sys_path()
    main()
