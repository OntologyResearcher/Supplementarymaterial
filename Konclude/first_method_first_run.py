import pickle
import json
import subprocess
from owlready2 import *
#opening the Ontology
with open('relations1.pkl', 'rb') as f:
    data = pickle.load(f)

onto = get_ontology("GENIALOntBFO.owl").load()
#list of the 10 tags
all_classes=list(onto.classes())
object_properties = list(onto.object_properties())
total=[]
total1=[]
total2=[]
total3=[]
total4=[]
total5=[]
total6=[]
total7=[]
functionsnamespaces=[]
deleted=[]
for el in all_classes:
    length=max(el.iri.rfind("/"),el.iri.rfind("#"))+1
    if el.iri[0:length]=="http://w3id.org/gbo#":
        total1.append(el.iri[length:].replace("_"," "))
        total.append(el.iri)
    if el.iri[0:length]=="http://w3id.org/gbo/CarModel/":
        total2.append(el.iri[length:].replace("_"," "))
        total.append(el.iri)
    if el.iri[0:length]=="http://www.ontology-of-units-of-measure.org/resource/om-2/":
        total3.append(el.iri[length:].replace("_"," "))
        total.append(el.iri)
    if el.iri[0:length]=="http://w3id.org/gbo/":
        total4.append(el.iri[length:].replace("_"," "))
        total.append(el.iri)
    if el.iri[0:length]=="http://www.w3.org/ns/sosa/":
        total5.append(el.iri[length:].replace("_"," "))
        total.append(el.iri)
for el in object_properties:
    length=max(el.iri.rfind("/"),el.iri.rfind("#"))+1
    if el.iri[0:length]=="http://w3id.org/gbo#":
        total6.append(el.iri[length:].replace("_"," "))   
    if el.iri[0:length]=="http://www.ontology-of-units-of-measure.org/resource/om-2/":
        total7.append(el.iri[length:].replace("_"," "))
    
with onto:
    a1 = get_namespace("http://w3id.org/gbo#")
    a2 = get_namespace("http://w3id.org/gbo/CarModel/")
    a3 = get_namespace("http://www.ontology-of-units-of-measure.org/resource/om-2/")
    a4 = get_namespace("http://w3id.org/gbo/")
    a5 = get_namespace("http://www.w3.org/ns/sosa/")
#fixing direct graph cycles
for i in range(len(data)):
    if data[i]["type"]=="subclass of" :
        for i1 in range(i+1,len(data)):
            if data[i1]["type"]=="subclass of" :
                if data[i]["head"]==data[i1]["tail"] and data[i]["tail"]==data[i1]["head"]:
                    data[i]="0"
                    break
for el in data:
    if el=="0":
        data.remove(el)
    else:
      if el["head"]==el["tail"] and el["type"]=="subclass of":
        data.remove(el)
#deleting instances where one of head or tail is ""
      if (el["head"]=="" or el ["tail"]==""):
          data.remove(el)
#deleting subclass that defies the Disjoint Rule
      if el["type"]=="subclass of" and el["head"] in ["hardware component","hardware elementary subpart","hardware part","hardware subpart"]  and el["tail"] in ["hardware component","hardware elementary subpart","hardware part","hardware subpart"]:
          data.remove(el)
#Function to save Ontology in an owl file function
def save():
    onto.save(file = "test.owl", format = "owlxml")
#function to code strings / to change unallowed symbols
def change(el:str):
    if el in total1 or el in total2 or el in total3 or el in total4 or el in total5 or el in total6 or el in total7:
        return(el.replace(" ","_"))
    return "_"+el.replace("�", "A0").replace("–", "A1").replace(":", "A2").replace(" ", "_").replace("$", "A3").replace("(", "A4").replace(")", "A5").replace(",", "A6").replace("−", "A7").replace("+", "A8").replace("'", "A9").replace("/", "A10").replace(".", "A11").replace("-", "A12").replace("²", "A13").replace("¼", "A14").replace("½", "A15")
    #return el.replace("�", "A0").replace("–", "A1").replace(":", "A2").replace(" ", "_").replace("$", "A3").replace("(", "A4").replace(")", "A5").replace(",", "A6").replace("−", "A7").replace("+", "A8").replace("'", "A9").replace("/", "A10").replace(".", "A11").replace("-", "A12").replace("²", "A13").replace("¼", "A14").replace("½", "A15")
def check2():
    save()
    os.system('start /wait cmd /c "Konclude consistency -i Test.owl -o result1.txt "')
    with open('result1.txt', 'r') as file:
        for line in file:
            if line[0:5]=="false":
                return True
    return False   
