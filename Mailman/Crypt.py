# Copyright (C) 1998 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import mm_cfg

if mm_cfg.USE_CRYPT:
    try:
        from crypt import crypt
    except ImportError:
        pass

if not globals().has_key('crypt'):
    # couldn't import crypt.crypt
    mm_cfg.USE_CRYPT = 0
    # This is good enough.
    # XXX: should we always just use md5?
    def crypt(string, seed):
        import md5
        return md5.new(string).digest()
