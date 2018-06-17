import xml.etree.ElementTree as ET
import copy
#from lxml import etree as lxmletree
from xml.dom import minidom as minidom
from natsort import natsorted, ns

WRITE_FILE_NAME = "../src/filename.xml"

ET.register_namespace('', "http://soap.sforce.com/2006/04/metadata")
tree = ET.parse('../src/package.xml')
root = tree.getroot()
writeRoot = copy.deepcopy(root)
for elem in writeRoot:
    if 'types' in elem.tag:
        elem.clear()

membersDict={}
for elem in root:
    membersSet = set([])
    for subelem in  elem :
        if('members' in subelem.tag):
            membersSet.add(subelem.text)
        elif('name' in subelem.tag):
            membersDict[subelem.text] = membersSet
            break

writeList = []
for key in membersDict:
    innerList = natsorted(membersDict[key], alg=ns.IGNORECASE)  
    #innerList = sorted(membersDict[key])
    innerList.append(key)
    writeList.append(innerList)

#for innerList in writeList:
#    print(innerList)

index =0
for elem in writeRoot:
    if 'types' in elem.tag:
        print('****** index {}'.format(index))
        innerList = writeList[index]

        for index2 in range(0, len(innerList)):
            if(index2 == len(innerList)-1):
                name = elem.makeelement('name',{})
                name.text = innerList[len(innerList)-1]
                elem.append(name)
            else:
                members = elem.makeelement('members',{})
                members.text = innerList[index2]
                elem.append(members)
    index+=1

writeTree = ET.ElementTree(writeRoot)
#writeTree.write('check.xml',encoding="utf-8",xml_declaration=True)

# # Prettyfy 1
# parser = lxmletree.XMLParser(remove_blank_text=True)
# prettyTree = lxmletree.parse(WRITE_FILE_NAME, parser)
# prettyTree.write(WRITE_FILE_NAME, pretty_print=True, encoding="utf-8",xml_declaration=True, indent='\t')


xmldoc = minidom.parseString(ET.tostring(writeRoot))
xmldoc.writexml( 
    open(WRITE_FILE_NAME, 'w'),
        indent="",
        addindent="    ",
        encoding="utf-8",
        newl='\n')

# with open(WRITE_FILE_NAME, "w") as f:
#      f.write(xmlstr)


