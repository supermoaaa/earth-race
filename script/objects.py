from bge import logic as gl

def libLoad( filePath, dataType, **args ):
	try:
		if filePath not in gl.LibList():
			gl.LibLoad( filePath, dataType, **args )
	except:
		print("impossible d'ouvrir le fichier "+filePath)
		print("heu… ben ça vas faire un bordel monstre")

def libList():
	return gl.LibList()

def libFree( filePath ):
	if filePath in gl.LibList():
			gl.LibFree( filePath )

def addObject( pos_ob, objectName ):
	try:
		scene = gl.getCurrentScene()
		child = scene.addObject( objectName, pos_ob, 0 )
		print('objet ajouté : ',child)
		print('-------------------')
		return child
	except:
		print("objet \""+objectName+"\" non trouvé")
		return None

def copyRelatifOrientation(pos_ob, objectTarget, mainObject):
	objectName = objectTarget.name
	modelPiece = gl.getCurrentScene().objects.get(objectName)
	newOri = pos_ob.orientation.to_quaternion()
	mainOri = mainObject.orientation.copy().to_quaternion()
	modelOri = modelPiece.orientation.copy().to_quaternion()
	newOri.rotate(mainOri.rotation_difference(modelOri))
	print('orientation : ', objectTarget.orientation)
	objectTarget.orientation = newOri.to_matrix()
	print('orientation : ', objectTarget.orientation)

def copyRelatifPosition(pos_ob, objectTarget, mainObject):
	objectName = objectTarget.name
	modelPiece = gl.getCurrentScene().objects.get(objectName)
	objectTarget.position = applyVectDifftoVect( mainObject.position, modelPiece.position, list(pos_ob.position) )

def copyRelatifScale(pos_ob, objectTarget, mainObject):
	objectName = objectTarget.name
	modelPiece = gl.getCurrentScene().objects.get(objectName)
	objectTarget.scaling = applyVectDifftoVect( mainObject.scaling, modelPiece.scaling, list(pos_ob.scaling) )

def applyVectDifftoVect( vect1, vect2, vect3 ):
	x = vect3[0]+vect2[0]-vect1[0]
	y = vect3[1]+vect2[1]-vect1[1]
	z = vect3[2]+vect2[2]-vect1[2]
	return (x,y,z)
