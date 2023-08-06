from TheSilent.clear import *
import os

cyan = "\033[1;36m"
red = "\033[1;31m"

#securely destroys data
def secure_overwrite(file):
    try:
        size = os.path.getsize(file)
        for i in range(1,8):
            clear()
            print(cyan + "pass: " + str(i))
            with open(file, "wb") as f:
                for byte in range(size):
                    f.seek(byte)
                    f.write(b"0")

    except PermissionError:
        print(red + "ERROR! Permission denied!")
        exit()

    except OSError:
        pass
    
    clear()
    print(cyan + file)
    print(cyan + "done")
