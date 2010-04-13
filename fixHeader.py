import GPS
from os.path import *

HEADER="""------------------------------------------------------------------------------
--                                                                          --
--                             0MQ Ada-binding                              --
--                                                                          --
%(name)s
--                                                                          --
%(ext)s
--                                                                          --
--            Copyright (C) 2010-2011, per.sandberg@bredband.net            --
--                                                                          --
-- 0MQ Ada-binding is free software;  you can  redistribute it  and/or      --
-- modify it under terms of the  GNU General Public License as published    --
-- by the Free Soft-ware  Foundation;                                       --
-- either version 2,  or (at your option) any later version.                --
-- 0MQ Ada-binding is distributed in the hope that it will be useful, but   --
-- WITH OUT ANY WARRANTY;                                                   --
-- without even the  implied warranty of MERCHANTABILITY or                 --
-- FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License    --
-- for  more details.  You should have  received  a copy of the GNU General --
-- Public License  distributed with GNAT;  see file COPYING.  If not, write --
-- to  the  Free Software Foundation,  51  Franklin  Street,  Fifth  Floor, --
-- Boston, MA 02110-1301, USA.                                              --
--                                                                          --
-- As a special exception,  if other files  instantiate  generics from this --
-- unit, or you link  this unit with other files  to produce an executable, --
-- this  unit  does not  by itself cause  the resulting  executable  to  be --
-- covered  by the  GNU  General  Public  License.  This exception does not --
-- however invalidate  any other reasons why  the executable file  might be --
-- covered by the  GNU Public License.                                      --
--                                                                          --
------------------------------------------------------------------------------
"""
import string
def to80Comment(s):
   n= 76 - len(s)
   n=n/2
   ret = "--" + (" " * n) + s
   ret = ret + (" " * (76 - len(ret))) + "--"
   return ret

def fixFile(f):
   name,ext=splitext(basename(f.name()))
   name=name.upper().replace("-",".")
   if ext==".ads":
      ext="S p e c"
   elif ext==".adb":
      ext="B o d y"
   elif ext==".gpr":
      ext="P r o j e c t"
   name =to80Comment( string.join(name," "))
   ext  =to80Comment( ext )

   print HEADER % {"name" : name , "ext" : ext}



for i in GPS.Project("zmq").sources():
   fixFile(i)
