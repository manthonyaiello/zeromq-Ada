#!/usr/bin/env python
#  ---------------------------------------------------------------------------
#            Copyright (C) 2020-2030, per.s.sandberg@bahnhof.se
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files
#  (the "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and / or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to
#  the following conditions :
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
#  ---------------------------------------------------------------------------

import GPS
from os.path import *
import string

HEADER = \
"""##############################################################################
##                                                                          ##
##                             0MQ Ada-binding                              ##
##                                                                          ##
%(name)s
##                                                                          ##
%(ext)s
##                                                                          ##
##            Copyright (C) 2013-2020, per.s.sandberg@bahnhof.se            ##
##                                                                          ##
## 0MQ Ada-binding is free software;  you can  redistribute it  and/or      ##
## modify it under terms of the  GNU General Public License as published    ##
## by the Free Soft-ware  Foundation;                                       ##
## either version 2,  or (at your option) any later version.                ##
## 0MQ Ada-binding is distributed in the hope that it will be useful, but   ##
## WITH OUT ANY WARRANTY;                                                   ##
## without even the  implied warranty of MERCHANTABILITY or                 ##
## FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License    ##
## for  more details.  You should have  received  a copy of the GNU General ##
## Public License  distributed with GNAT;  see file COPYING.  If not, write ##
## to  the  Free Software Foundation,  51  Franklin  Street,  Fifth  Floor, ##
## Boston, MA 02110-1301, USA.                                              ##
##                                                                          ##
## As a special exception,  if other files  instantiate  generics from this ##
## unit, or you link  this unit with other files  to produce an executable, ##
## this  unit  does not  by itself cause  the resulting  executable  to  be ##
## covered  by the  GNU  General  Public  License.  This exception does not ##
## however invalidate  any other reasons why  the executable file  might be ##
## covered by the  GNU Public License.                                      ##
##                                                                          ##
##############################################################################
"""


def to80Comment(s):
    if len(s) > 76:
        s = s.replace(" ", "")
    if len(s) > 76:
        s = s[:-76]
    n = 76 - len(s)
    n = n/2
    ret = "##" + (" " * n) + s
    ret = ret + (" " * (76 - len(ret))) + "##"
    return ret


def getHeader(f):
    name, ext = splitext(basename(f.name()))
    name = name.upper().replace("-", ".")
    name = to80Comment(string.join(name, " "))
    if ext == ".ads":
        ext = to80Comment("S p e c")
        return(HEADER % {"name": name, "ext": ext}).replace("#", "-")
    elif ext == ".adb":
        ext = to80Comment("B o d y")
        return (HEADER % {"name": name, "ext": ext}).replace("#", "-")
    elif ext == ".gpr":
        ext = to80Comment("P r o j e c t")
        return (HEADER % {"name": name, "ext": ext}).replace("#", "-")
    else:
        ext = to80Comment("")
        return HEADER % {"name": name, "ext": ext}


def fixFile(f, of):
    name, ext = splitext(basename(f.name()))
    ed = GPS.EditorBuffer.get(f)
    begin = ed.beginning_of_buffer()
    if (ext not in [".gpr", ".adb", ".ads",
                    ".c", ".cpp", ".h", ".hh", ".idl"]):
        begin = begin.forward_line(1)
    last = ed.beginning_of_buffer().search(r"\n\n", regexp=True)

    of.write("%s\n" % 80 * "/")
    of.write("%s\n" % f.name())
    of.write("%s\n" % 30 * "<")
    of.write("%s\n" % ed.get_chars(begin, last[0]))
    of.write("%s\n" % 30 * "<")
    of.write("%s\n" % getHeader(f))
    of.write("%s\n" % 80 * "/")

with file("temp.out", "w") as of:
    for i in GPS.Project("zmq.tests").sources():
        fixFile(i, of)



