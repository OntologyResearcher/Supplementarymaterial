import pickle
import json
from owlready2 import *
#opening the Ontology
with open('relations1.pkl', 'rb') as f:
    data = pickle.load(f)
with open('deleted.pkl', 'rb') as f:
     deleted = pickle.load(f)
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
union_list = set(total1) | set(total2) | set(total3) | set(total4) | set(total5) | set(deleted)
deleted = list(union_list)
print(len(deleted))    
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
    onto.save(file = "test.owl", format = "rdfxml")
#function to code strings / to change unallowed symbols
def change(el:str):
    if el in total1 or el in total2 or el in total3 or el in total4 or el in total5 or el in total6 or el in total7:
        return(el.replace(" ","_"))
    return "_"+el.replace("�", "A0").replace("–", "A1").replace(":", "A2").replace(" ", "_").replace("$", "A3").replace("(", "A4").replace(")", "A5").replace(",", "A6").replace("−", "A7").replace("+", "A8").replace("'", "A9").replace("/", "A10").replace(".", "A11").replace("-", "A12").replace("²", "A13").replace("¼", "A14").replace("½", "A15")
    #return el.replace("�", "A0").replace("–", "A1").replace(":", "A2").replace(" ", "_").replace("$", "A3").replace("(", "A4").replace(")", "A5").replace(",", "A6").replace("−", "A7").replace("+", "A8").replace("'", "A9").replace("/", "A10").replace(".", "A11").replace("-", "A12").replace("²", "A13").replace("¼", "A14").replace("½", "A15")

####
##2#
####
#Second run
#deleted=['instructions', 'computer program', 'logic operation', 'arithmetic', 'logic', 'processors', 'peripherals', 'graphics processing unit', 'graphics processing units', 'operation', 'hardware', 'ics', 'processor', 'registers', 'processor register', 'ic', 'microprocessor', 'integrated circuit', 'cpus', 'device', 'computer', 'central processing unit', 'operations', 'computer memory', 'harvard mark i', 'microcontroller', 'chip', 'tube', 'data', 'clock signal', 'discrete (individual) components', 'printed circuit board', 'discrete', 'main memory', 'instruction', 'simd', 'die', 'capacitor', 'mos', 'fairchild semiconductor', 'federico faggin', 'integrated circuits', 'personal computing devices', 'pc', 'personal computer', "moore's law", 'program', 'address', 'memory', 'block of memory', 'cache', 'register', 'caches', 'clock', 'addition instruction', 'arithmetic logic unit', 'circuitry', 'intel', 'ram', 'virtual memory', 'frequency modulation', 'simd execution unit', 'algorithm', 'digital signal', 'voltage', 'analog - to - digital converter', 'adc', 'phase noise', 'type', 'analog integrator', 'voltage - to - frequency converter', 'flash', 'hard drive', 'rom', 'earlier eeprom', 'flash memory', 'led', 'fpu', 'laser', 'laser sensor', 'debonair', 'mercedes - benz', 'single radar', 'single radar system', 'phase - locked loop', 'pll', 'disk', 'disks', 'western digital', 'sata', 'macintosh', 'data cable', 'scsi', 'moving coil motor', 'fujitsu eagle', 'fdd', 'device driver', 'ide', 'nvme', 'clock generator', 'motorola 68000', 'rop']
for i in range(len(data)):
    if data[i]["head"] not in deleted or data[i]["tail"] not in deleted :
        data[i]="0"
data = [i for i in data if i != "0"]

def save1():
    onto.save(file = "test1.owl", format = "rdfxml")
classes=[]
data1=data
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
    #print(el)
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
#adding instances to the ontology
for el in instanceof:
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
#adding relations to the ontology
for el in data:
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
            if el["head"] in total1 or el["head"] in total2 or el["head"] in total3 or el["head"] in total4 or el["head"] in total5:
                head_unchanged="_"+el["head"]
            else:
                head_unchanged=el["head"]+"_"
            if el["tail"] in total1 or el["tail"] in total2 or el["tail"] in total3 or el["tail"] in total4 or el["tail"] in total5:
                 tail_unchanged="_"+el["tail"]
            else:
                 tail_unchanged=el["tail"]+"_"
            exec(f"with onto: \n  a=onto.search(iri = \"*http://w3id.org/gbo/mgg#{head_unchanged}*\")[0] \n  b=onto.search(iri = \"*http://w3id.org/gbo/mgg#{tail_unchanged}*\")[0] \n  a.{relation}.append(b)")
            continue        
        exec(f"{onto_head}.{head}.is_a.append({onto_rel}.{relation}.some({onto_tail}.{tail}))")

#changing class names/removing _ or __ and adding function
all_classes=list(onto.classes())
object_properties = list(onto.object_properties())
for el in all_classes:
    index =max(el.iri.rfind("/"),el.iri.rfind("#"))+1
    if el.iri[index]=="_" :
        el.iri = el.iri[:index] + el.iri[index+1:]
for el in object_properties:
    print(el.iri)
    index =max(el.iri.rfind("/"),el.iri.rfind("#"))+1
    if el.iri[index]=="_" :
        if el.iri[index+1]=="_" :
            el.iri = el.iri[:index] + el.iri[index+2:]+"_function"
            continue
        el.iri = el.iri[:index] + el.iri[index+1:]+"_function"
        
save1()
