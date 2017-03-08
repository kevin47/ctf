#!/usr/bin/python
import angr
b = angr.Project('./angrman')
pg = b.factory.path_group().explore(find=0x400d2b)
print repr(pg.found[0].state.posix.dumps(0))
