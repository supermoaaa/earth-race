from bge import logic as gl

sce = gl.getCurrentScene()

# parent object
parentObj = "carosserie"

for obj in sce.objects:
    print(obj.name)
with open('fichier.txt', 'a') as mon_fichier:
    for obj in sce.objects:
        if obj.name == parentObj:
            mon_fichier.write("car = " + parentObj + "\n")
        elif obj.name == "fl":
            mon_fichier.write("wheel front left = 1 1 fl"+ "\n")
        elif obj.name == "fr":
            mon_fichier.write("wheel front right = 1 1 fr"+ "\n")
        elif obj.name == "bl":
            mon_fichier.write("wheel back left = 1 1 bl"+ "\n")
        elif obj.name == "br":
            mon_fichier.write("wheel back right = 1 1 br"+ "\n")
        elif obj.name == "__default__cam__":
            pass
        else:
            mon_fichier.write("child = " + obj.name+ "\n")
