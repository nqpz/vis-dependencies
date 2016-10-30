import heapq
import json
import copy

def defaults(defaultDic,**otherArgs):
    bindings = {}
    for key in defaultDic.keys():
        if key in otherArgs:
            bindings[key] = otherArgs[key]
        else:
            bindings[key] = defaultDic[key]
    return bindings


def loadData(path = "../data/newdeps2.json"):
    with open(path) as f:
        plist = json.load(f)


    packages = {}
    for p in plist:
        name = p['name']
        packages[name] = p
    return packages

def banCond(key):
    bans = ["QuickCheck",
            "tasty",
            "binary", "criterion",
            "statistics",
            "snap-server",
            "test-framework","test-framework-hunit","test-framework-quickcheck2",
            "test-framework-th"
            ]
    if key in bans:
        return True
    #if "quickcheck" in key:
    #    return True
    return False


def deleteBannedDependencies(pack):
    count = 0
    keys = pack.keys()
    for key in keys:
        deps = pack[key]["dependencies"]
        for dep in deps.keys():
            if banCond(dep):
                del deps[dep]
        pack[key]["dependencies"] = deps
        if banCond(key):
            count += 1
            del pack[key]
    print count
    return pack
    


def listOutsiders(pack):
    keys = pack.keys()
    newpacks = {}
    outsiders = {}
    for key in keys:
        p = pack[key]
        outsider = []
        newdep = {}
        for dep in p["dependencies"].keys():
            if dep in keys:
                newdep[dep] = p["dependencies"][dep]
            else:
                outsider.append(dep)
        newpack = p.copy()
        newpack["dependencies"] = newdep
        newpacks[key] = newpack
        if len(outsider) > 0:
            outsiders[key] = outsider
    return (outsiders, newpacks)

def deleteEmptyDependencies(pack):
    for key in pack:
        deps = pack[key]["dependencies"]
        for dep in deps.keys():
            if len(deps[dep]) == 0:
                del deps[dep]
        pack[key]["dependencies"] = deps
    return pack

def deleteSelfRef(pack):
    for key in pack:
        deps = pack[key]["dependencies"]
        if key in deps:
            del deps[key]
        pack[key]["dependencies"] = deps
    return pack

def addRevDependencies(data):
    #data = oldData.copy()
    for key in data:
        data[key]["revDep"] = []
    for key in data:
        for target in data[key]["dependencies"]:
            data[target]["revDep"].append(key)
    return data



        
def defaultDataGen():
    d = loadData()
    #deleteBannedDependencies(d)
    (_,data) = listOutsiders(d)
    deleteSelfRef(data)
    #deleteEmptyDependencies(data)
    return addRevDependencies(data)





# API requirements:
# have .keys()
# access by []
# iterable like a dictionary

def defaultRef(data):
    return data["dependencies"]

def defaultRefRev(data):
    return data["revDep"]

def defaultKeyValueIter(data):
    for key in data:
        yield (key,data[key])

    
class Node:

    # outdated
    def addForward(self,node):
        self.forward.append(node)
    # outdated
    def addReverse(self,node):
        self.reverse.append(node)
        
    def __init__(self,data = None,**args):
        self.data = data
        self.forward = []
        self.reverse = []




class Graph:

    def ref(self,value):
        return self.refBase(self.nodes[value].data)

    def refRev(self,value):
        return self.refRevBase(self.nodes[value].data)
    
    def __init__(self, data = None,
                 dataGen = defaultDataGen,
                 ref = defaultRef,
                 refRev = defaultRefRev,
                 keyValueIter = defaultKeyValueIter, **args):
        #if "path" in arg:
        #    startData = loadData(args["path"])
        #else:
        #    startData = loadData()
        #(_,data) = listOutsiders(startData)
        #self.data = data
        if data is None:
            data = dataGen()
        #self.data = data
        self.refBase = ref
        self.refRevBase = refRev
        self.nodes = {}
        for (key,value) in keyValueIter(data):
            self.nodes[key] = Node(value)
        for node in self.nodes:
            for dep in self.ref(node):
                self.nodes[node].addForward(dep)
        for node in self.nodes:
            for dep in self.ref(node):
                self.nodes[dep].addReverse(node)



    def __iter__(self):
        return self.nodes.__iter__()

    def keys(self):
        return [k for k in self.nodes]
    def __getitem__(self,key):
        return self.nodes[key]
    def __setitem__(self,key,value):
        #self.data[key] = value
        self.nodes[key] = value
    def __delitem__(self,key):
        #del self.data[key]
        del self.nodes[key]
    def __len__(self):
        return len(self.data)
    def __contains__(self,item):
        return item in self.nodes


    def follows(self,key):
        return self.nodes[key].forward
    def before(self,key):
        return self.nodes[key].reverse


def pe(elems):
    for e in elems:
        print e

def revI(lst):
    L = len(lst)
    for i in range(L):
        yield L-(i+1)

