import re
from compiler.ast import  flatten


class Comparehelper():
    def __init__(self):
        print "Comparehelper"

    def compareDictOfDict(self,dict1, dict2):
        resultList = []
        for keys in dict1:
            # ignoring Time Stamp
            if isinstance(dict1.get(keys),list):
                if len(dict1.get(keys))!=len(dict2.get(keys)):
                    resultList.append("the count of "+str(keys).upper()+" in qb1 is "+str(len(dict1.get(keys)))+" but in qb2 is "+str(len(dict2.get(keys))))
                    continue
                elif dict1.get(keys)==None or dict2.get(keys)==None:
                    resultList.append("either "+str(keys)+" in qb1 is empty or in qb2")
                    continue
                else:
                    i=0
                    while(i<len(dict1.get(keys))):
                        if isinstance(dict1.get(keys)[i],dict):
                            resultList.append(self.compareDictOfDict(dict1.get(keys)[i],dict2.get(keys)[i]))
                        i += 1
            try:
                if "id" in str(keys).lower() or self.ifTimeStamp(str(dict1.get(keys))) != None:
                    continue
            except UnicodeEncodeError:
                pass
            if not isinstance(dict1.get(keys), dict):
                if dict1.get(keys) != dict2.get(keys):
                    try:
                        if not isinstance(dict1.get(keys),list):
                            resultList.append(
                                "the value of " + str(keys).upper() + " in qb1 is " + str
                                (dict1.get(keys)).upper() + " but in qb2 is " + str(
                                    dict2.get(keys)).upper())
                    except UnicodeEncodeError :
                        pass
            elif isinstance(dict1.get(keys), dict) and dict2.get(keys) != None:
                resultList.append(self.compareDictOfDict(dict1.get(keys), dict2.get(keys)))
            else:
                resultList.append("the value of " + keys + " is present in qb1 but not in qb2")

        return resultList



    def ifTimeStamp(self,str):
        pattern = re.compile('\d\d\d\d-\d\d-\d\d(T)\d\d:\d\d:\d\d-\d\d:\d\d')
        return re.match(pattern, str)


    def filterresults(self,inputlist):
        i=0
        while(i<len(inputlist)):
            inputlist[i]=[e for e in inputlist[i] if e]
            inputlist[i]=flatten(inputlist[i])
            i += 1



    def filterresultsadvance(self,inputlist):
        for values in inputlist:
            if isinstance(values,inputlist):
                self.filterresultsadvance(values)
            else:
                if not hasattr(self.filterresultsadvance, "counter"):
                    self.filterresultsadvance.outputlist = []
                    self.filterresultsadvance.outputlist.append(values)




    atom = lambda self,x: not isinstance(x, list)
    nil  = lambda self,x: not x
    car  = lambda self,x: x[0]
    cdr  = lambda self,x: x[1:]
    cons = lambda self,x, y: x + y

    flatten = lambda self,x: [x] if self.atom(x) else x if self.nil(x) else self.cons(*map(flatten, [self.car(x), self.cdr(x)]))