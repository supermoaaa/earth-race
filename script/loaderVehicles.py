from bge import logic as gl
import xml.dom.minidom as minidom
import sys
sys.path.append(gl.expandPath("//")+'script')
from xmlHelper import getText
import vehicle

def addVehicleLoader( source, vehicleType, wheelsType, keys ):
	scene = gl.getCurrentScene()
	child = scene.addObject( source, source, 1 )
	child['id']=source['id']+1
	child['vehicleType']=vehicleType
	child['wheelsType']=wheelsType
	child['keys']=keys
	try:
		gl.cars.append([child['id'],child])
	except :
		gl.cars=[[child['id'],child]]
	print(child.get('id'))

def load():
	own = gl.getCurrentController().owner
	if own['id']==0:
		vehicles = []
		wheels = []
		propertieFile = minidom.parse(gl.expandPath("//")+"players.xml")
		for player in propertieFile.getElementsByTagName("player") :
			vehicleType = player.getElementsByTagName("vehicle")[0]
			wheelsType = player.getElementsByTagName("wheels")[0]
			addVehicleLoader( own, getText(vehicleType), getText(wheelsType), [] )
	else:
		print(own['vehicleType'])
		print(own['wheelsType'])
		car = vehicle.vehicleSimulation( own['vehicleType'], own['wheelsType'], own['keys'] )
