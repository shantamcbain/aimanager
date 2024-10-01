# -*- coding: utf-8 -*-
import inspect
import sys

def debug_print(*args):
    frame = inspect.currentframe().f_back
    message = " ".join(map(str, args))
    encoded_message = f"{frame.f_code.co_filename}:{frame.f_lineno} - {message}\n".encode('utf-8', errors='replace').decode('utf-8')
    try:
        print(encoded_message, end='')
    except UnicodeEncodeError:
        sys.stdout.write(encoded_message)
        sys.stdout.flush()