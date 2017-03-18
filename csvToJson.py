#!/Users/thor/anaconda/bin/python
import sys
import time
import json
import re

def flatten(lst):
  # credit Martijn Pieters StackOverflow
    for elem in lst:
        if isinstance(elem, (list, tuple)):
            for nested in flatten(elem):
                yield nested
        else:
            yield elem
def checkNestedElements(x, ys):
    return any(x == checkNestedElements for checkNestedElements in flatten(ys))

class jsonObj:
    def __init__(self):
        self.jsonDictObj = {}
        self.jsonArrayObj = []
    def __call__(self):
        return self
    def returnObj(self, objType):
        objType = objType.upper()
        if objType == 'DICT':
            return self.jsonDictObj
        elif objType == 'ARRAY':
            return self.jsonArrayObj
        else:
            return None
    def returnArrayObj(self):
        return self.jsonArrayObj
    def addToJsonArrayObj(self, a):
        if not self.jsonArrayObj:
            self.jsonArrayObj.append(a)
        else:
            self.jsonArrayObj.append(a)
    def addToJsonDictObj(self, k, v):
        if k not in self.jsonArrayObj:
            self.jsonDictObj[k] = v
        else:
            self.jsonDictObj[k] = v
    def addToJsonArrayObj_extend(self, itm, l):
        if itm not in self.jsonArrayObj:
            return None # important: use checkFor methods
        else:
            jArray = self.jsonArrayObj
            jArray = [l if x == itm else x for x in jArray]
            self.jsonArrayObj = jArray
    def addToJsonDictObj_extend(self, k, v):
        if k not in self.jsonDictObj:
            return None
        else:
            d = self.jsonDictObj
            d[k] = v
            self.jsonDictObj = d
    def checkForTopLevelKey(self, k):
        if k in self.jsonDictObj:
            return True
        else:
            return False
    def checkForTopLevelListItem(self, itm):
        if itm in self.jsonArrayObj:
            return True
        else:
            return False

def selectElements(h):
    inputEntered = 0
    retList = []
    p = re.compile('ALL')
    pHash = re.compile('#')
    while not inputEntered:
        print("\nHere is the header from your file\n")
        print(h)
        print("\n")
        print("Please enter the 0-based index of the elements that you'd like to use\n\nTo select all elements from the header, enter \"ALL#\"\n\nTo enter an element as a child element of another element, enter the indexes with a \"#\"\n\nTo select more than one, use a comma to separate the numbers.")
        print("\nFor example:\n1,2#3,4\n\nwill produce a structure using Hashes of\n1:{n,n,n}\n2:{n,3:{n,n,n},n}\n4:{n,n}\n")
        idx = input("-> ")
        idx = idx.rstrip('\r\n')
        idxList = idx.split(',')
        for i in idxList:
            m = re.search(p, i)
            if m:
                return (1, [-1]) # input is ALL#, use entire header
        if (len(idxList) == 1):
            m = re.search(pHash, idx)
            if m:
                idx_pchild = idx.split('#')
                pchild_parent = int(idx_pchild[0])
                pchild_child = int(idx_pchild[1])
                retList.append((pchild_parent, pchild_child))
                return (0, retList) # use a single parent-child relationship
            if idx:
                idx = int(idx)
                retList.append(idx)
                return (1, retList) # use a single item
            else:
                print("Sorry, your input was not recognized.  Please re-enter!")
        else:
            pchild = False
            for i in idxList: # list of integers specified
                m = re.search(pHash, i)
                if m:
                    pchild = True
                    itmList_pchild = i.split('#')
                    pchild_parent = int(itmList_pchild[0])
                    pchild_child = int(itmList_pchild[1])
                    retList.append((pchild_parent, pchild_child))
                else:
                    idxVal = int(i)
                    retList.append((-1, idxVal)) # -1 is non parent-child flag
            if not pchild:
                return (0, retList)
                # list of items
                # at least one instance of parent-child relationship
            else:
                return (1, retList)
                # list of items
                # no parent-child relationships
    return None
def selectedElements(c1, c2, resList, checkHdLine):
    retList = []
    p_c_Dict = {}
    if c1 == 1:
        if c2 == 1:
            if resList[0] != -1:
                return resList
            else:
                for i,j in enumerate(checkHdLine):
                    retList.append(j)
                    return retList
        else:
            return resList
    else:
        if c2 == 1:
            d = {}
            int_k = resList[1][0]
            int_v = resList[1][1]
            str_k = checkHdLine[int_k]
            str_k_k_v = checkHdLine[int_v]
            d[str_k_k_v] = '-1'
            p_c_Dict[str_k] = d
            retList.append(p_c_Dict)
            return retList
        else:
            resList_parse = resList[1]
            for i in resList_parse:
                if i[0] == -1:
                    str_k = checkHdLine[i[1]]
                    str_v = '-1'
                    p_c_Dict[str_k] = str_v
                else:
                    str_k = checkHdLine[i[0]]
                    str_k_k_v = str_v = checkHdLine[i[1]]
                    d = {}
                    d[str_k_k_v] = '-1'
                    p_c_Dict[str_k] = d
            retList.append(p_c_Dict)
            return retList

