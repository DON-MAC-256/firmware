#!/usr/bin/env python3
#
# (c) Copyright 2018 by Coinkite Inc. This file is part of Coldcard <coldcardwallet.com>
# and is covered by GPLv3 license found in COPYING.
#
import os, sys, pdb
from PIL import Image, ImageOps
import zlib

def read_text(fname):

    w = 0
    rows = [] 
    Z = b'\0'
    F = b'\xff'

    # do not trim whitespace; perhaps it is spacing data

    for ln in open(fname, 'rt').readlines():
        ln = ln.rstrip('\n')
        r = b''.join(F if i != ' ' else Z for i in ln)
        w = max(w, len(r))
        rows.append(r)

    assert 1 <= w < 128, w

    raw = b''
    for r in rows:
        r += Z*(w - len(r))
        raw += r

    return Image.frombytes('L', (w, len(rows)), raw).convert('1')

def read_img(fn):
    img = Image.open(fn)
    w,h = img.size
    assert 1 <= w < 128, w

    img = img.convert('L')
    # fix colour issues: assume minority colour is white (1)
    histo = img.histogram()
    assert len(histo) == 256, repr(histo)
    assert len(set(histo)) == 3, "Too many colours: "+repr(histo)

    if histo[-1] > histo[0]:
        img = ImageOps.invert(img)

    return img.convert('1', dither=False)

def compress(n, wbits=-9):
    z = zlib.compressobj(wbits=wbits)
    rv = z.compress(n)
    rv += z.flush(zlib.Z_FINISH)
    return rv

def crunch(n):
    # try them all... not finding any difference tho.
    a = [(wb,compress(n, wb)) for wb in range(-9, -15, -1)]

    a.sort(key=lambda i: (-len(i[1]), -i[0]))

    #print(' / '.join("%d => %d" % (wb,len(d)) for wb,d in a))

    return a[0]
        

def doit(outfname, fnames):

    fp = open(outfname, 'wt')

    fp.write("""\
# autogenerated; don't edit
#
class Graphics:
    # (w,h, w_bytes, wbits, data)

""")

    for fn in fnames:
        if fn.endswith('.txt'):
            img = read_text(fn)
        else:
            img = read_img(fn)

        assert img.mode == '1'
        #img.show()

        varname = fn.split('.')[0].replace('-', '_')

        w,h = img.size
        raw = img.tobytes()
        wbits, comp = crunch(raw)

        if 0:
            # is compression better?
            is_comp = len(comp)+8 < len(raw)
        else:
            # disable; taking too much runtime memory
            is_comp = False

        print("    %s = (%d, %d,  %d, %s, %r)\n" % (varname, w, h, ((w+7)//8),
                        wbits if is_comp else 0, raw if not is_comp else comp), file=fp)

        print("done: '%s' (%d x %d)" % (varname, w, h))

    fp.write("\n# EOF\n")

if 1:
    doit('graphics.py', sys.argv[1:])