def dependsD(data,base,other):
    return other in data[base]["dependencies"]

# speed O(n^2 lg n)
# doesnt work
def orderIter(data):
    misDep = [(len(data[name]["dependencies"]), name ) for name in data]
    misDep.sort()
    #heapq.heapify(misDep)
    result = []
    while len(misDep) > 0:
        (d,p) = misDep[0]
        if d > 0:
            print "error"
            print "left: ", len(misDep)
            break
        result.append(p)
        del misDep[0]
        for i in range(len(misDep)):
            (dr,name) = misDep[i]
            if p in data[name]['dependencies']:
                #print "."
                misDep[i] = (dr-1,name)
        misDep.sort()
    misses = {}
    for (d,p) in misDep:
        misses[p] = d
    return (result, misses)

def ordering(data):
    misDep = {name:len(data[name]["dependencies"]) for name in data}
    result = []
    tiebreaker =  lambda i: len(data[i]["revDep"])
    for name in misDep.keys():
        if misDep[name] == 0:
            result.append(name)
            del misDep[name]
    result.sort(key = tiebreaker, reverse = True)
    i = 0
    while i < len(result):
        name = result[i]
        stack = []
        for rdep in data[name]["revDep"]:
            if rdep in misDep:
                misDep[rdep] -= 1
                if misDep[rdep] == 0:
                    stack.append(rdep)
        for rdep in sorted(stack, key = tiebreaker, reverse = True):
            result.append(rdep)
            del misDep[rdep]
        i += 1
    if len(misDep) > 0:
        print "error"
        print "left: ", len(misDep)
    return (result, misDep)

def orderingLayer(data):
    misDep = {name:len(data[name]["dependencies"]) for name in data}
    result = []
    layer = []
    tiebreaker =  lambda i: len(data[i]["revDep"])
    for name in misDep.keys():
        if misDep[name] == 0:
            layer.append(name)
            del misDep[name]
    layer.sort(key = tiebreaker, reverse = True)
    result.append(layer)
    i = 0
    while i < len(result):
        previousLayer = layer
        layer = []
        for j in range(len(previousLayer)):
            name = previousLayer[j]
            stack = []
            for rdep in data[name]["revDep"]:
                if rdep in misDep:
                    misDep[rdep] -= 1
                    if misDep[rdep] == 0:
                        stack.append(rdep)
            for rdep in sorted(stack, key = tiebreaker, reverse = True):
                layer.append(rdep)
                del misDep[rdep]
        if len(layer):
            result.append(layer)
        i += 1
    if len(misDep) > 0:
        print "error"
        print "left: ", len(misDep)
    return (result, misDep)

        
##        if d == 0:
##            for rdep in data[p]["revDep"]:
##                if rdep in toUpdate:
##                    toUpdate[rdep] += 1
##                else:
##                    toUpdate[rdep] = 1
##            del misDep[0]
##            yield p
##        else:
##            if len(toUpdate) == 0:
##                print "error"
##                print "left count: ", len(misDep)
##                for (depN,name) in misDep:
##                    print " --- misses: ", depN, " name: ", name
##                print "with error, ended early"
##                break
##            for i in range(len(misDep)):
##                (dOld,name) = misDep[i]
##                if name in toUpdate:
##                    misDep[i] = (dOld - toUpdate[name],name)
##            toUpdate = {}
##            misDep.sort()
##        


def transitive(data,name, lst = None, base = None):
    if lst is None:
        lst = []
    #if name == base:
    #    print "cycle! ", name 
    if base is None:
        base = name
    else:
        lst.append(name)
    for other in data[name]["dependencies"].keys():
        if other not in lst and other != name:
            lst = transitive(data,other,lst,base)
    return lst

def findCycle(data,name,prev = None, n = None, maxDepth = 15):
    if n is None:
        n = 0
    if n > maxDepth:
        return False
    if prev is None:
        pre = [name]
    else:
        pre = []
        for k in prev:
            pre.append(k)
        pre.append(name)
        if pre[0] == name:
            return pre
    for other in data[name]["dependencies"].keys():
        if other != name:
            t = findCycle(data,other,pre,n+1)
        if t:
            return t
    return False
    
    
            

d = defaultDataGen()
(p,m) = ordering(d)

def ppm():
    s = 0
    for key in d:
        if key not in p:
            print key
            s += 1
    return s

def ts(name):
    ps = []
    for s in transitive(d,name):
        if s not in p:
            ps.append(s)
    return ps



def transitiveDep(data,order):
    orderNum = {order[i]:i for i in range(len(order))}
    ordDeps = [sorted(
        [orderNum[i] for i in data[name]["dependencies"] ])
               for name in order]
    trans = {}
    for i in range(len(order)):
        trans[i] = {j:1 for j in ordDeps[i]}
        for dep in ordDeps[i]:
            for transDep in trans[dep].keys():
                trans[i][transDep] = 1
    return {name:[order[num] for num in sorted(trans[orderNum[name]].keys())]
            for name in order}