def findItm(lst, x):
    # credit Martijn Pieters StackExchange
    r = []
    for i, j in enumerate(lst):
        # if j < x or j > y: lt or gt
        if j == x:
            r.append(i)
    return r # def find(lst, a, b):
                #   return [i for i, x in enumerate(lst) if x < a or x > b]


l = []
with open('/Users/thor/Documents/tmp4json.csv') as f:
  for i in f:
    i = i.rstrip('\r\n')
    l.append(i)
j = jsonObj()
headerLine = l.pop(0)
jsonDict = {}
jsonArray = []
jsonAsDictTopLevel = False
jsonTopLevelDictKey = ""
topLevelEntered = 0
while not topLevelEntered:
    print("Would you like an array, or a dictionary, for the top level of your json file?  Type \"dict\" for a dictionary, \"array\" for an array, or \"exit\" to exit")
    startInput = input("-> ")
    startInput = startInput.rstrip('\r\n')
    startInput = startInput.upper()
    if startInput == 'DICT':
        jsonAsDictTopLevel = True
        while True:
            print("Please enter a name for the top level of the json file.")
            jInput = input(" -> ")
            jInput = jInput.rstrip('\r\n')
            jsonTopLevelDictKey = jInput
            if jsonTopLevelDictKey:
                topLevelEntered = 1
                j.addToJsonDictObj(jsonTopLevelDictKey, '-1')
                break
            else:
                print("Sorry, the name you entered did not seem to be valid.")
    elif startInput == 'ARRAY':
        jsonAsDictTopLevel = False
        topLevelEntered = 1
    elif startInput == 'EXIT':
        print("Exiting...")
        sys.exit()
    else:
        print("Error, your command was not recognized, please try again!")
        time.sleep(2)

