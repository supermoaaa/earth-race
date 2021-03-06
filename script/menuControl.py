from menugui import *
from os import chdir, getcwd, sep

chdir(gl.expandPath("//"))
cont = gl.getCurrentController()
own = cont.owner

####viewport 2 joueurs
def viewportDeuxDivision(playerCams, mode):

        width = rd.getWindowWidth()
        height = rd.getWindowHeight()

        #vertical
        if mode == 2:

                # Player 1 viewport: left side
                left_1 = 0; bottom_1 = 0; right_1 = width/2; top_1 = height

                #  Player 2 viewport: right side
                left_2 = width/2; bottom_2 = 0; right_2 = width; top_2 = height

        #horizontal
        else:
                # Player 1 viewport: top half
                left_1 = 0; bottom_1 = height/2; right_1 = width; top_1 = height

                #  Player 2 viewport: bottom half
                left_2 = 0; bottom_2 = 0; right_2 = width; top_2 = height/2


        playerCams[0].setViewport( int(left_1), int(bottom_1), int(right_1), int(top_1))
        playerCams[1].setViewport( int(left_2), int(bottom_2), int(right_2), int(top_2))
        playerCams[0].useViewport = playerCams[1].useViewport = True

####viewport 3 et 4 joueurs
def viewportQuatreDivision(playerCams):

        width = rd.getWindowWidth()
        height = rd.getWindowHeight()


        # Player 1 viewport:  top left side
        left_1 = 0; bottom_1 = height/2; right_1 = width/2; top_1 = height

        #  Player 2 viewport: top right side
        left_2 = width/2; bottom_2 = height/2; right_2 = width; top_2 = height


        # Player 3 viewport: top half
        left_3 = 0; bottom_3 = 0; right_3 = width/2; top_3 = height/2

        #  Player 4 viewport: bottom half
        left_4 = width/2; bottom_4 = 0; right_4 = width; top_4 = height/2

        playerCams[0].setViewport( int(left_1), int(bottom_1), int(right_1), int(top_1))
        playerCams[1].setViewport( int(left_2), int(bottom_2), int(right_2), int(top_2))
        playerCams[2].setViewport( int(left_3), int(bottom_3), int(right_3), int(top_3))
        playerCams[3].setViewport( int(left_4), int(bottom_4), int(right_4), int(top_4))
        playerCams[0].useViewport = playerCams[1].useViewport = playerCams[2].useViewport = playerCams[3].useViewport = True

def setCam (cam):
	gl.getCurrentScene().active_camera = gl.getCurrentScene().objects[cam]