def transitiveRevDependencyScore(data,order):
    orderNum = {order[i]:i for i in range(len(order))}
    result = [1 for i in order]
    i = len(order)
    while i > 0:
        i -= 1
        for dep in data[order[i]]["dependencies"]:
            result[orderNum[dep]] += result[i]
    return {name:result[orderNum[name]] for name in order}
    
def writeTRDS():
    d =defaultDataGen()
    (order,_) = ordering(d)
    orderNum = {order[i]:i for i in range(len(order))}
    t = transitiveRevDependencyScore(d,order)
    tra= transitiveDep(d,order)
    with open("../data/trds.csv","w") as f:
        f.write("name, order, depencies, score\n")
        for name in order:
            f.write(name + ", " + str(orderNum[name]) + ", "
                    + str(len(tra[name])) + ", " + str(t[name]) +"\n")
    return None

def commonTranDep(data,trans,order):
    result = {}
    for name in order:
        for other in order:
            r = []
            for dep in trans[name]:
                if dep in trans[other]:
                    r.append(dep)
            if other in trans[name]:
                r.append(other)
            if name in trans[other]:
                r.append(name)
            result[(name,other)] = r
    return result
                
def writeCTD():
    d =defaultDataGen()
    (order,_) = ordering(d)
    orderNum = {order[i]:i for i in range(len(order))}
    t= transitiveDep(d,order)
    CTD = commonTranDep(d,t,order)
    with open("../data/ctd.csv","w") as f:
        for name in order:
            line = ""
            for other in order:
                line += str(len(CTD[(name,other)])) + ", "
            f.write(line[:-2] + "\n")
    return None

def writeOL():
    d =defaultDataGen()
    (order,_) = orderingLayer(d)
    with open("../data/ol.json","w") as f:
        json.dump(order, f)
    return None


def adjecencyMatrx(data, order):
    orderNum = {order[i]:i for i in range(len(order))}
    result = []
    for n1 in order:
        row = []
        for n2 in order:
            row.append(0)
        result.append(row)
    for name in order:
        for dep in data[name]["dependencies"].keys():
            result[orderNum[name]][orderNum[dep]] = 1
    return result

def writeAM():
    d =defaultDataGen()
    (order,_) = ordering(d)
    m = adjecencyMatrx(d,order)
    with open("../data/AM.csv","w") as f:
        for row in m:
            line = ""
            for val in row:
                line += str(val) + ", "
            f.write(line[:-2] + "\n")
    return None

def writeAMNamed(name):
    d =defaultDataGen()
    (order,_) = ordering(d)
    t= transitiveDep(d,order)
    subOrder = []
    deps = t[name]
    for i in order:
        if i in deps:
            subOrder.append(i)
    m = adjecencyMatrx(d,subOrder)
    with open("../data/AMN.csv","w") as f:
        for row in m:
            line = ""
            for val in row:
                line += str(val) + ", "
            f.write(line[:-2] + "\n")
    with open("../data/AMNnames.csv","w") as f:
        for sname in subOrder:
            f.write(sname + "\n")
    return None


def amcompare(data,order,deps1,deps2):
    orderNum = {order[i]:i for i in range(len(order))}
    result = []
    for n1 in order:
        row = []
        for n2 in order:
            row.append(0)
        result.append(row)
    for name in order:
        for dep in data[name]["dependencies"].keys():
            if dep in deps1:
                result[orderNum[name]][orderNum[dep]] = 1
            if dep in deps2:
                result[orderNum[name]][orderNum[dep]] = result[orderNum[name]][orderNum[dep]] +2
    return result

    

def writeAMCompare(name1,name2):
    d =defaultDataGen()
    (order,_) = ordering(d)
    t= transitiveDep(d,order)
    subOrder = []
    deps1 = t[name1]
    deps2 = t[name2]
    deps1.append(name1)
    deps2.append(name2)
    for i in order:
        if (i in deps1) or (i in deps2):
            subOrder.append(i)
    for i in deps1:
        if i not in deps2:
            print i
    print "/"
    for i in deps2:
        if i not in deps1:
            print i
    print len(deps1), len(deps2), len(subOrder)
    m = amcompare(d,subOrder,deps1,deps2)
    with open("../data/AMC.csv","w") as f:
        for row in m:
            line = ""
            for val in row:
                line += str(val) + ", "
            f.write(line[:-2] + "\n")
    with open("../data/AMCnames.csv","w") as f:
        for sname in subOrder:
            f.write(sname + "\n")
    return None
    
def writeTrans():
    d =defaultDataGen()
    (order,_) = ordering(d)
    t= transitiveDep(d,order)
    with open("../data/trans.json","w") as f:
        json.dump(t, f, indent = 2)
    return None

        
    