#onto.save(file = "test.owl", format = "rdfxml")
classes=[]
data1=data
#print(data[0:50])
#adding classes
for el in data:
    if isinstance(el, dict):
       if el["tail"] not in classes:
          classes.append(el["tail"])
       if el["head"] not in classes:
          classes.append(el["head"])
       
#Defining subcalsses List(each class of index i has his subclasses at index i)
SubClasses=[ [] for i in range(len(classes))]
instanceof=[]#list of dictionnaries with triples and type=="instance of"
instances=[]#list of instances
for el in data:
#adding subclasses for el in data:
    if el["type"]=="subclass of":
        index = classes.index(el["head"])
        if el["tail"] not in SubClasses[index]:
          SubClasses[index].append(el["tail"])
#adding relations to the instanceS list
for el in data:
    if el["type"]=="instance of":
        instanceof.append(el)
        instances.append(el["head"])
#weird bug manual correction
for i in range(len(SubClasses)):
    if classes[i]=="workflow" and SubClasses[i]==["workflow"]:
        SubClasses[i]=[]
#adding classes to Ontology         
for i in range(len(SubClasses)):
    if SubClasses[i]==[]:
        if classes[i] not in total1 and classes[i] not in total2 and classes[i] not in total3 and classes[i] not in total4 and classes[i] not in total5:
            class_name=change(classes[i])
            label=classes[i]
            exec(f"with onto: \n  class {class_name}(Thing): \n   label=\"{label}\" ")
    else:
        subclasses_of_el=""
        class_name=change(classes[i])
        label=classes[i]
        for subclass in SubClasses[i]:
            onto_subclass="onto"
            if subclass in total1:
                onto_subclass="a1"
            if subclass in total2:
                onto_subclass="a2"
            if subclass in total3:
                onto_subclass="a3"
            if subclass in total4:
                onto_subclass="a4"
            if subclass in total5:
                onto_subclass="a5"
            if subclasses_of_el=="":
                subclasses_of_el+=onto_subclass+"."+change(subclass)
            else:
                subclasses_of_el+=","+onto_subclass+"."+change(subclass)  # CPU,Compenent
            if subclass not in total1:
              missingclass=change(subclass)
              exec(f"with onto: \n  if not onto.{missingclass}: \n    class {missingclass}(Thing): \n      pass")
        if classes[i] not in total1 and classes[i] not in total2 and classes[i] not in total3 and classes[i] not in total4 and classes[i] not in total5:
            exec(f"with onto: \n  class {class_name}({subclasses_of_el}): \n    label=\"{label}\" ")

        else:
            if classes[i] in total1:
                exec(f"with onto: \n  class {class_name}({subclasses_of_el}): \n    label=\"{label}\" \n    namespace=a1 ")
            if classes[i] in total2:
                exec(f"with onto: \n  class {class_name}({subclasses_of_el}): \n    label=\"{label}\" \n    namespace=a2 ")
            if classes[i] in total3:
                exec(f"with onto: \n  class {class_name}({subclasses_of_el}): \n    label=\"{label}\" \n    namespace=a3 ")
            if classes[i] in total4:
                exec(f"with onto: \n  class {class_name}({subclasses_of_el}): \n    label=\"{label}\" \n    namespace=a4 ")
            if classes[i] in total5:
                exec(f"with onto: \n  class {class_name}({subclasses_of_el}): \n    label=\"{label}\" \n    namespace=a5 ")

#adding relations to the ontology
for el in data1:
    onto_rel="onto"
    if el["type"] in total7:
        onto_rel="a3"
    if el["type"] in total6:
        onto_rel="a1"
    if el["type"] in total6 or el["type"] in total7:
        relation=change(el["type"])
    else:
        relation="_"+change(el["type"])
    if el["type"]=="instance of":
        continue
    if el["type"]!="subclass of":
        onto_tail="onto"
        onto_head="onto"
        if el["head"]  in total1:
            onto_head="a1"
        if el["head"]  in total2:
            onto_head="a2"
        if el["head"]  in total3:
            onto_head="a3"
        if el["head"]  in total4:
            onto_head="a4"
        if el["head"]  in total5:
            onto_head="a5"
        if el["tail"]  in total1:
            onto_tail="a1"
        if el["tail"]  in total2:
            onto_tail="a2"
        if el["tail"]  in total3:
            onto_tail="a3"
        if el["tail"]  in total4:
            onto_tail="a4"
        if el["tail"]  in total5:
            onto_tail="a5"
        label=el["type"]
        head=change(el["head"])
        tail=change(el["tail"])
        head_unchanged=(el["head"])
        tail_unchanged=(el["tail"])
        #print(label+" "+head+" "+tail )
        if el["type"] not in total6 and el["type"] not in total7:
            exec(f"with onto: \n  class {relation}(ObjectProperty): \n    label=\"{label}\" ")
        if head_unchanged in instances and tail_unchanged in instances:
            continue        
        exec(f"{onto_head}.{head}.is_a.append({onto_rel}.{relation}.some({onto_tail}.{tail}))")

