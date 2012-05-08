import xml.dom.minidom as minidom

def getText(nodelist):
	rc = []
	for node in nodelist.childNodes:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

def listChilds(node):
	pass
