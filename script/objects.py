from bge import logic as gl
import logs


def libLoad(filePath, dataType, **args):
	try:
		if filePath not in gl.LibList():
			gl.LibLoad(filePath, dataType, **args)
	except:
		logs.log("error", "impossible d'ouvrir le fichier " + filePath)
		logs.log("error", "heu… ben ça vas faire un bordel monstre")


def libList():
	return gl.LibList()


def libFree(filePath):
	if filePath in gl.LibList():
			gl.LibFree(filePath)


def addObject(pos_ob, objectName, creator=None):
	try:
		scene = gl.getCurrentScene()
		child = scene.addObject(objectName, pos_ob, 0)
		logs.log("debug", 'objet ajouté : ' + str(child))
		logs.log("debug", '-------------------')
		if creator is not None:
			child['creator'] = creator
			for ob in child.childrenRecursive:
				ob['creator'] = creator
		logs.log('debug', 'creator : ' + str(creator))
		return child
	except:
		logs.log("error", "objet \"" + objectName + "\" non trouvé")
		return None


def copyRelatifOrientation(pos_ob, objectTarget, mainObject):
	objectName = objectTarget.name
	modelPiece = gl.getCurrentScene().objects.get(objectName)
	newOri = pos_ob.orientation.to_quaternion()
	mainOri = mainObject.orientation.copy().to_quaternion()
	modelOri = modelPiece.orientation.copy().to_quaternion()
	newOri.rotate(mainOri.rotation_difference(modelOri))
	logs.log("debug", 'orientation : ', objectTarget.orientation)
	objectTarget.orientation = newOri.to_matrix()
	logs.log("debug", 'orientation : ', objectTarget.orientation)


def copyRelatifPosition(pos_ob, objectTarget, mainObject):
	objectName = objectTarget.name
	modelPiece = gl.getCurrentScene().objects.get(objectName)
	objectTarget.position = applyVectDifftoVect(
			mainObject.position, modelPiece.position, list(pos_ob.position))


def copyRelatifScale(pos_ob, objectTarget, mainObject):
	objectName = objectTarget.name
	modelPiece = gl.getCurrentScene().objects.get(objectName)
	objectTarget.scaling = applyVectDifftoVect(
			mainObject.scaling, modelPiece.scaling, list(pos_ob.scaling))


def applyVectDifftoVect(vect1, vect2, vect3):
	x = vect3[0] + vect2[0] - vect1[0]
	y = vect3[1] + vect2[1] - vect1[1]
	z = vect3[2] + vect2[2] - vect1[2]
	return (x, y, z)
