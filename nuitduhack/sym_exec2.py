#!/usr/bin/python
import angr
proj = angr.Project('./step2.bin')
argv1 = angr.claripy.BVS('argv1', 8*32)
initial_state = proj.factory.entry_state(args=['./step2.bin', argv1])

initial_path = proj.factory.path(initial_state)
path_group = proj.factory.path_group(initial_state)
print 'finding'
pg = path_group.explore(find=0x400d9e)
print 'jizz'
#print repr(pg.found[0].state.posix.dumps(0))
print repr(pg.found[0].state.se.any_str(argv1))
