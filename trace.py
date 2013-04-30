from __future__ import print_function
import sys
import os
import runpy
from traceback import format_exception, extract_tb
import pprint
import functools


stderr = functools.partial(print, file=sys.stderr)

# def stack_trace_here(exit=None):


def limited_repr(value, limit):
    etc = ' (...)'
    limit -= len(etc)
    repr_ = repr(value)
    if len(repr_) > limit:
        return repr_[:limit] + etc
    else:
        return repr_


def _print_locals(frame):
    locals = frame.f_locals

    def is_not_dunder(name):
        return not(name.startswith('__') and name.endswith('__'))

    for name in filter(is_not_dunder, locals):
        length = len(name)
        padded_name = name + ((16 - length) * ' ' if length < 16 else '')
        repr_ = limited_repr(locals[name], 70 - len(padded_name) - 1)
        stderr(padded_name, repr_)

def _print_surrounding_lines(filename, lineno):
    import linecache
    for i in range(lineno - 3, lineno + 3):
        line = linecache.getline(filename, i).rstrip()
        if i == lineno:
            stderr('%4d>%s' % (i, line))
        else:
            stderr('     %s' % line)

def _iterate_trace(trace):
    while trace:
        yield trace
        trace = trace.tb_next


def _exception_handler(type_, exception, traceback):
    frames = _iterate_trace(traceback)
    formatted = format_exception(type_, exception, traceback)
    
    exc_title, lines, exc_pretty = formatted[0], formatted[1:-1], formatted[-1]

    exc_title, exc_pretty = exc_title.strip('\n'), exc_pretty.strip('\n')

    lineids = ((filename, lineno) for filename, lineno, _, _ in extract_tb(traceback))

    stderr(exc_title)
    for frame, line, lineid in zip(frames, lines, lineids):
        stderr('-> ', line.strip().splitlines()[0])
        _print_surrounding_lines(*lineid)
        #print '-' * 4, 'locals', '-' * 4
        stderr('')
        stderr('locals:')
        _print_locals(frame.tb_frame)
        stderr('-' * 70)
    stderr(exc_pretty)


# from pdb
def main():
    if not sys.argv[1:] or sys.argv[1] in ("--help", "-h"):
        stderr("usage: trace.py scriptfile [arg] ...")
        sys.exit(2)

    filename = sys.argv[1]     # Get script filename
    if not os.path.exists(filename):
        stderr('Error:', filename, 'does not exist')
        sys.exit(1)

    del sys.argv[0]         # Hide "trace.py" from argument list

    # Replace pdb's dir with script's dir in front of module search path.
    sys.path[0] = os.path.dirname(filename)

    globs = {
        "__name__": "__main__",
        "__file__": filename,
        "__builtins__": __builtins__,
    }

    sys.excepthook = _exception_handler

    runpy.run_path(
        filename,
        init_globals=globs,
        run_name='__main__')
    

if __name__ == '__main__':
    main()

