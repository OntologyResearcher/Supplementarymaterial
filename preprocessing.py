import pickle
import json
from owlready2 import *
import pandas as pd
#opening the Ontology
with open('relations.pkl', 'rb') as f:
    data = pickle.load(f)
    
onto = get_ontology("http://test.org/xx")
annotations_data = pd.read_csv('combined_data_v8.csv')
annotations= annotations_data[['Word', 'Agila_DB_tag']]
def Add_SubClasses(name,fullname,index,i):
    word=""
    if annotations["Agila_DB_tag"][i]=="B-"+name:
        word+=annotations["Word"][i]
        j=i+1
        
        while(annotations["Agila_DB_tag"][j]=="I-"+name):
            word+=" "+annotations["Word"][j]
            j+=1
        triple={
                    'head': word.strip(),
                    'type': "subclass of",
                    'tail': fullname
                }
        if  triple not in data and word.strip() in classes:
            data.append({
                    'head': word.strip(),
                    'type': "subclass of",
                    'tail': fullname
                })
            
classes=["component","function","hardware component","hardware part","hardware subpart","measure","quantity","software","system","unit"]
#adding classes
for el in data:
    if isinstance(el, dict):
       if el["tail"] not in classes:
          classes.append(el["tail"])
       if el["head"] not in classes:
          classes.append(el["head"])
       
#adding subclasses for the super classes
for i in range(len(annotations)):
    Add_SubClasses("comp","component",0,i)
    Add_SubClasses("func","function",1,i)
    Add_SubClasses("hwc","hardware component",2,i)
    Add_SubClasses("hwp","hardware part",3,i)
    Add_SubClasses("hwsp","hardware subpart",4,i)
    Add_SubClasses("mea","measure",5,i)
    Add_SubClasses("qt","quantity",6,i)
    Add_SubClasses("sw","software element",7,i)
    Add_SubClasses("sys","system",8,i)
    Add_SubClasses("unit","unit",9,i)

#lowercase change
for el in data:
    el["head"]=el["head"].lower()
    el["type"]=el["type"].lower()
    el["tail"]=el["tail"].lower()
#print(data[-100:-1])
#saving data in pickle file
with open('relations1.pkl', 'wb') as f:
  pickle.dump(data, f)
