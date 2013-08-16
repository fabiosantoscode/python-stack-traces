from __future__ import print_function
import os
import trace


if __name__ == '__main__':
    print('running example file!')
    print('__file__ is', __file__)
    print('this folder:', os.path.realpath('.'))

    var_outside_all = 3
    another_thing = 1
    @trace.trace_here
    def outer_func():
        var_in_outer_func = {'here': 'is', 'a': dict()}
        def inner_func():
            here_we_have = 'a local variable'.split()
            lists_of_lists = [
                [[None], [False], [123],],
                [[], ['some'], ['basd'],],
                [[], [], [u'asd'],],
                [[],],
            ]
            and_a_range = list(range(0, 10))
            
            lets_cause_a_mess = 1 / 0

        inner_func()
    outer_func()