def main (self):
	#print(gl.status)
	own['sys'].main()
	own['fond'].main()
	scene = gl.getCurrentScene()

	if not own["fond"].ouvert :
		sys = own["fond"]
	else :
		sys = own["sys"]

	if not sys.ouvert :
		if gl.status == "MenuPrincipal" :
			if sys.action == "retour" :
				gl.endGame()
			elif sys.action == "joueurSolo" :
				own["sys"] = jouerSoloGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				own["fond"].frame.img.visible = False
				gl.status = "MenuselectionVoiture1J"

				gl.dispPlayers[0] = 0
				gl.LibLoad('//'+  "carSelect.blend", "Scene")
				setCam ('CameraPlayer1')
				gl.colorCar1 = scene.addObject("color ramp", "car1")
				gl.colorGlass1 = scene.addObject("color ramp", "glass1")

				own["sys"].voiture_label.text = str(gl.conf[0][0][3])
				own["sys"].roue_label.text = str(gl.conf[0][0][4])
				gl.voiture = vehicleLinker(posObj = scene.objects['carpos1'], physic = False, parent = True)
				gl.voiture.setVehicle( str(gl.conf[0][0][3]) )
				gl.voiture.setWheels( str(gl.conf[0][0][4]) )
				gl.voiture.setVehicleColor(*gl.conf[0][0][5])
				gl.voiture.setWindowsColor(*gl.conf[0][0][6])



			elif sys.action == "MenuMultijoueurs" :
				own["sys"] = MenuMultijoueursGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuMultijoueurs"

			elif sys.action == "MenuTelechargement" :
				own["sys"] = MenuTelechargementGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuTelechargement"

			elif sys.action == "MenuOptions" :
				own["sys"] = MenuOptionsGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuOptions"

		elif gl.status == "MenuselectionVoiture1J" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuPrincipalGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Quitter"
				own["fond"].frame.img.visible = True
				gl.status = "MenuPrincipal"
				setCam ('CamMenu')
				gl.colorCar1.endObject()
				gl.colorGlass1.endObject()
				del gl.colorCar1, gl.colorGlass1

				try:
					for lib in gl.LibList():
						gl.LibFree(lib)
				except:
					pass
				logs.log("info", gl.LibList())

				if hasattr(gl , 'voiture'):
					del gl.voiture

			elif sys.action == "MenuSelectionCircuit" :
				own["sys"] = MenuSelectionCircuitGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				own["fond"].frame.img.visible = True
				own["sys"].gPosJoueur1.img.texco = [(0,0.5), (0.5,0.5), (0.5,1), (0,1)]
				gl.status = "MenuSelectionCircuit"
				try:
					for lib in gl.LibList():
						gl.LibFree(lib)
				except:
					pass
				logs.log("info", gl.LibList())

				print(gl.LibList())
				if hasattr(gl , 'voiture'):
					del gl.voiture


		elif gl.status == "MenuMultijoueurs" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuPrincipalGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Quitter"
				gl.status = "MenuPrincipal"

			elif sys.action == "MenuEcranSpliter" :
				own["sys"] = MenuEcranSpliterGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.dispPlayers.append(gl.conf[0][1][0])
				gl.status = "MenuEcranSpliter"
				gl.dispPlayers[0] = 1

		elif gl.status == "MenuTelechargement" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuPrincipalGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Quitter"
				gl.status = "MenuPrincipal"

		elif gl.status == "MenuSelectionCircuit" :
			if sys.action == "retour" :
				if gl.dispPlayers[0] == 0:
					own["sys"].detruire()
					own["sys"] = jouerSoloGui(own["fond"].frame)
					own["fond"].reinit()
					own["fond"].retour_label.text = "Retour"
					own["fond"].frame.img.visible = False
					gl.status = "MenuselectionVoiture1J"

					gl.LibLoad('//'+"carSelect.blend", "Scene")
					setCam ('CameraPlayer1')
					own["sys"].voiture_label.text = str(gl.conf[0][0][3])
					own["sys"].roue_label.text = str(gl.conf[0][0][4])
					gl.voiture = vehicleLinker(posObj = scene.objects['carpos1'], physic = False, parent = True)
					gl.voiture.setVehicle( str(gl.conf[0][0][3]) )
					gl.voiture.setWheels( str(gl.conf[0][0][4]) )
					gl.voiture.setVehicleColor(*gl.conf[0][0][5])
					gl.voiture.setWindowsColor(*gl.conf[0][0][6])

			if sys.action == "depart" :
				confParser.savePlayer()
				scene = gl.getCurrentScene()
				for lib in gl.LibList():
					gl.LibFree(lib)

				scene.replace('game')

		elif gl.status == "MenuOptions" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuPrincipalGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Quitter"
				gl.status = "MenuPrincipal"

			elif sys.action == "Affichage" :
				own["sys"] = MenuAffichageGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuAffichage"

			elif sys.action == "joueurs" :
				own["sys"] = MenuNomsJoueursGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuJoueurs"

			elif sys.action == "son" :
				own["sys"] = MenuOptionsSon(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				own["fond"].frame.img.visible = False
				gl.fondSon = scene.addObject("fondSon", "soundPos")
				gl.cadreSon = scene.addObject("cadreSon", "soundPos")
				gl.curseurSon = scene.addObject("cursor", "soundPos")
				gl.barreVSon = scene.addObject("verticalBarre", "soundPos")
				gl.barreHSon = scene.addObject("horizontalBarre", "soundPos")
				hg = scene.objects["hautGauche"].position
				bd = scene.objects["basDroit"].position
				volX = (gl.sound[0] / 10) * (bd[0] - hg[0]) + hg[0]
				volY = (gl.sound[1] / 10 -1 ) * (-1) * (bd[1]-hg[1]) + hg[1]
				scene.objects["cursor"].position[0] = volX
				scene.objects["cursor"].position[1] = volY
				scene.objects["verticalBarre"].worldPosition[0] = volX
				scene.objects["horizontalBarre"].worldPosition[1] = volY
				own["soundCursorAc"] = True
				gl.status = "MenuSon"

			elif sys.action == "commandes" :
				gl.configurablePlayers = [gl.conf[0][0][0], gl.conf[0][1][0], gl.conf[0][2][0], gl.conf[0][3][0]]
				own["sys"] = MenuCommandesGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuCommandes"

		elif gl.status == "MenuAffichage" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuOptionsGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuOptions"

		elif gl.status == "MenuEcranSpliter" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuMultijoueursGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.dispPlayers=[0, gl.conf[0][0][0]]
				gl.status = "MenuMultijoueurs"

			elif sys.action == "valider" :
				own["sys"].detruire()
				own["fond"].detruire()
				own["fond"] = FondGui()
				own["sys"] = MenuVoitureMultijoueursGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				own["fond"].frame.img.visible = False

				gl.LibLoad(gl.expandPath("//")+"carSelect.blend", "Scene")
				if gl.dispPlayers[0] == 1:
					viewportDeuxDivision([scene.objects['CameraPlayer1'], scene.objects['CameraPlayer2']], gl.dispPlayers[0])

				elif gl.dispPlayers[0] == 2:
					viewportDeuxDivision([scene.objects['CameraPlayer1'], scene.objects['CameraPlayer2']], gl.dispPlayers[0])

				elif gl.dispPlayers[0] == 3:
					viewportQuatreDivision([scene.objects['CameraPlayer1'], scene.objects['CameraPlayer2'], scene.objects['CameraPlayer3'], scene.objects['CameraPlayer4']])

				elif gl.dispPlayers[0] == 4:
					viewportQuatreDivision([scene.objects['vueVide'], scene.objects['CameraPlayer2'], scene.objects['CameraPlayer3'], scene.objects['CameraPlayer4']])

				elif gl.dispPlayers[0] == 5:
					viewportQuatreDivision([scene.objects['CameraPlayer1'], scene.objects['vueVide'], scene.objects['CameraPlayer3'], scene.objects['CameraPlayer4']])

				elif gl.dispPlayers[0] == 6:
					viewportQuatreDivision([scene.objects['CameraPlayer1'], scene.objects['CameraPlayer2'], scene.objects['CameraPlayer3'], scene.objects['vueVide']])

				elif gl.dispPlayers[0] == 7:
					viewportQuatreDivision([scene.objects['CameraPlayer1'], scene.objects['CameraPlayer2'], scene.objects['vueVide'], scene.objects['CameraPlayer4']])

				gl.status = "MenuVoitureMultijoueurs"

		elif gl.status == "MenuJoueurs" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuOptionsGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuOptions"

		elif gl.status == "MenuCommandes" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuOptionsGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuOptions"
				del gl.configurablePlayers

		elif gl.status == "MenuVoitureMultijoueurs" :
			if sys.action == "retour" :
				gl.dispPlayers=[1, gl.conf[0][0][0], gl.conf[0][1][0]]
				for lib in gl.LibList():
					gl.LibFree(lib)

				own["fond"].detruire()
				own["fond"] = FondGui()
				own["sys"].detruire()
				own["sys"] = MenuEcranSpliterGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				own["fond"].frame.img.visible = True
				own["sys"].nombreJoueurs_label.text = str(len(gl.dispPlayers)-1) + " JOUEURS"
				gl.status = "MenuEcranSpliter"

		elif gl.status == "MenuSon" :
			if sys.action == "retour" :
				own["sys"].detruire()
				own["sys"] = MenuOptionsGui(own["fond"].frame)
				own["fond"].reinit()
				own["fond"].retour_label.text = "Retour"
				gl.status = "MenuOptions"
				own["fond"].frame.img.visible = True
				gl.fondSon.endObject()
				gl.cadreSon.endObject()
				gl.curseurSon.endObject()
				gl.barreVSon.endObject()
				gl.barreHSon.endObject()
				del gl.fondSon
				del gl.cadreSon
				del gl.curseurSon
				del gl.barreVSon
				del gl.barreHSon
				logs.log("info", gl.LibList())