#deleting  inconsistant classes
all_classes=list(onto.classes())
for el in all_classes:
    save()
    r = subprocess.run(['cmd', '/c', "Konclude satisfiability -i Test.owl -o result.txt -x " +el.iri], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    #os.system('start /wait  cmd /c "Konclude satisfiability -i Test.owl -o result.txt -x '+el.iri+'"')
    with open('result.txt', 'r') as file:
        for line in file:
            if line[0:5]=="false" :
                if el.iri in total:
                    print(el.iri)
                    continue
                print("x")
                deleted.append(el.label)
                with onto:
                    destroy_entity(el)
                save()
print("checking")
all_classes=list(onto.classes())
for el in all_classes:
    if el.iri in total:
        os.system('start /wait  cmd /c "Konclude satisfiability -i Test.owl -o result.txt -x '+el.iri+'"')
        with open('result.txt', 'r') as file:
            for line in file:
                if line[0:5]=="false" :
                    print(el.iri)
for i in range(len(deleted)):
    if isinstance(deleted[i], list):
        deleted[i]=deleted[i][0]
print(deleted)
instances1=[]
#adding instances to the ontology
for el in instanceof:
    if el["head"]  in deleted or el["tail"]  in deleted:
        continue
    onto_tail="onto"
    onto_head="onto"
    if el["head"]  in total1:
        onto_head="a1"
    if el["head"]  in total2:
        onto_head="a2"
    if el["head"]  in total3:
        onto_head="a3"
    if el["head"]  in total4:
        onto_head="a4"
    if el["head"]  in total5:
        onto_head="a5"
    if el["tail"]  in total1:
        onto_tail="a1"
    if el["tail"]  in total2:
        onto_tail="a2"
    if el["tail"]  in total3:
        onto_tail="a3"
    if el["tail"]  in total4:
        onto_tail="a4"
    if el["tail"]  in total5:
        onto_tail="a5"
    head=el["head"]+"_"
    label=el["head"]
    if head in total1 or head in total2 or head in total3 or head in total4 or head in total5:
        head="_"+el["head"]
    tail=change(el["tail"])
    changed_head=change(el["head"])
    #print(head+" "+tail)
    exec(f"with onto: \n  instance={onto_tail}.{tail}(\"{head}\") \n  instance.label=\"{label}\"")
    exec(f"with onto: \n  instance={onto_head}.{changed_head}(\"{head}\")")
    #reasoning
    if check2():
        with onto:
            destroy_entity(instance)
        instances1=[x for x in instances1 if x != el["head"]]
    else:
        instances1.append(el["head"])
#Adding relations between instances        
for el in data1:
    if el["head"]  in deleted or el["tail"]  in deleted:
        continue
    #not doing subclass of or instance of
    if el["type"]=="instance of" or el["type"]=="subclass of" :
        continue
    #fixing type variable
    if el["type"] in total6 or el["type"] in total7:
        relation=change(el["type"])
    else:
        relation="_"+change(el["type"])

    head=el["head"]
    tail=el["tail"]
    #doing the relation
    if el["head"] in instances1 and el["tail"] in instances1:
            exec(f"with onto: \n  a=onto.search(iri = \"*http://w3id.org/gbo/mgg#{head}*\")[0] \n  b=onto.search(iri = \"*http://w3id.org/gbo/mgg#{tail}*\")[0] \n  a.{relation}.append(b)")
            continue
#changing class names/removing _ or __ and adding function
all_classes=list(onto.classes())
object_properties = list(onto.object_properties())
for el in all_classes:
    index =max(el.iri.rfind("/"),el.iri.rfind("#"))+1
    if el.iri[index]=="_" :
        #print(el.iri)
        el.iri = el.iri[:index] + el.iri[index+1:]
for el in object_properties:
    index =max(el.iri.rfind("/"),el.iri.rfind("#"))+1
    if el.iri[index]=="_" :
        if el.iri[index+1]=="_" :
            el.iri = el.iri[:index] + el.iri[index+2:]+"_function"
            continue
        el.iri = el.iri[:index] + el.iri[index+1:]+"_function"
        
save()
print(deleted)
with open("deleted.pkl", "wb") as f:
    # Save the list in the file
    pickle.dump(deleted, f)
