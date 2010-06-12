#!/usr/bin/env python

"""t is for people that want do things, not organize their tasks."""

from __future__ import with_statement

import os, re, sys, hashlib
from operator import itemgetter
from optparse import OptionParser, OptionGroup


class InvalidTaskfile(Exception):
    """Raised when the path to a task file already exists as a directory."""
    pass

class AmbiguousPrefix(Exception):
    """Raised when trying to use a prefix that could identify multiple tasks."""
    def __init__(self, prefix):
        super(AmbiguousPrefix, self).__init__()
        self.prefix = prefix
    

class UnknownPrefix(Exception):
    """Raised when trying to use a prefix that does not match any tasks."""
    def __init__(self, prefix):
        super(UnknownPrefix, self).__init__()
        self.prefix = prefix
    


def _hash(text):
    """Return a hash of the given text for use as an id.
    
    Currently SHA1 hashing is used.  It should be plenty for our purposes.
    
    """
    return hashlib.sha1(text).hexdigest()

def _task_from_taskline(taskline):
    """Parse a taskline (from a task file) and return a task.
    
    A taskline should be in the format:
    
        summary text ... | meta1:meta1_value,meta2:meta2_value,...
    
    The task returned will be a dictionary such as:
    
        { 'id': <hash id>,
          'text': <summary text>,
           ... other metadata ... }
    
    A taskline can also consist of only summary text, in which case the id
    and other metadata will be generated when the line is read.  This is
    supported to enable editing of the taskfile with a simple text editor.
    """
    if '|' in taskline:
        text, _, meta = taskline.partition('|')
        task = { 'text': text.strip() }
        for piece in meta.strip().split(','):
            label, data = piece.split(':')
            task[label.strip()] = data.strip()
    else:
        text = taskline.strip()
        task = { 'id': _hash(text), 'text': text }
    return task

def _tasklines_from_tasks(tasks):
    """Parse a list of tasks into tasklines suitable for writing."""
    
    tasklines = []
    tlen = max(map(lambda t: len(t['text']), tasks)) if tasks else 0
    
    for task in tasks:
        meta = [m for m in task.items() if m[0] != 'text']
        meta_str = ', '.join('%s:%s' % m for m in meta)
        tasklines.append('%s | %s\n' % (task['text'].ljust(tlen), meta_str))
    
    return tasklines

def _prefixes(ids):
    """Return a mapping of ids to prefixes in O(n) time.
    
    This is much faster than the naitive t function, which
    takes O(n^2) time.
    
    Each prefix will be the shortest possible substring of the ID that
    can uniquely identify it among the given group of IDs.
    
    If an ID of one task is entirely a substring of another task's ID, the
    entire ID will be the prefix.
    """
    pre = {}
    for id in ids:
        id_len = len(id)
        for i in range(1, id_len+1):
            """ identifies an empty prefix slot, or a singular collision """
            prefix = id[:i]
            if (not prefix in pre) or (pre[prefix] != ':' and prefix != pre[prefix]):
                break
        if prefix in pre:
            """ if there is a collision """
            collide = pre[prefix]
            for j in range(i,id_len+1):
                if collide[:j] == id[:j]:
                    pre[id[:j]] = ':'
                else:
                    pre[collide[:j]] = collide
                    pre[id[:j]] = id
                    break
            else:
                pre[collide[:id_len+1]] = collide
                pre[id] = id
        else:
            """ no collision, can safely add """
            pre[prefix] = id
    pre = dict(zip(pre.values(),pre.keys()))
    if ':' in pre:
        del pre[':']
    return pre


