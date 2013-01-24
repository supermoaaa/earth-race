# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~ TileTex 5in1          2002 by Doc Holiday ~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Web:	http://Project.Blender.onlinehome.de
# Mail:	Project.Blender@online.de
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Function Summing:
# =================

# Implicit Propertys
# ------------------
# String-Matrix	  - Dimensions of the Texture
#					in Frames (2x4;5x1...)

# Modes
# -----
# Mode 0	- Linear
# Mode 1	- Reverse
# Mode 2	- Ping Pong
# Mode 3	- Set Frame direct
#			  (need Property Int-DFrame)
# Mode 4	- Set Random Frame

# Extra Propertys
# ---------------
# Int-StartAt	- if StartFrame ist NOT 0
# Int-Wait	- set Waitloops
# Int-Play	- set Payloops
# Int-CurrMtxLoc	- reads current Frame
# Int-Sleep	- reads the 'Sleep Time'
#			  (if using Waitloops)
# Int-Part	- Set the Meshpart to animate
#			  (Experimental! Use with care!)

# ==--==--==-- Have fun! --==--==--==--==--==--==

# Changed by HG1 to Blender 2.49b and Blender 2.5x 20.09.2011
# Changed by Moaaa for blender 2.6x

def setMtx(Own, Mesh, MtxL):
	CurrLoc = (Own["CurrMtxLoc"]-floor(Own["CurrMtxLoc"]/Own["MtxX"])*Own["MtxX"],floor(Own["CurrMtxLoc"]/Own["MtxX"]))
	NewLoc = (MtxL-floor(MtxL/Own["MtxX"])*Own["MtxX"],floor(MtxL/Own["MtxX"]))
	if Own["Part"] < Own["MatCount"]:
		if Own["Part"] == -1: CS,CE = (0,Own["MatCount"])
		else: CS,CE = (Own["Part"],Own["Part"]+1)
		for Mat in range(CS,CE):
			Mlen = Mesh.getVertexArrayLength(Mat)
			for Vi in range(0,Mlen):
				Vertex = Mesh.getVertex(Mat,Vi)
				uv = Vertex.getUV()
				uv[0] = (uv[0]-CurrLoc[0]*1.0/Own["MtxX"]) + NewLoc[0]*1.0/Own["MtxX"]
				uv[1] = (uv[1]-CurrLoc[1]*1.0/Own["MtxY"]) + NewLoc[1]*1.0/Own["MtxY"]
				Vertex.setUV(uv)
				Vi += 1
		Own["CurrMtxLoc"] = MtxL
	else: print ("** WARNING: Part overflow! **")

# ===================================================

from bge import logic as GL
from math import *

def setUv():
	Cont = GL.getCurrentController()
	Own = Cont.owner
	Mesh = Own.meshes[0]
	Sens = Cont.sensors[0]

	# Timer zuruecksetzen
	# ~~~~~~~~~~~~~~~~~~~
	Own["Speed"] = 0

	# finde Matrix und setzte Start Variablen
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	if "NL" not in Own:
		Own["MtxX"] = int(Own["Matrix"].split("x")[0])
		Own["MtxY"] = int(Own["Matrix"].split("x")[1])

		# ~~~~~~~~~~~ Settings
		Own["First"] = 1
		if "Mode" not in Own:
			Own["Mode"] = 0
		if "StartAt" in Own:
			Own["CurrMtxLoc"] = Own["StartAt"]
		else:
			Own["CurrMtxLoc"] = 0
		Own["NL"] = 0
		Own["Sleep"] = 0
		if "Play" not in Own:
			Own["Play"] = -1
		if "Part" not in Own:
			Own["Part"] = -1
		Own["MatCount"] = Mesh.numMaterials

	# verarbeite Sleep- & PlayLoops
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	if Sens.positive and not Own["CurrMtxLoc"] and Own["Mode"] <=2 and not Own["First"]:
		if Own["Sleep"]:
			Own["Sleep"] -= 1
		else:
			if Own["Play"] > 0:
				Own["Play"] -= 1
			if not Own["Play"]:
				Own["First"] = 1
			if "Wait" in Own and not Own["First"]:
				Own["Sleep"] = Own["Wait"]


	# verarbeite AnimationsModus
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~
	if Sens.positive and not Own["Sleep"] and Own["Play"]:
		Own["First"] = 0
		if not Own["Mode"]: # ------------------------------ >> Mode 0 << - Linear
			Own["NL"] += 1
			if Own["NL"] == Own["MtxX"]*Own["MtxY"]: Own["NL"] = 0
			setMtx(Own, Mesh, Own["NL"])
			Own["PPR"] = 1

		elif Own["Mode"] == 1: # --------------------------- >> Mode 1 << - Linear Reverse
			Own["NL"] -= 1
			if Own["NL"] == -1: Own["NL"] = Own["MtxX"]*Own["MtxY"]-1
			setMtx(own, Mesh, Own["NL"])
			Own["PPR"] = 0

		elif Own["Mode"] == 2: # --------------------------- >> Mode 2 << - Ping Pong
			if "PPR" not in Own:
				Own["PPR"] = 1
			if Own["PPR"]:
				Own["NL"] += 1
				if Own["NL"] == Own["MtxX"]*Own["MtxY"]:
					Own["NL"] -= 2
					Own["PPR"] = 0
				setMtx(Own, Mesh, Own["NL"])
			else:
				Own["NL"] -= 1
				if Own["NL"] == -1:
					Own["NL"] += 2
					Own["PPR"] = 1
				setMtx(Own, Mesh, Own["NL"])

		elif Own["Mode"] == 3: # --------------------------- >> Mode 3 << - Set Frame
			if "DFrame" not in Own:
				print ("** WARNING: Integer-DFrame Property missing. **")
			else:
				if Own["DFrame"] > Own["MtxX"]*Own["MtxY"]-1 or Own["DFrame"] < 0:
					print ("** WARNING: Wrong DFrame Value! **")
				elif Own["DFrame"] != Own["CurrMtxLoc"]:
					setMtx(Own, Mesh, Own["DFrame"])

		elif Own["Mode"] == 4: # --------------------------- >> Mode 4 << - Random Frame
			while Own["NL"] == Own["CurrMtxLoc"]:
				Own["NL"] = floor(Own["MtxX"]*Own["MtxY"]*GL.getRandomFloat())
			setMtx(Own, Mesh, Own["NL"])
