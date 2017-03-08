#!/usr/bin/python
import angr
b = angr.Project('./angrman')
pg = b.factory.path_group().explore(find=lambda x: "Stream" in x.state.posix.dumps(1))
print repr(pg.found[0].state.posix.dumps(2))