while True:
    tmpLine = l[0]
    checkHeaderLine = headerLine.split(',')
    checkFirstLine = tmpLine.split(',')
    print("Header is")
    print(checkHeaderLine)
    if (len(checkHeaderLine) != len(checkFirstLine)):
        print("It looks like the header may not be aligned to the rest of your data!\nPlease check the dataset and relaunch the program.")
        print(checkHeaderLine)
        print(len(checkHeaderLine))
        print(checkFirstLine)
        print(len(checkFirstLine))
        sys.exit()
    rList = selectElements(headerLine)
    rListVals = []
    check2 = len(rList[1])
    check1 = rList[0] # will always be a single integer
    rListVals = selectedElements(check1, check2, rList, checkHeaderLine) # will always return a list
    print("\n\nHow would you like the next level of your json organized? Type \"dict\" for a dictionary, \"array\" for an array, \"header\" to see the header again, or \"exit\" to exit")
    firstInput = input("-> ")
    firstInput = firstInput.rstrip('\r\n')
    firstInput = firstInput.upper()
    d = {}
    if firstInput == 'DICT':
        if not jsonAsDictTopLevel:
            print("Array top level, Dict next level")
            jsonOrganization = rListVals[0]
            jList = []
            jDict = {}
            if isinstance(jsonOrganization, list):
                jList = jsonOrganization
                for i in jList:
                    k = checkHeaderLine[i]
                    v = checkFirstLine[i]
                    d[k] = v
                j.addToJsonArrayObj(d)
                tmpJson = j.returnObj('array')
                print(json.dumps(tmpJson, sort_keys=True, indent=4))
                thirdInput = input("Here is a preview of the json file.  Continue adding? [Y/N] -> ")
                thirdInput = thirdInput.rstrip('\r\n')
                thirdInput = thirdInput.upper()
                if thirdInput == 'N':
                    # current format is [d]
                    print("output is")
                    print(json.dumps(tmpJson, sort_keys=True, indent=4))
                    break
                else:
                    print("Restarting json parse")
                    continue
            elif isinstance(jsonOrganization, dict):
                jDict = jsonOrganization
                for k,v in jDict.items():
                    if v == '-1': # WARNING!!  If value != -1 or a dict{} this WILL cause a crash.
                        if k in checkHeaderLine:
                            v_idx_l = findItm(checkHeaderLine, k)
                            v_idx = v_idx_l.pop(0)
                            d[k] = checkFirstLine[v_idx]
                            j.addToJsonArrayObj(d)
                        else:
                            print("Error, key did not match Header.  Please check json key-values")
                            print(checkHeaderLine)
                            print(jDict)
                            sys.exit()
                    else:
                        t_dict = v
                        for k1,v1 in t_dict.items():
                            if v1 != -1:
                                print("Sorry, only one level of recursion is currently supported.\nPlease re-enter values.")
                                time.sleep(2)
                                continue
                            else:
                                v_idx_l = findItm(checkHeaderLine, k1)
                                v_idx = v_idx_l.pop(0)
                                k1_val = checkFirstLine[v_idx]
                                d[k] = {k1 : k1_val}
                                j.addToJsonArrayObj(d)
            else:
                print("Error, check json organization structure")
                print(rListVals)
                print(jsonOrganization)
                sys.exit()
            tmpJson = j.returnObj('array')
            print(json.dumps(tmpJson, sort_keys=True, indent=4))
            thirdInput = input("Here is a preview of the json file.  Continue adding? [Y/N] -> ")
            thirdInput = thirdInput.rstrip('\r\n')
            thirdInput = thirdInput.upper()
            if thirdInput == 'N':
                # current format is [d]
                print("output is")
                print(json.dumps(tmpJson, sort_keys=True, indent=4))
                break
            else:
                print("Restarting json parse")
                continue
        else:
            jsonOrganization = rListVals[0]
            jList = []
            jDict = {}
            if isinstance(jsonOrganization, list):
                jList = jsonOrganization
                j_dict = {}
                for i in jList:
                    k = checkHeaderLine[i]
                    v = checkFirstLine[i]
                    j_dict[k] = v
                j.addToJsonDictObj(jsonTopLevelDictKey, j_dict)
                tmpJson = j.returnObj('dict')
                print(json.dumps(tmpJson, sort_keys=True, indent=4))
                thirdInput = input("Here is a preview of the json file.  Continue adding? [Y/N] -> ")
                thirdInput = thirdInput.rstrip('\r\n')
                thirdInput = thirdInput.upper()
                if thirdInput == 'N':
                    # current format is [d]
                    print("output is")
                    print(json.dumps(tmpJson, sort_keys=True, indent=4))
                    break
                else:
                    print("Restarting json parse")
                    continue
            elif isinstance(jsonOrganization, dict):
                jDict = jsonOrganization
                for k,v in jDict.items():
                    if v == '-1': # WARNING!!  If value != -1 or a dict{} this WILL cause a crash.
                        if k in checkHeaderLine:
                            v_idx_l = findItm(checkHeaderLine, k)
                            v_idx = v_idx_l.pop(0) # for current release, only supports the first value
                            d[k] = checkFirstLine[v_idx]
                            j.addToJsonDictObj(jsonTopLevelDictKey, d)
                        else:
                            print("Error, key did not match Header.  Please check json key-values")
                            print(checkHeaderLine)
                            print(jDict)
                            sys.exit()
                    else:
                        t_dict = v
                        for k1,v1 in t_dict.items():
                            if v1 != -1:
                                print("Sorry, only one level of recursion is currently supported.\nPlease re-enter values.")
                                time.sleep(2)
                                continue
                            else:
                                v_idx_l = findItm(checkHeaderLine, k1)
                                v_idx = v_idx_l.pop(0)
                                k1_val = checkFirstLine[v_idx]
                                d[k] = {k1 : k1_val}
                                j.addToJsonDictObj(jsonTopLevelDictKey, d)
            else:
                print("Error, check json organization structure")
                print(rListVals)
                print(jsonOrganization)
                sys.exit()
            tmpJson = j.returnObj('dict')
            print(json.dumps(tmpJson, sort_keys=True, indent=4))
            thirdInput = input("Here is a preview of the json file.  Continue adding? [Y/N] -> ")
            thirdInput = thirdInput.rstrip('\r\n')
            thirdInput = thirdInput.upper()
            if thirdInput == 'N':
                # current format is [d]
                print("output is")
                print(json.dumps(tmpJson, sort_keys=True, indent=4))
                break
            else:
                print("Restarting json parse")
                continue
    elif firstInput == 'ARRAY':
        jsonArray = []
        if not jsonAsDictTopLevel:
            print("Array top level, Array next level")
            jsonOrganization = rListVals[0]
            jList = []
            jDict = {}
            if isinstance(jsonOrganization, list):
                jList = jsonOrganization
                for i in jList:
                    k = checkHeaderLine[i]
                    j.addToJsonArrayObj(k)
                tmpJson = j.returnObj('array')
                print(json.dumps(tmpJson, sort_keys=True, indent=4))
                thirdInput = input("Here is a preview of the json file.  Continue adding? [Y/N] -> ")
                thirdInput = thirdInput.rstrip('\r\n')
                thirdInput = thirdInput.upper()
                if thirdInput == 'N':
                    # current format is [d]
                    print("output is")
                    print(json.dumps(tmpJson, sort_keys=True, indent=4))
                    break
                else:
                    print("Restarting json parse")
                    continue
            elif isinstance(jsonOrganization, dict):
                jDict = jsonOrganization
                dict_to_add = {}
                for k,v in jDict.items():
                    if v == '-1': # WARNING!!  If value != -1 or a dict{} this WILL cause a crash.
                        if k in checkHeaderLine:
                            j.addToJsonArrayObj(k)
                        else:
                            print("Error, key did not match Header.  Please check json key-values")
                            print(checkHeaderLine)
                            print(jDict)
                            sys.exit()
                    else:
                        t_dict = v
                        for k1,v1 in t_dict.items():
                            if v1 != -1:
                                print("Sorry, only one level of recursion is currently supported.\nPlease re-enter values.")
                                time.sleep(2)
                                continue
                            else:
                                v_idx_l = findItm(checkHeaderLine, k1)
                                v_idx = v_idx_l.pop(0)
                                k1_val = checkFirstLine[v_idx]
                                j.addToJsonArrayObj_extend(k1, k1_val)
            else:
                print("Error, check json organization structure")
                print(rListVals)
                print(jsonOrganization)
                sys.exit()
            tmpJson = j.returnObj('array')
            print(json.dumps(tmpJson, sort_keys=True, indent=4))
            thirdInput = input("Here is a preview of the json file.  Continue adding? [Y/N] -> ")
            thirdInput = thirdInput.rstrip('\r\n')
            thirdInput = thirdInput.upper()
            if thirdInput == 'N':
                # current format is [d]
                print("output is")
                print(json.dumps(tmpJson, sort_keys=True, indent=4))
                break
            else:
                print("Restarting json parse")
                continue
        else:
            print("Dict top level, Array next level")
            jsonOrganization = rListVals[0]
            jList = []
            jDict = {}
            t_list = []
            if isinstance(jsonOrganization, list):
                jList = jsonOrganization
                for i in jList:
                    k = checkHeaderLine[i]
                    t_list.append(k)
                j.addToJsonDictObj(jsonTopLevelDictKey, t_list)
                tmpJson = j.returnObj('dict')
                print(json.dumps(tmpJson, sort_keys=True, indent=4))
                thirdInput = input("Here is a preview of the json file.  Continue adding? [Y/N] -> ")
                thirdInput = thirdInput.rstrip('\r\n')
                thirdInput = thirdInput.upper()
                if thirdInput == 'N':
                    # current format is [d]
                    print("output is")
                    print(json.dumps(tmpJson, sort_keys=True, indent=4))
                    break
                else:
                    print("Restarting json parse")
                    continue
            elif isinstance(jsonOrganization, dict):
                jDict = jsonOrganization
                jsonList4Array = []
                for k,v in jDict.items():
                    if v == '-1': # WARNING!!  If value != -1 or a dict{} this WILL cause a crash.
                        if k in checkHeaderLine:
                            jsonList4Array.append(k)
