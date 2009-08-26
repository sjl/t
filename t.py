#!/usr/bin/env python

from __future__ import with_statement

import os, hashlib, operator
from optparse import OptionParser


class InvalidTaskfile(Exception):
    pass
class AmbiguousPrefix(Exception):
    pass

_hash = lambda s: hashlib.sha1(s).hexdigest()
def _hash(s):
    """Return a hash of the given string for use as an id.
    
    Currently SHA1 hashing is used.  It should be plenty for our purposes.
    
    """
    return hashlib.sha1(s).hexdigest()

def _task_from_taskline(taskline):
    """Parse a taskline (from a task file) and return a task.
    
    A taskline should be in the format:
    
        summary text ... | meta1:meta1_value,meta2:meta2_value,...
    
    The task returned will be a dictionary such as:
    
        { 'id': <hash id>,
          'text': <summary text>,
           ... other metadata ... }
    
    """
    text, _, meta = taskline.partition('|')
    task = {'text': text.strip()}
    for piece in meta.strip().split(','):
        k, v = piece.split(':')
        task[k.strip()] = v.strip()
    return task

def _prefixes(ids):
    """Return a mapping of ids to prefixes.
    
    Each prefix will be the shortest possible substring of the ID that
    can uniquely identify it among the given group of IDs.
    
    """
    
    prefixes = {}
    for id in ids:
        others = set(ids).difference([id])
        for i in range(1, len(id)+1):
            prefix = id[:i]
            if not any(map(lambda o: o.startswith(prefix), others)):
                prefixes[id] = prefix
                break
    return prefixes


class TaskDict(object):
    """A set tasks, both finished and unfinished for a given list.
    
    The list's files are read from disk when the TaskDict is initialized. They
    can be written back out to disk with the write() function.
    
    """
    def __init__(self, taskdir='.', name='tasks'):
        """Initialize by reading the task files, if they exist."""
        self.tasks = {}
        self.done = {}
        self.name = name
        self.taskdir = taskdir
        filemap = (('tasks', self.name), ('done', '.%s.done' % self.name))
        for kind, filename in filemap:
            path = os.path.join(os.path.expanduser(self.taskdir), filename)
            if os.path.isdir(path):
                raise InvalidTaskfile
            if os.path.exists(path):
                with open(path, 'r') as tfile:
                    tls = [tl.strip() for tl in tfile.xreadlines() if tl]
                    tasks = map(_task_from_taskline, tls)
                    for task in tasks:
                        getattr(self, kind)[task['id']] = task
    
    def add_task(self, text):
        """Add a new, unfinished task with the given summary text."""
        id = _hash(text)
        self.tasks[id] = {'id': id, 'text': text}
    
    def print_list(self, kind='tasks', verbose=False):
        """Print out a nicely formatted list of unfinished tasks."""
        tasks = dict(getattr(self, kind).items())
        label = 'prefix' if not verbose else 'id'
        if not verbose:
            for id, prefix in _prefixes(tasks).items():
                tasks[id]['prefix'] = prefix
        plen = max(map(lambda t: len(t[label]), tasks.values())) if tasks else 0
        for t in tasks.values():
            print ('%-' + str(plen) + 's - %s') % (t[label], t['text'])
    
    def finish_task(self, prefix):
        """Mark the task with the given prefix as finished.
        
        If more than one task matches the prefix an AmbiguousPrefix exception
        will be raised.
        
        """
        matched = filter(lambda id: id.startswith(prefix), self.tasks.keys())
        if len(matched) == 1:
            task = self.tasks.pop(matched[0])
            self.done[task['id']] = task
        else:
            raise AmbiguousPrefix
    
    def delete_finished(self):
        """Remove all finished tasks."""
        self.done = {}
    
    def write(self):
        """Flush the finished and unfinished tasks to the files on disk."""
        filemap = (('tasks', self.name), ('done', '.%s.done' % self.name))
        for kind, filename in filemap:
            path = os.path.join(os.path.expanduser(self.taskdir), filename)
            if os.path.isdir(path):
                raise InvalidTaskfile
            with open(path, 'w') as tfile:
                tasks = getattr(self, kind).values()
                tasks.sort(key=operator.itemgetter('id'))
                for task in tasks:
                    meta = [m for m in task.items() if m[0] != 'text']
                    meta_str = ', '.join('%s:%s' % m for m in meta)
                    tfile.write('%s | %s\n' % (task['text'], meta_str))
    

def build_parser():
    parser = OptionParser()
    
    parser.add_option("-a", "--add",
                      action="store_true", dest="add", default=True,
                      help="add the text as a task (default)")
    
    parser.add_option("-e", "--edit", dest="edit",
                      help="edit TASK", metavar="TASK")
    
    parser.add_option("-f", "--finish", dest="finish",
                      help="mark TASK as finished", metavar="TASK")
    
    parser.add_option("-l", "--list", dest="name", default="tasks",
                      help="work on LIST", metavar="LIST")
    
    parser.add_option("-t", "--task-dir", dest="taskdir", default="",
                      help="work in DIR", metavar="DIR")
    
    parser.add_option("-D", "--delete-finished", dest="delete_finished",
                      action="store_true", default=False,
                      help="delete finished items to save space")
    
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print more detailed output (full task ids, etc)")
    return parser

def _main():
    (options, args) = build_parser().parse_args()
    
    td = TaskDict(taskdir=options.taskdir, name=options.name)
    text = ' '.join(args)
    
    if options.finish:
        td.finish_task(options.finish)
        td.write()
    elif options.delete_finished:
        td.delete_finished()
        td.write()
    elif text:
        td.add_task(text)
        td.write()
    else:
        td.print_list(verbose=options.verbose)


if __name__ == '__main__':
    _main()
