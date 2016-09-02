# -*- coding: utf-8 -*-
import sys
import traceback

def printe(error):
    estr = "\n---\n"
    sys_info = sys.exc_info()
    sys_info_len = len(sys_info)
    if(sys_info_len>0):
        estr += str(sys_info[0]) + "\n"
        if(sys_info_len>1):
            estr += str(sys_info[1])  + "\n"
            if(sys_info_len>2):
                estr +=  str(traceback.format_exc()) + "\n"

    estr += "\n---\n"
    estr += str(error)

    print(estr)
