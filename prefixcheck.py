'''
Test the prefix generating method of t vs my bug program

Created on Jun 11, 2010

@author: Michael Diamond
'''

import math,random,hashlib,cProfile

#
# Initial t Prefix
#
def t_prefixes(ids):
    """Return a mapping of ids to prefixes.
    
    Each prefix will be the shortest possible substring of the ID that
    can uniquely identify it among the given group of IDs.
    
    If an ID of one task is entirely a substring of another task's ID, the
    entire ID will be the prefix.
    
    """
    prefixes = {}
    for task_id in ids:
        others = set(ids).difference([task_id])
        for i in range(1, len(task_id)+1):
            prefix = task_id[:i]
            if not any(map(lambda o: o.startswith(prefix), others)):
                prefixes[task_id] = prefix
                break
            prefixes[task_id] = task_id
    return prefixes

#
# New t Prefix
#
def new_prefixes(ids):
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
        #print(id)
        id_len = len(id)
        for i in range(1, id_len+1):
            """ identifies an empty prefix slot, or a singular collision """
            prefix = id[:i]
            #print (pre)
            #print (prefix)
            if (not prefix in pre) or (pre[prefix] != ':' and prefix != pre[prefix]):
                break
        #print (prefix)
        #print ("--")
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
        #print("Additional")
        #print(pre)
        #print("\n***\n")
    pre = dict(zip(pre.values(),pre.keys()))
    if ':' in pre:
        del pre[':']
    return pre

#
# Test the prefix methods
#
def _hash(text):
    """ Return a hash of the given text for use as a testing id """
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

def _gen_ids(num, substr=.4):
    """ Generates a list of hashes of size num to be used as ids.
    substr specifies the percentage of ids that should be substrings
    of other ids """
    out = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    min = 5
    max = 15
    sub_prefix = int(math.floor(num*substr))
    num -= sub_prefix
    for _ in range(num):
        string = ''
        for x in random.sample(alphabet,random.randint(min,max)):
            string+=x
        out.append(_hash(string))
    for _ in range(sub_prefix):
        str = random.choice(out)
        if len(str) < 2:
            sub_prefix += 1
            continue
        out.append(str[:random.randint(1,len(str)-1)])
    random.shuffle(out)
    return out

def _check_prefixes(t_pre,new_pre):
    """ Tests two prefix maps to confirm they are the same """
    for k in t_pre:
        if not k in new_pre:
            raise Exception(k+" not in new.  Should be: "+new_pre[k])
        if t_pre[k] != new_pre[k]:
            raise Exception(k+" doesn't match.  t: "+t_pre[k]+" - new: "+new_pre[k])
    for k in new_pre:
        if not k in t_pre:
            raise Exception(k+" not in t.  Expected: "+new_pre[k])
        if new_pre[k] != t_pre[k]:
            raise Exception(k+" doesn't match.  new: "+new_pre[k]+" - t: "+t_pre[k])
    print("No errors found.  Both maps are identical.")
    
def check_prefixes(size=1000):
    ids = _gen_ids(size)
    _check_prefixes(t_prefixes(ids),new_prefixes(ids))

def speed_check(base=10,max_pow=7,size_limit=5000):
    for i in range(max_pow):
        size = int(math.pow(base,i))
        print("-----\n\nSize: %s\n" % size)
        globals()['ids'] = _gen_ids(size)
        #print(ids)
        
        if size <= size_limit:
            print("t_prefixes()")
            cProfile.run("t_prefixes(ids)")
        else:
            print("Too big to run t_prefixes() efficiently.  Would take several minutes.\n")
            
        print("new_prefixes()")
        cProfile.run("new_prefixes(ids)")

#check_prefixes()
speed_check()