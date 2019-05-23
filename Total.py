import J
import T
import F
import time 

def execute():
	start = time.time()
	#clean_all()
	#route, cellules = J.creer_route() 
	#J.creer_anim(route)
	liste_cell = T.execute()
	F.execute(liste_cell)
	print("--- %s seconds ---" % (time.time() - start))
	#T.main(cellules)
