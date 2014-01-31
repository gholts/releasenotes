""" Entry point for fantasm (just to get our paths set up correctly). """
import set_sys_path
from keys import KEY
from fantasm.main import main as fantasm_main

def main():
    fantasm_main()

if __name__ == '__main__':
    if KEY.IS_LOCAL_DEV:
        set_sys_path.set_sys_path()
    main()
