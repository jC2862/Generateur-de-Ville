import Utils
from mathutils import Vector
import bpy

class Voronoi():
    def print(self):
        for face in self.Faces:
            print(face[0])
            for a in face[1]:
                print("\t"+str(a))

    def conversion_Ancre(self, Ancre):
        #print("CONV")
        aretes = []
        for face in self.Faces:
            if face[0] == Ancre:
                #print("face")
                #print(face)
                aretes = face[1]
        #print(Ancre)
        #print(aretes)
        conv = []
        for a in aretes:
            conv.append([self.Sommets.index(a[0]), self.Sommets.index(a[1])])
        aretes = conv
        conv = []
        for s in self.Sommets:
            conv.append([s.x, s.y, 0])
        conv.append([Ancre.x, Ancre.y, 1])
        sommets = conv
        return [sommets, aretes]
    '''
    def conversion(self):
        conv = []
        for a in self.Aretes:
            conv.append([self.Sommets.index(a[0]), self.Sommets.index(a[1])])
        aretes = conv
        conv = []
        for s in self.Sommets:
            conv.append([s.x, s.y, 0])
        for a in self.Ancres:
            conv.append([a.x, a.y, 1])
        sommets = conv
        return [sommets, aretes]
    '''
    def conversion(self):
        aretes = []
        for face in self.Faces:
            for a in face[1]:
                z = [self.Sommets.index(a[0]), self.Sommets.index(a[1])]
                if z not in aretes:
                    aretes.append(z)
        conv = []
        for s in self.Sommets:
            conv.append([s.x, s.y, 0])
        for a in self.Ancres:
            conv.append([a.x, a.y, 1])
        sommets = conv
        return [sommets, aretes]

    def __init__(self):
        cad = Utils.creer_cadre(10)
        self.Sommets = cad[0]
        self.Aretes = cad[1]
        self.Ancres = []
        self.Faces = []

    def killAll():
        killList = []
        killList.append(A)
        killList.append(B)
        nb_modif=1
        #while(nb_modif != 0):

        return

    def ajouter_arete_ancre(self, ancre, arete):
        for face in self.Faces:
            if face == ancre :  
                face[1].append(arete)

    #a_remplacer: AB
    #remplacant: [AC,CB]
    def remplacer2(self, a_remplacer, remplacant):
        for face in self.Faces:
            for a in face[1]:
                if(a == a_remplacer):
                    face[1].remove(a)
                    face[1].append(remplacant[0])
                    face[1].append(remplacant[1])
    
    def remplacer(self, ints_dsc):
        a_remplacer =[ints_dsc[0],ints_dsc[1]] 
        remplacant = [[ints_dsc[0], ints_dsc[2]],[ints_dsc[2], ints_dsc[1]]]
        self.remplacer2(a_remplacer, remplacant)

    #liste des sommets duquel on veut recupérer les aretes
    def get_arete_de(self, ancres):
        aretes = []
        for face in self.Faces:
            if(face[0] in ancres):
                for a in face[1]:
                    if a not in aretes:
                        aretes.append(a)
        #print("ARET"  + str(aretes))
        return aretes
    '''
    def intersections_droite_millieux(droite_millieux, aretes):
        print("IUNTERSECTION")
        #Milieu = (droite_millieux[0]+droite_millieux[1])/2
        its = []
        for a in aretes:
            print("/!\\")
            print(a)
            it = Utils.intersection(droite_millieux, a)
            if(it != None):
                print("intersection")
                its.append([a, it])
        return its
    '''
    def transferer_arete(self, ancre_A, ancre_B, arete):
        print("tr "+str(arete))
        for face in self.Faces:
            if(face[0] == ancre_A):
                face[1].remove(arete)
                #print("A")
                #print(face)
            elif(face[0] == ancre_B):
                face[1].append(arete)
                #print("B")
                #print(face)
        return
    def edge_equal(ar1, ar2):
        return (ar1[0] == ar2[0] and ar1[1] == ar2[1]) or (ar1[0] == ar2[1] and ar1[1] == ar2[0])

    def transferer_possessions(self, ancre_A, ancre_B, ints):
        trf_list = []
        pro_list = []
        #Ajouter
        for inte in ints:
            if(Utils.distance2(ancre_A, inte[0]) < Utils.distance2(ancre_A, inte[1])):
                trf_list.append(inte[1])
                self.transferer_arete(ancre_A, ancre_B, [inte[2], inte[1]])
            else:
                trf_list.append(inte[0])
                self.transferer_arete(ancre_A, ancre_B, [inte[0], inte[2]])
            pro_list.append(inte[2])

        for face in self.Faces:
            if(face[0] == ancre_A):
                for a in face[1]:
                    #if(a[0] in pro_list or a[1] in pro_list):continue
                    print(a)
                    for i in range(2):
                        if(a[i] in trf_list):
                            #print("a")
                            #print(a)
                            if(a[1-i] not in pro_list):
                                trf_list.append(a[1-i])
                            self.transferer_arete(ancre_A, ancre_B, a)
                            break



        return

    def test_avec_ancre(self, ancre_A, ancre_B):
        droite_millieux = Utils.creer_droite_milieux(ancre_A, ancre_B)
        ar = self.get_arete_de([ancre_A, ancre_B])
        ints = self.trouver_intersections(droite_millieux, ar)
        #print("LEN" + str(len(ints)))
        if(ints == None or len(ints)%2 != 0):return
        #print(ints)
        for i in  ints:
            self.Sommets.append(i[2])
            self.remplacer(i)
        #self.print()
        self.transferer_possessions(ancre_A, ancre_B, ints)
        n_ar = [ints[0][2],ints[1][2]]
        for face in self.Faces:
            if(face[0] == ancre_A or face[0] == ancre_B):
                face[1].append(n_ar)



    def tester_avec_autres_ancres(self, ancre):
        for anc in self.Ancres:
            if(ancre != anc):
                print("ANCRE:" + str(self.Ancres.index(anc)))
                self.test_avec_ancre(anc, ancre)
                print("FIN")


    def ajouterAncre(self, point):
        print("INSERTION -----------------------------")
        #print(len(point))
        assert(type(point)==Vector and len(point) == 2)
        self.Ancres.append(point)
        if(len(self.Faces) == 0):
            Z = Utils.creer_cadre(10)
            self.Sommets = Z[0]
            self.Faces.append([point, Z[1]])
            return
        self.Faces.append([point, []])
        self.tester_avec_autres_ancres(point)
        self.print()

    @staticmethod
    def trouver_intersections(a_tester, aretes):
        intersections = []
        deja_traiter = []
        for a in aretes:
            inter = Utils.intersection(a_tester, a)
            if(inter != None and (a not in deja_traiter)):
                #"a" decomposé pour éviter len(intersertions) == 2 si seulement 1 valeur
                intersections.append([a[0], a[1], inter])
                deja_traiter.append(a)
        if(len(intersections) != 2):
            return None
        return intersections
        




