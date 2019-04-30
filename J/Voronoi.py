import Utils
from mathutils import Vector
import bpy

class Voronoi():
    def conversion_Ancre(self, Ancre):
        aretes = []
        for face in self.Faces:
            if face[0] == Ancre:
                aretes = face[1]
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
    def test_avec_ancre(self, ancre_A, ancre_B):
        droite_millieux = Utils.creer_droite_milieux(ancre_A, ancre_B)
        ar = self.get_arete_de([ancre_A, ancre_B])
        ints = self.trouver_intersections(droite_millieux, ar)
        assert(ints != None and len(ints)==2)
        print(ints)
        for i in  ints:
            self.Sommets.append(i[2])
            self.remplacer(i)



    def tester_avec_autres_ancres(self, ancre):
        droite_millieux 
        D, E = intersections(droite_milieux, aretesancre, autre)
        #trouver segment entre ancre et autres #D B
        #supprilmer db
        #ajouter liaison


    def ajouterAncre(self, point):
        assert(type(point)!=Vector and len(point) == 2)
        Ancres.append(point)

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
        




