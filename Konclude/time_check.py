import os
from owlready2 import *
import sqlite3
print(sqlite3.sqlite_version)
start_time = time.time()
onto = get_ontology("test.owl").load()
all_classes=list(onto.classes())
a1 = get_namespace("http://w3id.org/gbo#")
#populating total lists
all_classes=list(onto.classes())
sync_reasoner()
for el in all_classes:
        os.system("Konclude satisfiability -i test.owl -o result.txt -x "+el.iri)
        #process = subprocess.check_output("./Konclude satisfiability -i test.owl -o result.txt -x "+el.iri+" -w 24", shell=True)
        #if Nothing in el.equivalent_to:
        #    print("x")
        with open('result.txt', 'r') as file:
            for line in file:
               if line[0:5]=="false":
                   print(el.iri)
                
    
    
#onto.save(file = "test.owl", format = "rdfxml")
elapsed_time = time.time() - start_time

print("Elapsed time: {:.2f} seconds".format(elapsed_time))
