from fgmk.ff import write_file
import json
import os

def test_fwriteKeyVals():
    tfile = 'temporary_testfile'

    jsontree = {'test': [[0, 0],[0,0],[0,0]],
                'nest_things':{'thing1': ['item1', 'item2'],
                               'thing2': 'text'},
                'iamnumber': 0,
                '12':12,
                'iamnotnumber': '90'
                }

    f = open(tfile, 'w+')
    write_file.fwriteKeyVals(jsontree, f)
    f.close()

    f = None

    f = open(tfile, 'r')
    resjsontree = json.load(f)
    f.close()

    os.remove(tfile)

    assert jsontree == resjsontree


def test_writesafe_success():
    tfile = 'temporary_testfile'

    jsontree = {'test': [[0, 0],[0,0],[0,0]],
                'nest_things':{'thing1': ['item1', 'item2'],
                               'thing2': 'text'},
                'iamnumber': 0,
                '12':12,
                'iamnotnumber': '90'
                }

    write_file.writesafe(jsontree, tfile)

    f = open(tfile, 'r')
    resjsontree = json.load(f)
    f.close()

    os.remove(tfile)

    assert jsontree == resjsontree