class TaskDict(object):
    """A set of tasks, both finished and unfinished, for a given list.
    
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
                    tls = [tl.strip() for tl in tfile if tl]
                    tasks = map(_task_from_taskline, tls)
                    for task in tasks:
                        getattr(self, kind)[task['id']] = task
    
    def __getitem__(self, prefix):
        """Return the unfinished task with the given prefix.
        
        If more than one task matches the prefix an AmbiguousPrefix exception
        will be raised, unless the prefix is the entire ID of one task.
        
        If no tasks match the prefix an UnknownPrefix exception will be raised.
        
        """
        matched = filter(lambda tid: tid.startswith(prefix), self.tasks.keys())
        if len(matched) == 1:
            return self.tasks[matched[0]]
        elif len(matched) == 0:
            raise UnknownPrefix(prefix)
        else:
            matched = filter(lambda tid: tid == prefix, self.tasks.keys())
            if len(matched) == 1:
                return self.tasks[matched[0]]
            else:
                raise AmbiguousPrefix(prefix)
    
    def add_task(self, text):
        """Add a new, unfinished task with the given summary text."""
        task_id = _hash(text)
        self.tasks[task_id] = {'id': task_id, 'text': text}
    
    def edit_task(self, prefix, text):
        """Edit the task with the given prefix.
        
        If more than one task matches the prefix an AmbiguousPrefix exception
        will be raised, unless the prefix is the entire ID of one task.
        
        If no tasks match the prefix an UnknownPrefix exception will be raised.
        
        """
        task = self[prefix]
        if text.startswith('s/') or text.startswith('/'):
            text = re.sub('^s?/', '', text).rstrip('/')
            find, _, repl = text.partition('/')
            text = re.sub(find, repl, task['text'])
        
        task['text'] = text
    
    def finish_task(self, prefix):
        """Mark the task with the given prefix as finished.
        
        If more than one task matches the prefix an AmbiguousPrefix exception
        will be raised, if no tasks match it an UnknownPrefix exception will
        be raised.
        
        """
        task = self.tasks.pop(self[prefix]['id'])
        self.done[task['id']] = task
    
    def print_list(self, kind='tasks', verbose=False, quiet=False, grep=''):
        """Print out a nicely formatted list of unfinished tasks."""
        tasks = dict(getattr(self, kind).items())
        label = 'prefix' if not verbose else 'id'
        
        if not verbose:
            for task_id, prefix in _prefixes(tasks).items():
                tasks[task_id]['prefix'] = prefix
        
        plen = max(map(lambda t: len(t[label]), tasks.values())) if tasks else 0
        for task in tasks.values():
            if grep.lower() in task['text'].lower():
                p = '%s - ' % task[label].ljust(plen) if not quiet else ''
                print p + task['text']
    
    def write(self, delete_if_empty=False):
        """Flush the finished and unfinished tasks to the files on disk."""
        filemap = (('tasks', self.name), ('done', '.%s.done' % self.name))
        for kind, filename in filemap:
            path = os.path.join(os.path.expanduser(self.taskdir), filename)
            if os.path.isdir(path):
                raise InvalidTaskfile
            tasks = sorted(getattr(self, kind).values(), key=itemgetter('id'))
            if tasks or not delete_if_empty:
                with open(path, 'w') as tfile:
                    for taskline in _tasklines_from_tasks(tasks):
                        tfile.write(taskline)
            elif not tasks and os.path.isfile(path):
                os.remove(path)
    


def _build_parser():
    """Return a parser for the command-line interface."""
    usage = "Usage: %prog [-d DIR] [-l LIST] [options] [TEXT]"
    parser = OptionParser(usage=usage)
    
    actions = OptionGroup(parser, "Actions",
        "If no actions are specified the TEXT will be added as a new task.")
    actions.add_option("-e", "--edit", dest="edit", default="",
                       help="edit TASK to contain TEXT", metavar="TASK")
    actions.add_option("-f", "--finish", dest="finish",
                       help="mark TASK as finished", metavar="TASK")
    parser.add_option_group(actions)
    
    config = OptionGroup(parser, "Configuration Options")
    config.add_option("-l", "--list", dest="name", default="tasks",
                      help="work on LIST", metavar="LIST")
    config.add_option("-t", "--task-dir", dest="taskdir", default="",
                      help="work on the lists in DIR", metavar="DIR")
    config.add_option("-d", "--delete-if-empty",
                      action="store_true", dest="delete", default=False,
                      help="delete the task file if it becomes empty")
    parser.add_option_group(config)
    
    output = OptionGroup(parser, "Output Options")
    output.add_option("-g", "--grep", dest="grep", default='',
                      help="print only tasks that contain WORD", metavar="WORD")
    output.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print more detailed output (full task ids, etc)")
    output.add_option("-q", "--quiet",
                      action="store_true", dest="quiet", default=False,
                      help="print less detailed output (no task ids, etc)")
    parser.add_option_group(output)
    
    return parser

def _main():
    """Run the command-line interface."""
    (options, args) = _build_parser().parse_args()
    
    td = TaskDict(taskdir=options.taskdir, name=options.name)
    text = ' '.join(args).strip()
    
    try:
        if options.finish:
            td.finish_task(options.finish)
            td.write(options.delete)
        elif options.edit:
            td.edit_task(options.edit, text)
            td.write(options.delete)
        elif text:
            td.add_task(text)
            td.write(options.delete)
        else:
            td.print_list(verbose=options.verbose, quiet=options.quiet,
                          grep=options.grep)
    except AmbiguousPrefix, e:
        sys.stderr.write('The ID "%s" matches more than one task.' % e.prefix)
    except UnknownPrefix, e:
        sys.stderr.write('The ID "%s" does not match any task.' % e.prefix)


if __name__ == '__main__':
    _main()