#                            v_idx_l = findItm(checkHeaderLine, k)
#                            v_idx = v_idx_l.pop(0)
#                            k1_val = checkFirstLine[v_idx]
                            # j.addToJsonDictObj(k, k1_val)
#                            j.addToJsonDictObj()
                        else:
                            print("Error, key did not match Header.  Please check json key-values")
                            print(checkHeaderLine)
                            print(jDict)
                            sys.exit()
                    else:
                        t_dict = v
                        for k1,v1 in t_dict.items():
                            if v1 != -1:
                                print("Sorry, only one level of recursion is currently supported.\nPlease re-enter values.")
                                time.sleep(2)
                                continue
                            else:
                                v_idx_l = findItm(checkHeaderLine, k1)
                                v_idx = v_idx_l.pop(0)
                                k1_val = checkHeaderLine[v_idx]
                                k1_val = list(k1_val)
                                jsonList4Array = [k1_val if k1 == v_idx else x for x in jsonList4Array]
#                                j.addToJsonArrayObj_extend(k1, k1_val)
                j.addToJsonDictObj(jsonTopLevelDictKey, jsonList4Array)
            else:
                print("Error, check json organization structure")
                print(rListVals)
                print(jsonOrganization)
                sys.exit()
            tmpJson = j.returnObj('dict')
            print(json.dumps(tmpJson, sort_keys=True, indent=4))
            secondInput = input("Here is a preview of the json file.  Continue? [Y/N] -> ")
            secondInput = secondInput.rstrip('\r\n')
            secondInput = secondInput.upper()
            if secondInput == 'N':
                # current format is {l[0]} as jsonArray
                print("output is")
                print(json.dumps(tmpJson, sort_keys=True, indent=4))
                break
    elif firstInput == 'EXIT':
        print("Exiting...")
        time.sleep(1)
        sys.exit()
    else:
        print("Sorry, the command was not recognized.  Please retry!")
        time.sleep(1)
