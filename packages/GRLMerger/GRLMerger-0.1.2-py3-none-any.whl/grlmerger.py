import pandas as pd
import numpy as np
import re
from random import randint
import statistics 
import neattext as nt
import neattext.functions as nfx
import warnings
warnings.filterwarnings('ignore')

from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag, pos_tag_sents
lemmatizer = WordNetLemmatizer()

from tabulate import tabulate
from sys import exit 




#SBERT
from sentence_transformers import SentenceTransformer, util

SBERT = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# ----------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# ------------------------------ CONVERTING TGRL TO CSV ----------------------------- #
# ----------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------- #

# CONVERTING TGRL INTO CSV #
def readModel(file_name):
    global lines
    with open(file_name) as f:
        lines = f.readlines()

def splitSentences():
    count = 0
    models = []
    global lines
    for line in lines:
        line = line.strip() #remove white spaces/tabs
        line = re.split('({|}|;|,)', line) #split the line based on { or } or ; and keep them
        line = list(filter(None, line)) #remove empty strings
        line = [i.strip() for i in line] #remove white spaces around a string
        if len(line) != 0: #not including empty lines
            models.append(line)
            count += 1
            
    global flatList 
    flatList = [ item for elem in models for item in elem] #convert the list of lists to a list
    
# preprocess the attributes
# ensure that they are in the form of (a_type = a_name | comment "some text")
def processAttributes():
    global flatList
    f = 0
    loop_len = len(flatList)
    while f < loop_len:
        if flatList[f] == '=' or flatList[f].startswith('='):
            n = f 
            while flatList[n] != ';':
                flatList[f-1] = flatList[f-1] + ' ' + flatList[n] 
                flatList.pop(n)
                loop_len = loop_len - 1
            f = f + 1
        elif flatList[f].endswith('=') and len(flatList[f]) > 1:
            n = f + 1
            while flatList[n] != ';':
                flatList[f] = flatList[f] + ' ' + flatList[n]
                flatList.pop(n)
                loop_len = loop_len - 1
            f = f + 1
        elif flatList[f].startswith('comment'):
            n = f + 1
            while flatList[n] != ';':
                flatList[f] = flatList[f] + ' ' + flatList[n]
                flatList.pop(n)
                loop_len = loop_len - 1
            f = f + 1
        else:
            f = f + 1 
            
# preprocess the intentional elements
# ensure that they are in the form of (type ID)
def processElements():
    global flatList
    f = 0
    loop_len = len(flatList)
    while f < loop_len:
        if flatList[f] == 'goal' or flatList[f] == 'softGoal' or flatList[f] == 'task' or flatList[f] == 'resource' or flatList[f] == 'belief' or flatList[f] == 'indicator':
            flatList[f] = flatList[f] + ' ' + flatList[f+1]
            flatList.pop(f+1)
            loop_len = loop_len - 1
        else:
            f = f + 1
            
# Preprocess the splitted strings
def processStrings():
    global flatList
    f = 0
    loop_len = len(flatList)
    while f < loop_len:
        if flatList[f].startswith('name') or flatList[f].startswith('description') or flatList[f].startswith('metadata') or flatList[f].startswith('decompositionType'):
            n = f + 1
            while flatList[n] != ';':
                flatList[f] = flatList[f] + ' ' + flatList[n]
#                print('----------------', flatList[f])
                flatList.pop(f+1)
                loop_len = loop_len - 1
            f = f + 1
        elif (flatList[f].startswith('"') and (not flatList[f].endswith('"'))) or flatList[f] == '"': #for relation description
            n = f + 1
            while flatList[n] != '}':
#                print(flatList[n])
                flatList[f] = flatList[f] + ' ' + flatList[n]
                flatList.pop(f+1)
                loop_len = loop_len - 1
            f = f + 1
        else:
            f = f + 1
            
# preprocess the contribution 
# ensure that they are in the form of (child contributesTo parent | parent decomposedBy|dependsOn child)
def processRelationsForm():
    global flatList
    f = 0
    loop_len = len(flatList)
    while f < loop_len:
        if flatList[f] == 'contributesTo' or flatList[f].startswith('contributesTo') or flatList[f] == 'decomposedBy' or flatList[f].startswith('decomposedBy') or flatList[f] == 'dependsOn' or flatList[f].startswith('dependsOn'):
            n = f 
            while flatList[n] != '{' and flatList[n] != ';':
                flatList[f-1] = flatList[f-1] + ' ' + flatList[n] 
                flatList.pop(n)
                loop_len = loop_len - 1
        elif (flatList[f].endswith('contributesTo') or flatList[f].endswith('decomposedBy') or flatList[f].endswith('dependsOn')) and len(flatList[f]) > 1:
            n = f + 1
            while flatList[n] != '{' and flatList[n] != ';':
                flatList[f] = flatList[f] + ' ' + flatList[n]
                flatList.pop(n)
                loop_len = loop_len - 1
        else:
            f = f + 1 
        
def processList():
    global flatList 
    flatList = list(filter(None, flatList))
    # Remove spaces around strings inside strings
    for n in range(len(flatList)):
        flatList[n] = re.sub('("\ *)','"', flatList[n])
        flatList[n] = re.sub('(\ *")', '"', flatList[n])
        
        
# Function that starts all parsing steps
def startParsing():
    ac = 0
    actor_ID = ''
    dummy_exist = False
    relation_index = []
    global flatList
    for x in range(len(flatList)):
        if flatList[x].startswith('//'):
    #         print("Comment:", flatList[x])
            continue
        # Processing goal model ID
        elif flatList[x].startswith('grl'): #grl does not have "name" attribute
            statement_elements = flatList[x].split()
            model_name = statement_elements[1]
#            print("Model Name:", model_name)
            if flatList[x+1] == '{' and flatList[x+2] == '}':
                # I do not think that I need to store the empty model
                insertRow(model_name, '', '', '', '', '', '', '')
        # ----- Processing actor        
        elif flatList[x].startswith('actor'):
            ac = 1
            statement_elements = flatList[x].split()
            actor_ID = statement_elements[1]
#            print("Actor ID:", actor_ID)
            if (flatList[x+1] == '{' or flatList[x+1] == ';') and flatList[x+2] == '}':
                insertActor(model_name, actor_ID, '', '', '', '')
            # ----- Process actor's attributes
            elif flatList[x+1] == '{':
                y = x+2
                actor_name = ''
                actor_description = ''
                actor_importance = ''
                actor_metadata = ''
                while y in range(len(flatList)):
                    if not flatList[y].startswith('actor'):
                        if flatList[y] == '{':
                            z = y
                            while flatList[z] != '}':
                                z = z + 1
                            y = z+1
                        elif flatList[y].startswith(('name', 'description', 'importance', 'metadata')):
                            a_details = flatList[y].split('=')
                            a_details[0] = a_details[0].strip()
                            a_details[1] = a_details[1].strip()
                            if a_details[0] == 'name':
                                actor_name = a_details[1].strip('"')
#                                 print("After assigning the name", actor_name)
                            elif a_details[0] == 'description':
                                actor_description = a_details[1].strip('"')
#                                 print("After assigning the description", actor_description)
                            elif a_details[0] == 'importance':
                                actor_importance = a_details[1]
#                                 print("After assigning the importance", actor_importance)
                            elif a_details[0].startswith('metadata'):
                                metadata_attribute = a_details[0].split()
                                metadata_attribute = metadata_attribute[1]
                                actor_metadata = actor_metadata + metadata_attribute + ' = ' + a_details[1] + ' ; '
#                                 print("After assigning the metadata", actor_metadata)
                            y = y + 1
                        else:
                            y = y + 1
                    else:
                        break
                insertActor(model_name, actor_ID, actor_name, actor_description, actor_importance, actor_metadata)


        # set counter if actor is found c = 1 
        # add 1 if { else if } minus 1
        # if c == 0 ; assign dummy actor XX; add actor XX with name and description to the actors csv
        # ----- Processing intentional elements        
        elif flatList[x].startswith(('goal', 'softGoal', 'task', 'resource', 'belief', 'indicator')):
            statement_elements = flatList[x].split()
            element_type = statement_elements[0]
            element_ID = statement_elements[1]
            element_name = statement_elements[1]
            element_description = ''
            element_importance = ''
            element_metadata = ''
            decomposition_type = ''
#             print("Intentional element:", flatList[x])
            y = x + 1
            ielement_attributes = []
            if flatList[y] == '{':
                y = y + 1
                while flatList[y] != '}':
                    if flatList[y] != ';':
#                         print("Intentional element attribute", flatList[y])
                        ielement_attributes.append(flatList[y])
                    y = y + 1
            # Processing intentional element attributes
            for i in range(len(ielement_attributes)):
                attribute_elements = ielement_attributes[i].split('=')
                attribute_elements = [i.strip() for i in attribute_elements]
    #             print("THIS SPLIT", attribute_elements)
    #             print("Attribute name", attribute_elements[0], "Attribute value", attribute_elements[1])
                if attribute_elements[0] == 'name':
                    attribute_elements[1] = attribute_elements[1].strip('"|\'')
                    element_name = attribute_elements[1]
                elif attribute_elements[0] == 'description':
                    attribute_elements[1] = attribute_elements[1].strip('"')
                    element_description = attribute_elements[1]
                elif attribute_elements[0] == 'importance':
                    element_importance = attribute_elements[1]
                elif attribute_elements[0].startswith('metadata'):
                    metadata_attribute = attribute_elements[0].split()
                    metadata_attribute = metadata_attribute[1]
                    attribute_elements[1] = attribute_elements[1].strip('"')
                    element_metadata = element_metadata + metadata_attribute + ' = ' + attribute_elements[1] + ' ; '
                elif attribute_elements[0] == 'decompositionType':
                    decomposition_type = attribute_elements[1]
                    
            if ac == 1 or actor_ID == '':
                actor_ID = 'X#Y'
                actor_name = 'X#YDUMMYACTOR'
                if not dummy_exist:
                    insertActor(model_name, actor_ID, actor_name, '', '', '')
                    dummy_exist = True 
#                insertActor(model_name, actor_ID, actor_name, '', '', '')
            insertRow(model_name, actor_ID, element_type, element_ID, element_name, element_description, element_importance, element_metadata, decomposition_type)
#            print('The inserted ROW', model_name, actor_ID, element_type, element_ID, element_name, element_description, element_importance, element_metadata, decomposition_type)
#            print('---------------')


        elif flatList[x].startswith("comment"):
            statement_elements = flatList[x].split('"')
            element_type = 'comment'
            comment_text = statement_elements[1]
            insertRow(model_name, '', element_type, '', comment_text, '', '', '', '')

        elif flatList[x] == '{':
            ac = ac + 1
            
        elif flatList[x] == '}':
            ac = ac - 1
            
        elif flatList[x].find("decomposedBy") != -1 or flatList[x].find("dependsOn") != -1 or flatList[x].find("contributesTo") != -1:
            # I don't parse the relations during parsing the intentional elements
            # because I want all i elements to be stored, hence I can get their actors
            relation_index.append(x)
            
            
    for x in range(len(relation_index)):
        processRelation(relation_index[x])
        
def insertActor(model_name, actor_ID, actor_name, actor_description, actor_importance, actor_metadata):
    global a_models_name
    global a_actors_ID
    global actors_name
    global actors_description
    global actors_importance
    global actors_metadata
    a_models_name.append(model_name)
    a_actors_ID.append(actor_ID)
    actors_name.append(actor_name)
    actors_description.append(actor_description)
    actors_importance.append(actor_importance)
    actors_metadata.append(actor_metadata)
    
def insertRow(model_name, actor_ID, element_type, element_ID, element_name, element_description, element_importance, element_metadata, decomposition_type):
    models_name.append(model_name)
    actors_ID.append(actor_ID)
    ielements_type.append(element_type)
    ielements_ID.append(element_ID)
    ielements_name.append(element_name)
    ielements_description.append(element_description)
    ielements_importance.append(element_importance)
    ielements_metadata.append(element_metadata)
    ielements_decompositionType.append(decomposition_type)
    
# Inserting relation elements in a row
def insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor, child_ID, decomposition_type, contribution_value):
    parent_actors_IDs.append(parent_actor_ID)
    parent_elements_IDs.append(parent_element_ID)
    relation_types.append(relation_type)
    children_actors_IDs.append(child_actor)
    children_elements_IDs.append(child_ID)
    decomposition_types.append(decomposition_type)
    contribution_values.append(contribution_value)
    
def processRelation(x):
    global flatList
    relation = re.split(' ', flatList[x])
#    print(relation, "- Length:", len(relation))
    relation_type = relation[1]
#    print(relation_type)
    
    if relation_type == 'decomposedBy' or relation_type == 'dependsOn':
        p = 0
        c = 2
#        print("RELATION TYPE", relation_type, "PARENT INDEX", p, 'CHILD INDEX', c)
    elif relation_type == 'contributesTo':
        p = 2
        c = 0
#        print("RELATION TYPE", relation_type, "PARENT INDEX", p, 'CHILD INDEX', c)
        
    parent = relation[p]
    if parent.find(".") != -1:
        parent = re.split('\.', parent)
        parent_actor_ID = parent[0]
        parent_element_ID = parent[1]   
    else:
        index = ielements_ID.index(parent)
        parent_actor_ID = actors_ID[index]
        parent_element_ID = parent
      
        
    
    child = relation[c]
    if child.find('.') != -1:
        child = re.split('\.', child)
        child_actor_ID = child[0]
        child_element_ID = child[1]
    else:
        index = ielements_ID.index(child)
        child_actor_ID = actors_ID[index]
        child_element_ID = child
            
        
        
    if relation_type == 'decomposedBy':
        relation_type = 'decomposition'
        contribution_value = ''
        d_type = decompositionType(parent_actor_ID, parent_element_ID)
        if d_type == '':
            decomposition_type = 'and'
        else:
            decomposition_type = d_type
        insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
            
    elif relation_type == 'dependsOn':
        relation_type = "dependency"
        decomposition_type = ''
        contribution_value = ''
        insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
        
    elif relation_type == 'contributesTo':
        relation_type = 'contribution'
        decomposition_type = ''
    
    if relation_type == 'dependency' or relation_type == 'decomposition':
        c = x + 1
        # continue inserting the children in a relation of a parent
        while flatList[c] != ';':
            if flatList[c] == '{':
                n = c + 1
                while flatList[n] != '}':
                    n = n + 1
                c = n + 1
            elif flatList[c] == ',':
                n = c + 1
                child = flatList[n]
                if child.find('.') != -1:
                    child = re.split('\.', child)
                    child_actor_ID = child[0]
                    child_element_ID = child[1]
                else:
                    index = ielements_ID.index(child)
                    child_actor_ID = actors_ID[index]
                    child_element_ID = child
                
                insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
            c = n + 1         
        x = c + 1 #update the x index in case there are many children 
        
    elif relation_type == 'contribution':
        if flatList[x+1] == ',' or flatList[x+1] == ';':
            contribution_value = 25
            insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
            if flatList[x+1] == ',':
                m = x + 1
                c = insertAnotherParent(m, parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
            m = c
        elif flatList[x+1] == '{':
            n = x + 1
            if flatList[n+1] == '}': #in case the user writes {}
                contribution_value = 25
                insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
            else:
                while flatList[n] != '}': #to get the contribution value
                    if contribution_pattern.match(flatList[n]):
                        contribution_value = flatList[n]
                        insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
                    n = n + 1
                m = n + 1
                while flatList[m] != ';':
                    if flatList[m] == ',':
                        contribution_value = 25
                        c = insertAnotherParent(m, parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
                    m = c


# to get the actor name in case the element in the relation with no actor (it would be the current actor or dummy actor):
def findActor(element):
    element_exist = ielements_ID.count(element)
    if element_exist > 0:
        index = ielements_ID.index(element)
        return actors_ID[index]
    elif element_exist == 0:
        
        return "dummy"
    
# to get the decomposition type from the elements dataframe 
def decompositionType(parent_actor_ID, parent_element_ID):
#     actors_ID = df_elements['actor_ID'].to_list()
#     elements_ID = df_elements['ielement_ID'].to_list()
#     decomposition_type = df_elements['ielement_decomposition_type'].to_list()
    for x in range(len(actors_ID)):
        if parent_actor_ID == actors_ID[x] and parent_element_ID == ielements_ID[x]:
            return ielements_decompositionType[x]
        

# Inserting contribution relation for the same child 
def insertAnotherParent(m, parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value):
    global flatList
    l = m + 1
    parent = flatList[l]
    
    if parent.find(".") != -1:
        parent = re.split('\.', parent)
        parent_actor_ID = parent[0]
        parent_element_ID = parent[1]   
    else:
        index = ielements_ID.index(parent)
        parent_actor_ID = actors_ID[index]
        parent_element_ID = parent
    
    
    if flatList[l+1] == ',' or flatList[l+1] == ';':
        contribution_value = 25
        insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
    elif flatList[l+1] == '{':
        z = l + 1
        if flatList[z] == '}': #in case the user writes {}
            contribution_value = 25
            insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
        else:
            while flatList[z] != '}':
                if contribution_pattern.match(flatList[z]):
                    contribution_value = flatList[z]
                    insertRelationRow(parent_actor_ID, parent_element_ID, relation_type, child_actor_ID, child_element_ID, decomposition_type, contribution_value)
                z = z + 1
            c = z + 1
        return c
                   
        
def checkUniqueIDs(IDs_list):
    oc_set = set()
    duplicate_index = []
    for idx, val in enumerate(IDs_list):
        if val not in oc_set:
            oc_set.add(val)         
        else:
            duplicate_index.append(idx) 

    if len(duplicate_index) > 0:
        for r in range(len(duplicate_index)):
            value = randint(0, 100)
            IDs_list[duplicate_index[r]] = IDs_list[duplicate_index[r]]+str(value)
            
# Storing multiple CSV in one excel file
def dfs_tabs(df_list, sheet_list, file_name):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0, index=False)   
    writer.save()  


def insertActors():
    global a_models_name
    global a_actors_ID
    global actors_name
    global actors_description
    global actors_importance
    global actors_metadata
    
    table = {'model_name': [],'actor_ID': [], 'actor_name': [], 'actor_description': [], 'actor_importance': [], 'actor_metadata': []}

    # Check uniqueness of actors IDs
    checkUniqueIDs(a_actors_ID)

    for x in range(len(actors_name)):
        table["model_name"].append(a_models_name[x])
        table["actor_ID"].append(a_actors_ID[x])
        if actors_name[x] == "":
            table["actor_name"].append(a_actors_ID[x])
        else:
            table["actor_name"].append(actors_name[x])
        table["actor_description"].append(actors_description[x])
        table["actor_metadata"].append(actors_metadata[x])
        table["actor_importance"].append(actors_importance[x])   
    df_actors=pd.DataFrame.from_dict(table,orient='index').transpose()
    return df_actors

def insertElements():
    global models_name
    global actors_ID
    global ielements_type
    global ielements_ID
    global ielements_name
    global ielements_description
    global ielements_importance
    global ielements_metadata
    global ielements_decompositionType

    table = {'model_name': [],'actor_ID': [], 'ielement_type': [], 'ielement_ID': [], 'ielement_name': [], 'ielement_description': [], 'ielement_importance': [], 'ielement_metadata': [], 'ielement_decomposition_type': []}

    # Check uniqueness of elements IDs
    checkUniqueIDs(ielements_ID)

    for x in range(len(ielements_type)):
        if models_name[x] == "":
            table["model_name"].append(ielements_ID[x])
        else:
            table["model_name"].append(models_name[x])
        table["actor_ID"].append(actors_ID[x])
        table["ielement_type"].append(ielements_type[x])
        table["ielement_ID"].append(ielements_ID[x])
        if ielements_type[x] == 'belief':
            table["ielement_name"].append(ielements_description[x])
            table["ielement_description"].append(ielements_name[x])
        else:
            table["ielement_name"].append(ielements_name[x])
            table["ielement_description"].append(ielements_description[x])

        table["ielement_importance"].append(ielements_importance[x])        
        table["ielement_metadata"].append(ielements_metadata[x])
        table["ielement_decomposition_type"].append(ielements_decompositionType[x])
    df_elements=pd.DataFrame.from_dict(table,orient='index').transpose()
    return df_elements


def insertRelations(model_ID):
    global parent_actors_IDs
    global parent_elements_IDs
    global relation_types
    global children_actors_IDs
    global children_elements_IDs
    global decomposition_types
    global contribution_values

    table = {'relation_ID': [], 'parent_actor_ID': [], 'parent_element_ID': [], 'relation_type': [], 'child_actor_ID': [], 'child_element_ID': [], 'decomposition_type': [], 'contribution_value': []}

    # Check uniqueness of elements IDs
#     checkUniqueIDs(r_ID)

    for x in range(len(parent_actors_IDs)):
        contribution_value = ''
        r_ID = "R" + str(x)+ str(model_ID)
        table['relation_ID'].append(r_ID)
        table["parent_actor_ID"].append(parent_actors_IDs[x])
        table["parent_element_ID"].append(parent_elements_IDs[x])
        table["relation_type"].append(relation_types[x])
        table["child_actor_ID"].append(children_actors_IDs[x])
        table["child_element_ID"].append(children_elements_IDs[x])
        table["decomposition_type"].append(decomposition_types[x])
        table["contribution_value"].append(contribution_values[x])

    df_relations=pd.DataFrame.from_dict(table,orient='index').transpose()
    return df_relations

def convert_tgrl_to_csv(model_a, model_b):
    models_files = [model_a, model_b]
    df_list = []
    global input_model_a_name 
#    input_model_a_name = ""
    global input_model_b_name
#    input_model_b_name= ""
    global inputModels_file_name
#    inputModels_file_name = ""

    for f in range(len(models_files)):
#        print("--------- File Name", models_files[f])

        # Defining arrays for actors
        global a_models_name
        a_models_name = []
        global a_actors_ID
        a_actors_ID = []
        global actors_name
        actors_name = []
        global actors_description
        actors_description = []
        global actors_importance
        actors_importance = []
        global actors_metadata
        actors_metadata = []

        # Defining arrays for intentional elements
        global models_name
        models_name = []
        global actors_ID
        actors_ID = []
        global ielements_type
        ielements_type = []
        global ielements_ID
        ielements_ID = []
        global ielements_name
        ielements_name = []
        global ielements_description
        ielements_description = []
        global ielements_importance
        ielements_importance = []
        global ielements_metadata
        ielements_metadata = []
        global ielements_decompositionType
        ielements_decompositionType = []

        # Defining arrays for relations elements
        global parent_actors_IDs
        parent_actors_IDs = []
        global parent_elements_IDs
        parent_elements_IDs = []
        global relation_types
        relation_types = []
        global children_actors_IDs
        children_actors_IDs = []
        global children_elements_IDs
        children_elements_IDs = []
        global decomposition_types
        decomposition_types = []
        global contribution_values
        contribution_values = []


        # Contribution assets
        contribution_value = 0
        x = m = c = n = 0
        global contribution_pattern
        contribution_pattern = re.compile('hurt|break|make|help|someNegative|somePositive|[-|+]?[0-9]+')


        # Read the model file 
        # pass the file name as string
        lines = []
        flatList = []
        readModel(models_files[f])

        # Start preprocessing the sentences
        splitSentences()

        processStrings()

        processAttributes()

        processElements()

    #     processStrings()

        processRelationsForm()

        processList()

        for f in range(len(flatList)):
            flatList[f] = flatList[f].strip() #remove white spaces/tabs
    #         new_string = flatList[f].strip("'") 
            flatList[f] = re.split('({|}|;|,)', flatList[f]) #split the line based on { or } or ; and keep them
            flatList[f] = list(filter(None, flatList[f])) #remove empty strings
            flatList[f] = [i.strip() for i in flatList[f]] #remove white spaces around a string

        flatList = [ item for elem in flatList for item in elem] #convert the list of lists to a list

        processStrings()
#        print(flatList)
        # Start running all functions
        startParsing()

        df_actors = insertActors()
        df_list.append(df_actors)

        df_elements = insertElements()
        df_list.append(df_elements)

        df_relations = insertRelations(f)
        df_list.append(df_relations)
        
        if df_actors.empty and df_elements.empty:
            exit("Cannot perform integration. Please use two GRL models.")
        else:
            if f == 0:
                input_model_a_name = a_models_name[0]
            elif f == 1:
                input_model_b_name = a_models_name[0]

    # Store the dataframes in one excel file
    sheets = ['actors_a', 'elements_a', 'relations_a', 'actors_b', 'elements_b', 'relations_b']
    inputModels_file_name = 'inputModels_'+str(input_model_a_name)+'_'+str(input_model_b_name)+'.xlsx'
    dfs_tabs(df_list, sheets, inputModels_file_name)
#    return input_model_a_name, input_model_b_name
#    dfs_tabs(df_list, sheets, 'inputModels.xlsx')



# ----------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# ------------------------------------ GRL Merger ----------------------------------- #
# ----------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------- #


def startGRLMerger(model_a, model_b):
#    global model_1_name
#    model_1_name = ''
#    global model_2_name 
#    model_2_name = ''
    global input_model_a_name 
    input_model_a_name = ""
    global input_model_b_name
    input_model_b_name= ""
    
    global base_dummy_actor 
    base_dummy_actor = False 

    global new_dummy_actor 
    new_dummy_actor = False 
    
    global inputModels_file_name 
    inputModels_file_name = ""
    convert_tgrl_to_csv(model_a, model_b)
    # Dataframe to store the matched actors IDs and their matched Elements ID
    global matched_elements_df
    matched_elements_df = pd.DataFrame(columns=['m_actor_ID', 'm_element_ID', 'm_similarity'])
    ## Defining dataframes for the merged model
    global merged_model_df
    merged_model_df = pd.DataFrame(columns=['model_name','actor_ID', 'ielement_type', 'ielement_ID', 'ielement_name', 'ielement_description', 'ielement_importance', 'ielement_metadata', 'ielement_decomposition_type'])
    global merged_relations_df
    merged_relations_df = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
    global trace_conflict_df
    trace_conflict_df = pd.DataFrame(columns=['m_ID', 'conflict_type', 'actor_name', 'base_name', 'base_value', 'new_name', 'new_value', 'm_selected_value'])
    global trace_error_df
    trace_error_df = pd.DataFrame(columns=['m_ID', 'error_type', 'actor_name', 'solution', 'description'])

    
    global the_merged_actors
    the_merged_actors = pd.DataFrame(columns=['actor_1', 'actor_2', 'similarity'])

    global the_merged_elements
    the_merged_elements = pd.DataFrame(columns=['actor', 'element_1', 'element_2', 'similarity'])

    global the_merged_links
    the_merged_links = pd.DataFrame(columns=['parent_element_1', 'link_1', 'child_element_1', 'parent_element_2', 'link_2', 'child_element_2'])


    merged_constructs = []


    global t
    t = 0 # For temporary elements ID

    # Read files and process the dataframes/lists
#    global inputModels_file_name
#    file_name = 'inputModels.xlsx'

    # Ask the user which merging method
    print("Please select the merging method you want by entering its number.")
    print("1- Automatic Merging")
    print("2- Interactive Merging")
    while True:
        merging_method = input("1 | 2 :")
        try:
            merging_method = int(merging_method)
            if merging_method == 1 or merging_method == 2:
                break;
            else:
                print("Please enter a valid input (1 or 2)")
                continue;
        except ValueError:
            print("Please enter a valid input (1 or 2)")
        
#    merging_method = input("1 | 2 :")

    merging_method = str(merging_method)
    if merging_method == "1":
        # Read the models names
#        model_1_name, model_2_name = readModels(inputModels_file_name)

        # Ask the user to specify the base model
        print("Please select the base model that will be used for resolving conflicts by entering its number.")
        print("1-", input_model_a_name)
        print("2-", input_model_b_name)
        while True:
            base_model_number = input("1 | 2 :")
            try:
                base_model_number = int(base_model_number)
                if base_model_number == 1 or base_model_number == 2:
                    break;
                else:
                    print("Please enter a valid input (1 or 2)")
                    continue;
            except ValueError:
                print("Please enter a valid input (1 or 2)")


        manageData(inputModels_file_name, str(base_model_number))

        # Store the original siblings for later checking
        storeOriginalSiblings()

        print("--- Processing Actors ---")
        actorsSimilarityValues()
        semanticMatchActors(merging_method)

        mergeActors(merging_method)
        global merged_actors_df
        if len(merged_actors_df) == 0 and not base_dummy_actor and not new_dummy_actor:
            processUnmatchedActors()
            print("--- Processing Elements ---")
            processUnmatchedElements()
            print("--- Processing Links ---")
            processUnmatchedRelations()
            print("--- Resolve Cycles ---")
            checkDirectCycles(merging_method)
            checkIndirectCycles(merging_method)
            print("--- Refining Links ---")
            checkSiblingsRelations(merging_method)
        else:
            print("--- Processing Elements ---")
            elementsSimilarityValue()
            findElementsThreshold(merging_method)
            startMatchingElements()
            startMergingElements(merging_method)

            processUnmatchedActors()
            processUnmatchedElements()

            print("--- Processing Links ---")
            mergeRelations(merging_method)
            processUnmatchedRelations()

            print("--- Resolve Cycles ---")
            checkDirectCycles(merging_method)
            checkIndirectCycles(merging_method)

            print("--- Refining Links ---")
            checkSiblingsRelations(merging_method)

        #     print(merged_actors_df)
        #     print(merged_model_df)
        #     print(merged_relations_df)

    else:
#        model_1_name, model_2_name = readModels(inputModels_file_name)
#
#        manageData(inputModels_file_name, "2")
#
#        # Store the original siblings for later checking
#        storeOriginalSiblings()
#
#        print("--- Processing Actors ---")
#        actorsSimilarityValues()
#        semanticMatchActors(merging_method)
#        mergeActors(merging_method)
#
#
#        print("--- Processing Elements ---")
#        elementsSimilarityValue()
#        findElementsThreshold(merging_method)
#        startMatchingElements()
#        startMergingElements(merging_method)
#
#        processUnmatchedActors()
#        processUnmatchedElements()
#
#        print("--- Processing Links ---")
#        mergeRelations(merging_method)
#        processUnmatchedRelations()
#
#        print("--- Resolve Cycles ---")
#        checkDirectCycles(merging_method)
#        checkIndirectCycles(merging_method)
#
#        print("--- Refining Links ---")
#        checkSiblingsRelations(merging_method)

    #     print(merged_actors_df)
    #     print(merged_model_df)
    #     print(merged_relations_df)
        #################################################
#        model_1_name, model_2_name = readModels(inputModels_file_name)

        manageData(inputModels_file_name, "2")

        # Store the original siblings for later checking
        storeOriginalSiblings()

        print("--- Processing Actors ---")
        actorsSimilarityValues()
        semanticMatchActors(merging_method)
        mergeActors(merging_method)

        if len(merged_actors_df) == 0 and not base_dummy_actor and not new_dummy_actor:
            processUnmatchedActors()
            print("--- Processing Elements ---")
            processUnmatchedElements()
            print("--- Processing Links ---")
            processUnmatchedRelations()
            print("--- Resolve Cycles ---")
            checkDirectCycles(merging_method)
            checkIndirectCycles(merging_method)
            print("--- Refining Links ---")
            checkSiblingsRelations(merging_method)

        else:
            print("--- Processing Elements ---")
            elementsSimilarityValue()
            findElementsThreshold(merging_method)
            startMatchingElements()
            startMergingElements(merging_method)

            processUnmatchedActors()
            processUnmatchedElements()

            print("--- Processing Links ---")
            mergeRelations(merging_method)
            processUnmatchedRelations()

            print("--- Resolve Cycles ---")
            checkDirectCycles(merging_method)
            checkIndirectCycles(merging_method)

            print("--- Refining Links ---")
            checkSiblingsRelations(merging_method)
        
        
    print("Merging is completed.")
    cleanIDs()
    DFtoTGRL()
    
    # Save conflict cases
    downloadConflictCases()
    
    # Save merged constructs
    merged_constructs.append(the_merged_actors)
    merged_constructs.append(the_merged_elements)
    merged_constructs.append(the_merged_links)

    sheets = ['Merged Actors', 'Merged Intentional Elements', 'Merged Links']
    mergedConstruct_fileName = 'integratedConstructs_'+str(input_model_a_name)+"_"+str(input_model_b_name)+".xlsx"

    dfs_tabs(merged_constructs, sheets, mergedConstruct_fileName)
    

#def readModels(fileName):
#    global base_actors_df
#    actors_1_df = pd.DataFrame(columns=['model_name','actor_ID', 'actor_name', 'actor_description', 'actor_importance', 'actor_metadata'])
#
#    global new_actors_df
#    actors_2_df = pd.DataFrame(columns=['model_name','actor_ID', 'actor_name', 'actor_description', 'actor_importance', 'actor_metadata'])
#
#    actors_1_df = pd.read_excel(fileName, sheet_name='actors_a')
#    actors_1_df.fillna('', inplace=True)
#    actors_2_df = pd.read_excel(fileName, sheet_name='actors_b')
#    actors_2_df.fillna('', inplace=True)
#    
#    
##    if len(actors_1_df['model_name'].tolist()) == 0 or len(actors_2_df['model_name'].tolist()) == 0:
##        exit("Cannot perform integration. Please use two GRL models.")
##    else:
#    model_1_name = (actors_1_df['model_name'].unique().tolist())[0]
#    model_2_name = (actors_2_df['model_name'].unique().tolist())[0]
#
#    return model_1_name, model_2_name

    
def manageData(fileName, baseModelNumber):

    global base_actors_IDs 
    base_actors_IDs = []

    global base_actors_names
    base_actors_names = []

    global new_actors_IDs
    new_actors_IDs = []

    global new_actors_names
    new_actors_names = []

    global base_elements 
    base_elements = []
    
    global base_elements_IDs
    base_elements_ID = []

    global new_elements
    new_elements = []
    
    global new_elements_IDs
    new_elements_ID = []

    global base_actors_df
    base_actors_df = pd.DataFrame(columns=['model_name','actor_ID', 'actor_name', 'actor_description', 'actor_importance', 'actor_metadata'])

    global new_actors_df
    new_actors_df = pd.DataFrame(columns=['model_name','actor_ID', 'actor_name', 'actor_description', 'actor_importance', 'actor_metadata'])

    global base_dummy_actor 
    base_dummy_actor = False 
    
    global new_dummy_actor 
    new_dummy_actor = False 
    
    global base_model_df
    base_model_df = pd.DataFrame(columns=['model_name','actor_ID', 'ielement_type', 'ielement_ID', 'ielement_name', 'ielement_description', 'ielement_importance', 'ielement_metadata', 'ielement_descomposition_type'])

    global new_model_df
    new_model_df = pd.DataFrame(columns=['model_name','actor_ID', 'ielement_type', 'ielement_ID', 'ielement_name', 'ielement_description', 'ielement_importance', 'ielement_metadata', 'ielement_descomposition_type'])

    global base_relations_df
    base_relations_df = pd.DataFrame(columns=['relation_ID', 'parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])

    global new_relations_df
    new_relations_df = pd.DataFrame(columns=['relation_ID', 'parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])

    if baseModelNumber == "1":
        base_actors_df = pd.read_excel(fileName, sheet_name='actors_a')
        base_actors_df.fillna('', inplace=True)
        new_actors_df = pd.read_excel(fileName, sheet_name='actors_b')
        new_actors_df.fillna('', inplace=True)

        base_model_df = pd.read_excel(fileName, sheet_name='elements_a')
        base_model_df.fillna('', inplace=True)
        new_model_df = pd.read_excel(fileName, sheet_name='elements_b')
        new_model_df.fillna('', inplace=True)

        base_relations_df = pd.read_excel(fileName, sheet_name='relations_a')
        base_relations_df.fillna('', inplace=True)
        new_relations_df = pd.read_excel(fileName, sheet_name='relations_b')
        new_relations_df.fillna('', inplace=True)
        
    
    elif baseModelNumber == "2":
        base_actors_df = pd.read_excel(fileName, sheet_name='actors_b')
        base_actors_df.fillna('', inplace=True)
        new_actors_df = pd.read_excel(fileName, sheet_name='actors_a')
        new_actors_df.fillna('', inplace=True)

        base_model_df = pd.read_excel(fileName, sheet_name='elements_b')
        base_model_df.fillna('', inplace=True)
        new_model_df = pd.read_excel(fileName, sheet_name='elements_a')
        new_model_df.fillna('', inplace=True)

        base_relations_df = pd.read_excel(fileName, sheet_name='relations_b')
        base_relations_df.fillna('', inplace=True)
        new_relations_df = pd.read_excel(fileName, sheet_name='relations_a')
        new_relations_df.fillna('', inplace=True)
        
        
        
    for ba in range(len(base_actors_df)):
        if type(base_actors_df['actor_importance'][ba]) == float:
            base_actors_df['actor_importance'][ba] = int(base_actors_df['actor_importance'][ba])

    for na in range(len(new_actors_df)):
        if type(new_actors_df['actor_importance'][na]) == float:
            new_actors_df['actor_importance'][na] = int(new_actors_df['actor_importance'][na])

    for ba in range(len(base_model_df)):
        if type(base_model_df['ielement_importance'][ba]) == float:
            base_model_df['ielement_importance'][ba] = int(base_model_df['ielement_importance'][ba])

    for na in range(len(new_model_df)):
        if type(new_model_df['ielement_importance'][na]) == float:
            new_model_df['ielement_importance'][na] = int(new_model_df['ielement_importance'][na])

    for b in range(len(base_relations_df)):
        if type(base_relations_df['contribution_value'][b]) == float:
            base_relations_df['contribution_value'][b] = int(base_relations_df['contribution_value'][b])

    for n in range(len(new_relations_df)):
        if type(new_relations_df['contribution_value'][n]) == float:
            new_relations_df['contribution_value'][n] = int(new_relations_df['contribution_value'][n])

    checkUniqueness()
    # Drop duplicated actors (dummy could be duplicated)
    base_actors_df.drop_duplicates(subset ="actor_ID", inplace = True)
    # Reset index and drop the old index
    base_actors_df = base_actors_df.reset_index(drop = True)
    
    baseDummyActorIndex = base_actors_df[(base_actors_df['actor_ID'] == 'X#Y')].index
#    print("##############", baseDummyActorIndex)
    if len(baseDummyActorIndex) > 0: 
        base_actors_df.drop(baseDummyActorIndex , inplace=True)
        base_actors_df = base_actors_df.reset_index(drop = True)
        base_dummy_actor = True

    # Convert the actors DF to a list for comparison
    base_actors_IDs = base_actors_df['actor_ID'].to_list()
    base_actors_names = base_actors_df['actor_name'].to_list()

    new_actors_df.drop_duplicates(subset ="actor_ID", inplace = True)
    new_actors_df = new_actors_df.reset_index(drop = True)
    
    newDummyActorIndex = new_actors_df[(new_actors_df['actor_ID'] == 'X#Y')].index
#    print("##############", newDummyActorIndex)
    if len(newDummyActorIndex) > 0:
        new_actors_df.drop(newDummyActorIndex , inplace=True)
        new_actors_df = new_actors_df.reset_index(drop = True)
        new_dummy_actor = True

    new_actors_IDs = new_actors_df['actor_ID'].to_list()
    new_actors_names = new_actors_df['actor_name'].to_list() 

    base_elements = base_model_df['ielement_name'].to_list()
    base_elements_IDs = base_model_df['ielement_ID'].to_list()

    new_elements = new_model_df['ielement_name'].to_list()
    new_elements_IDs = new_model_df['ielement_ID'].to_list()
    
    preprocessing()


def preprocessing():
    global base_actors_names
    global new_actors_names
    global base_elements
    global new_elements
    
    for x in range(len(base_actors_names)):
        base_actors_names[x] = base_actors_names[x].lower()
        base_actors_names[x] = base_actors_names[x].replace(r"’", r"'")
        # Replace “ or ” to "
        base_actors_names[x] = base_actors_names[x].replace(r"“|”", r'"')
        # Replace the newline with .
        base_actors_names[x] = base_actors_names[x].replace("\n", ".")
        # Replace & to and
        base_actors_names[x] = base_actors_names[x].replace("&", "and")
        base_actors_names[x] = base_actors_names[x].replace(" u ", " you ")
        base_actors_names[x] = nfx.fix_contractions(base_actors_names[x])
        base_actors_names[x] = nfx.remove_puncts(base_actors_names[x])
        base_actors_names[x] = nfx.remove_special_characters(base_actors_names[x])
    
    tagged_base_actors = pos_tag_sents(map(word_tokenize, base_actors_names))

    for x in range(len(tagged_base_actors)):
        for y in range(len(tagged_base_actors[x])):
            token, tag = tagged_base_actors[x][y]
            if re.match(r'NN|NNS|NNPS|IN', tag): 
                tagged_base_actors[x][y] = (token, 'n')
            elif re.match(r'JJ|JJR|JJS|TO|DT|CC|(|)', tag):
                tagged_base_actors[x][y] = (token, 'a')
            elif re.match(r'VB|VBD|VBG|VBN|VBP|VBZ', tag):
                tagged_base_actors[x][y] = (token, 'v')
                
    for x in range(len(tagged_base_actors)):
        for y in range(len(tagged_base_actors[x])):
            token, tag = tagged_base_actors[x][y]
            lem_token = lemmatizer.lemmatize(token, tag)
            tagged_base_actors[x][y] = (lem_token, tag)
    
    base_actors_names = []            
    for i in range(len(tagged_base_actors)):
        base_actors_names.append(' '.join(map(lambda x: str(x[0]), tagged_base_actors[i])))
        
        
#------------------------------------------------------------
        
    for x in range(len(new_actors_names)):
        new_actors_names[x] = new_actors_names[x].lower()
        new_actors_names[x] = new_actors_names[x].replace(r"’", r"'")
        # Replace “ or ” to "
        new_actors_names[x] = new_actors_names[x].replace(r"“|”", r'"')
        # Replace the newline with .
        new_actors_names[x] = new_actors_names[x].replace("\n", ".")
        # Replace & to and
        new_actors_names[x] = new_actors_names[x].replace("&", "and")
        new_actors_names[x] = new_actors_names[x].replace(" u ", " you ")
        new_actors_names[x] = nfx.fix_contractions(new_actors_names[x])
        new_actors_names[x] = nfx.remove_puncts(new_actors_names[x])
        new_actors_names[x] = nfx.remove_special_characters(new_actors_names[x])  
        
    tagged_new_actors = pos_tag_sents(map(word_tokenize, new_actors_names))

    for x in range(len(tagged_new_actors)):
        for y in range(len(tagged_new_actors[x])):
            token, tag = tagged_new_actors[x][y]
            if re.match(r'NN|NNS|NNPS|IN', tag): 
                tagged_new_actors[x][y] = (token, 'n')
            elif re.match(r'JJ|JJR|JJS|TO|DT|CC|(|)', tag):
                tagged_new_actors[x][y] = (token, 'a')
            elif re.match(r'VB|VBD|VBG|VBN|VBP|VBZ', tag):
                tagged_new_actors[x][y] = (token, 'v')
    
    for x in range(len(tagged_new_actors)):
        for y in range(len(tagged_new_actors[x])):
            token, tag = tagged_new_actors[x][y]
            lem_token = lemmatizer.lemmatize(token, tag)
            tagged_new_actors[x][y] = (lem_token, tag)
    
    new_actors_names = []            
    for i in range(len(tagged_new_actors)):
        new_actors_names.append(' '.join(map(lambda x: str(x[0]), tagged_new_actors[i])))
        
# ------------------------------------------------------------------
    
    base_model_df['preprocessed_name'] = base_model_df['ielement_name'].str.lower()
    base_model_df['preprocessed_name'] = base_model_df['preprocessed_name'].str.replace(r"’", r"'")
    base_model_df['preprocessed_name'] = base_model_df['preprocessed_name'].str.replace(r"“|”", r'"')
    base_model_df['preprocessed_name'] = base_model_df['preprocessed_name'].str.replace("\n", ".")
    base_model_df['preprocessed_name'] = base_model_df['preprocessed_name'].str.replace("&", "and")
    base_model_df['preprocessed_name'] = base_model_df['preprocessed_name'].str.replace(" u ", " you ")
    for x in range(len(base_model_df)):
        base_model_df['preprocessed_name'][x] = nfx.fix_contractions(base_model_df['preprocessed_name'][x])
#         base_model_df['ielement_name'][x] = nfx.remove_puncts(base_model_df['ielement_name'][x])
        base_model_df['preprocessed_name'][x] = nfx.remove_special_characters(base_model_df['preprocessed_name'][x])
    
    tagged_base_elements = pos_tag_sents(map(word_tokenize, base_model_df['preprocessed_name']))

    for x in range(len(tagged_base_elements)):
        for y in range(len(tagged_base_elements[x])):
            token, tag = tagged_base_elements[x][y]
            if re.match(r'NN|NNS|NNPS|IN', tag): 
                tagged_base_elements[x][y] = (token, 'n')
            elif re.match(r'JJ|JJR|JJS|TO|DT|CC|(|)', tag):
                tagged_base_elements[x][y] = (token, 'a')
            elif re.match(r'VB|VBD|VBG|VBN|VBP|VBZ', tag):
                tagged_base_elements[x][y] = (token, 'v')
                
    
    for x in range(len(tagged_base_elements)):
        for y in range(len(tagged_base_elements[x])):
            token, tag = tagged_base_elements[x][y]
            lem_token = lemmatizer.lemmatize(token, tag)
            tagged_base_elements[x][y] = (lem_token, tag)
    
    for i in range(len(tagged_base_elements)):
        base_model_df['preprocessed_name'][i] = ' '.join(map(lambda x: str(x[0]), tagged_base_elements[i]))
        
        
#-----------------------------------------------------------
    
    new_model_df['preprocessed_name'] = new_model_df['ielement_name'].str.lower()
    new_model_df['preprocessed_name'] = new_model_df['preprocessed_name'].str.replace(r"’", r"'")
    new_model_df['preprocessed_name'] = new_model_df['preprocessed_name'].str.replace(r"“|”", r'"')
    new_model_df['preprocessed_name'] = new_model_df['preprocessed_name'].str.replace("\n", ".")
    new_model_df['preprocessed_name'] = new_model_df['preprocessed_name'].str.replace("&", "and")
    new_model_df['preprocessed_name'] = new_model_df['preprocessed_name'].str.replace(" u ", " you ")
    for x in range(len(new_model_df)):
        new_model_df['preprocessed_name'][x] = nfx.fix_contractions(new_model_df['preprocessed_name'][x])
#         new_model_df['ielement_name'][x] = nfx.remove_puncts(new_model_df['ielement_name'][x])
        new_model_df['preprocessed_name'][x] = nfx.remove_special_characters(new_model_df['preprocessed_name'][x])
    
    tagged_new_elements = pos_tag_sents(map(word_tokenize, new_model_df['preprocessed_name']))

    for x in range(len(tagged_new_elements)):
        for y in range(len(tagged_new_elements[x])):
            token, tag = tagged_new_elements[x][y]
            if re.match(r'NN|NNS|NNPS|IN', tag): 
                tagged_new_elements[x][y] = (token, 'n')
            elif re.match(r'JJ|JJR|JJS|TO|DT|CC|(|)', tag):
                tagged_new_elements[x][y] = (token, 'a')
            elif re.match(r'VB|VBD|VBG|VBN|VBP|VBZ', tag):
                tagged_new_elements[x][y] = (token, 'v')
                
    for x in range(len(tagged_new_elements)):
        for y in range(len(tagged_new_elements[x])):
            token, tag = tagged_new_elements[x][y]
            lem_token = lemmatizer.lemmatize(token, tag)
            tagged_new_elements[x][y] = (lem_token, tag)
    
    for i in range(len(tagged_new_elements)):
        new_model_df['preprocessed_name'][i] = ' '.join(map(lambda x: str(x[0]), tagged_new_elements[i]))
#         print(new_model_df['ielement_name'][i])

def checkUniqueness():
    # Uniqueness of actors
    base_actors_IDs = base_actors_df['actor_ID'].to_list()
    new_actors_IDs = new_actors_df['actor_ID'].to_list()
    for x in range(len(base_actors_IDs)):
        if base_actors_IDs[x] != 'X#Y':
            for y in range(len(new_actors_IDs)):
                if base_actors_IDs[x] == new_actors_IDs[y]:
                    value = randint(0, 99)
                    new_actors_df.loc[new_actors_df['actor_ID'] == new_actors_IDs[y], 'actor_ID'] = new_actors_IDs[y]+str(value)
                    new_model_df.loc[new_model_df['actor_ID'] == new_actors_IDs[y], 'actor_ID'] = new_actors_IDs[y]+str(value)
                    new_relations_df.loc[new_relations_df['parent_actor_ID'] == new_actors_IDs[y], 'parent_actor_ID'] = new_actors_IDs[y]+str(value)
                    new_relations_df.loc[new_relations_df['child_actor_ID'] == new_actors_IDs[y], 'child_actor_ID'] = new_actors_IDs[y]+str(value)

    # Uniqueness of elements
    base_elements_IDs = base_model_df['ielement_ID'].to_list()
    new_elements_IDs = new_model_df['ielement_ID'].to_list()
    for x in range(len(base_elements_IDs)):
        for y in range(len(new_elements_IDs)):
            if base_elements_IDs[x] == new_elements_IDs[y]:
                value = randint(0, 99)
                new_model_df.loc[new_model_df['ielement_ID'] == new_elements_IDs[y], 'ielement_ID'] = new_elements_IDs[y]+str(value)
                new_relations_df.loc[new_relations_df['parent_element_ID'] == new_elements_IDs[y], 'parent_element_ID'] = new_elements_IDs[y]+str(value)
                new_relations_df.loc[new_relations_df['child_element_ID'] == new_elements_IDs[y], 'child_element_ID'] = new_elements_IDs[y]+str(value)

    # Uniqueness of links
    base_relations_IDs = base_relations_df['relation_ID'].to_list()
    new_relations_IDs = new_relations_df['relation_ID'].to_list()
    for x in range(len(base_relations_IDs)):
        for y in range(len(new_relations_IDs)):
            if base_relations_IDs[x] == new_relations_IDs[y]:
                value = randint(0, 99)
                new_relations_df.loc[new_relations_df['relation_ID'] == new_relations_IDs[y], 'relation_ID'] = new_relations_IDs[y]+str(value)
                
# Function returns unmatched elements
# It should be run after getting the most matched elements
def findUnmatchedElements(matched_elements, base, new):
    for x in range(len(matched_elements)):
        if matched_elements[x] in base or matched_elements[x] in new:
            base.remove(matched_elements[x])
            new.remove(matched_elements[x])
        else:
            matches = re.split('\+', matched_elements[x])
            if matches[0] in base:
                base.remove(matches[0])
            if matches[1] in new:
                new.remove(matches[1])
    return base, new


def actorsSimilarityValues():  
    global actors_similarity_df

    actors_similarity_df = pd.DataFrame(columns=['base_actor_ID', 'base_actor_name', 'new_actor_ID', 'new_actor_name', 'similarity_value'])
    base_actors_vector_list = []
    new_actors_vector_list = []
    
    # Convert the base actors' names into vectors
    for b in range(len(base_actors_names)):
        base_actor_vector = SBERT.encode(base_actors_names[b], convert_to_tensor=True)
        base_actors_vector_list.append(base_actor_vector)

    # Convert the new actors' names into vectors
    for n in range(len(new_actors_names)):
        new_actor_vector = SBERT.encode(new_actors_names[n], convert_to_tensor=True)
        new_actors_vector_list.append(new_actor_vector)

    # Calculate the similarity value using cosine similarity index
    for bv in range(len(base_actors_vector_list)):
        for nv in range(len(new_actors_vector_list)):
            similarity_value = util.pytorch_cos_sim(base_actors_vector_list[bv], new_actors_vector_list[nv])
            actors_similarity_row = {'base_actor_ID': base_actors_IDs[bv], 'base_actor_name': base_actors_names[bv], 'new_actor_ID': new_actors_IDs[nv], 'new_actor_name': new_actors_names[nv],  'similarity_value': similarity_value.item()}
            actors_similarity_df = actors_similarity_df.append(actors_similarity_row, ignore_index=True)

    # Sort similarity values 
    actors_similarity_df = actors_similarity_df.sort_values('similarity_value', ascending=False)
    actors_similarity_df = actors_similarity_df.reset_index(drop=True)
    actors_similarity_df['similarity_value'] = actors_similarity_df['similarity_value'].convert_dtypes()

    if len(actors_similarity_df) > 0:
        print(tabulate(actors_similarity_df, headers = 'keys', tablefmt = 'psql'))

#    print("--------------")
#    print(actors_similarity_df)
    actors_similarity_df['similarity_value'] = np.around(actors_similarity_df['similarity_value'].astype(np.double),2)
    

def semanticMatchActors(mergingMethod):
    global matched_actors_df
    matched_actors_df = pd.DataFrame(columns=['actors', 'similarity'])
    global unmatched_base_actors
    global unmatched_new_actors
    global actors_similarity_df


    
    # Compare the similarity value with the threshold
    # for now it is a fixed threshold, later we will ask the user to specify it or will use some formula.
    loop_i = len(actors_similarity_df)
    # Variable to iterate through the similarity DF without exceeding the size
    counter = 0
    # Counter to iterate through the existing elements
    as_df = 0
    while counter < loop_i:
#         print("---", as_df)
        if actors_similarity_df['similarity_value'][as_df] == 1:
            counter = doMatchActors(as_df, counter)
        else:
            print("Does the actor (", actors_similarity_df['base_actor_name'][as_df], ") match the actor (", actors_similarity_df['new_actor_name'][as_df], ")?")
            print("1- Yes")
            print("2- No")
            while True:
                actors_matching = input("1 | 2:")
                try:
                    actors_matching = int(actors_matching)
                    if actors_matching == 1 or actors_matching == 2:
                        break;
                    else:
                        print("Please enter a valid input (1 or 2)")
                        continue;
                except ValueError:
                    print("Please enter a valid input (1 or 2)")
            
#            actors_matching = input("1 | 2:")
            if actors_matching == 1:
                counter = doMatchActors(as_df, counter)
            else:
                counter = counter + 1

        as_df = as_df+1


    unmatched_base_actors, unmatched_new_actors = findUnmatchedElements(matched_actors_df['actors'].tolist(), base_actors_IDs, new_actors_IDs)
    

def doMatchActors(as_df, counter):
    global actors_similarity_df    
    global matched_actors_df
    
    
    matchedActors = actors_similarity_df['base_actor_ID'][as_df] + '+' + actors_similarity_df['new_actor_ID'][as_df]

    the_matched_actor_row = {'actors': matchedActors, 'similarity': actors_similarity_df['similarity_value'][as_df]}
    matched_actors_df = matched_actors_df.append(the_matched_actor_row, ignore_index=True)
    
    
    counter = counter + 1

    # if the two elements are matched, we shall remove them from the similarity value df
    base_index_to_drop = actors_similarity_df[(actors_similarity_df['base_actor_ID'] == actors_similarity_df['base_actor_ID'][as_df]) & (actors_similarity_df['new_actor_ID'] != actors_similarity_df['new_actor_ID'][as_df])].index
    actors_similarity_df.drop(base_index_to_drop, inplace=True)
    actors_similarity_df = actors_similarity_df.reset_index(drop=True)
    counter = counter + len(base_index_to_drop)

    new_index_to_drop = actors_similarity_df[(actors_similarity_df['new_actor_ID'] == actors_similarity_df['new_actor_ID'][as_df]) & (actors_similarity_df['base_actor_ID'] != actors_similarity_df['base_actor_ID'][as_df])].index
    actors_similarity_df.drop(new_index_to_drop, inplace=True)
    actors_similarity_df = actors_similarity_df.reset_index(drop=True)
    counter = counter + len(new_index_to_drop)
    
    return counter 

    
def processUnmatchedActors():
    global merged_actors_df
    global unmatched_base_actors
    global unmatched_new_actors

    unmatched_base_actors_df = base_actors_df.loc[base_actors_df['actor_ID'].isin(unmatched_base_actors)].reset_index(drop=True)
    unmatched_new_actors_df = new_actors_df.loc[new_actors_df['actor_ID'].isin(unmatched_new_actors)].reset_index(drop=True)
    
    # If I use this line, the model name would be taken from the original models (not 'merged_model')
    merged_actors_df = merged_actors_df.append(unmatched_base_actors_df, ignore_index=True)
    merged_actors_df = merged_actors_df.append(unmatched_new_actors_df, ignore_index=True)
    

def mergeActors(mergingMethod):
    # Merging actors:
    global merged_actors_df
    merged_actors_df = pd.DataFrame(columns=['model_name','actor_ID', 'actor_name', 'actor_description', 'actor_importance', 'actor_metadata'])
    
    global the_merged_actors
    
    matched_actors = matched_actors_df['actors'].tolist()
    matched_actors_similarity = matched_actors_df['similarity'].tolist()


    for m in range(len(matched_actors)):

        matches = re.split('\+', matched_actors[m])
        base_actor = matches[0]
        new_actor = matches[1]

        # Get the index of the current base and new actors
        base_index = base_actors_df.index[base_actors_df['actor_ID'] == base_actor][0]
        new_index = new_actors_df.index[new_actors_df['actor_ID'] == new_actor][0]

        m_model_name = 'merged_model'
        m_actor_ID = matched_actors[m]
        
        # here we can change based on cosine similarity value
#         if base_actors_names[base_index] == new_actors_names[new_index]: 
            # Automatic filling of the merged actor information by the base actor information
        if mergingMethod == "1":
            # Get the type of the base element
            m_actor_name = base_actors_df['actor_name'][base_index]
            m_actor_description = base_actors_df['actor_description'][base_index]
            m_actor_importance = base_actors_df['actor_importance'][base_index]
            if not quantitativeImportanceValue(base_actors_df['actor_importance'][base_index], new_actors_df['actor_importance'][new_index]):
                traceConflict(m_actor_name, base_actors_df['actor_name'][base_index], base_actors_df['actor_importance'][base_index], new_actors_df['actor_name'][new_index], new_actors_df['actor_importance'][new_index], m_actor_importance, m_actor_ID, 'Actor Importance')

            m_actor_metadata = base_actors_df['actor_metadata'][base_index]
        elif mergingMethod == "2":
            if base_actors_df['actor_name'][base_index] != new_actors_df['actor_name'][new_index]:
                print("Select the name of the merged actor for the matched actors [", base_actors_df['actor_name'][base_index], "] with [", new_actors_df['actor_name'][new_index], "]")
                print("1- ", base_actors_df['actor_name'][base_index])
                print("2- ", new_actors_df['actor_name'][new_index])
                print("3- ", base_actors_df['actor_name'][base_index] + "/" + new_actors_df['actor_name'][new_index])
                
                while True:
                    actor_name_number = input("1 | 2 | 3 :")
                    try:
                        actor_name_number = int(actor_name_number)
                        if actor_name_number == 1 or actor_name_number == 2 or actor_name_number == 3:
                            break;
                        else:
                            print("Please enter a valid input (1 or 2 or 3)")
                            continue;
                    except ValueError:
                        print("Please enter a valid input (1 or 2 or 3)")
                
                if actor_name_number ==  1:
                    m_actor_name = base_actors_df['actor_name'][base_index]
                elif actor_name_number ==  2:
                    m_actor_name = new_actors_df['actor_name'][new_index]
                elif actor_name_number == 3:
                    m_actor_name = base_actors_df['actor_name'][base_index] + "/" + new_actors_df['actor_name'][new_index]
                traceConflict(m_actor_name, base_actors_df['actor_name'][base_index], '', new_actors_df['actor_name'][new_index], '', m_actor_name, m_actor_ID, 'Actor Name')

            else:
                m_actor_name = base_actors_df['actor_name'][base_index]

            # Merged Actor Description
            if base_actors_df['actor_description'][base_index]:
                if new_actors_df['actor_description'][new_index]:
                    # edit this condition later and add for it else
                    if base_actors_df['actor_description'][base_index] == new_actors_df['actor_description'][new_index]:
                        print("Select the description of the merged actor [", m_actor_name, "]")
                        print("1- ", base_actors_df['actor_description'][base_index])
                        print("2- ", new_actors_df['actor_description'][new_index])
                        print("3- Combine all:", base_actors_df['actor_description'][base_index]+ ". "+ new_actors_df['actor_description'][new_index])
                        while True:
                            actor_description_number = input("1 | 2 | 3 :")
                            try:
                                actor_description_number = int(actor_description_number)
                                if actor_description_number == 1 or actor_description_number == 2 or actor_description_number == 3:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2 or 3)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2 or 3)")
                        
                        if actor_description_number ==  1:
                            m_actor_description = base_actors_df['actor_description'][base_index]
                        elif actor_description_number ==  2:
                            m_actor_description = new_actors_df['actor_description'][new_index]
                        elif actor_description_number == 3:
                            m_actor_description = base_actors_df['actor_description'][base_index] + ". " + new_actors_df['actor_description'][new_index]
                        traceConflict(m_actor_name, base_actors_df['actor_name'][base_index], base_actors_df['actor_description'][base_index], new_actors_df['actor_name'][new_index], new_actors_df['actor_description'][new_index], m_actor_description, m_actor_ID, 'Actor Description')

                else:
                    print("Actor", base_actors_df['actor_name'][base_index], " has description \'", base_actors_df['actor_description'][base_index], "'")
                    print("Actor", new_actors_df['actor_name'][new_index], ' does not have description')
                    print("Select the description of the merged actor [", m_actor_name, "]")
                    print("1- ", base_actors_df['actor_description'][base_index])
                    print("2- Do not add description to the merged actor")
                    
                    while True:
                        actor_description_number = input("1 | 2 :")
                        try:
                            actor_description_number = int(actor_description_number)
                            if actor_description_number == 1 or actor_description_number == 2:
                                break;
                            else:
                                print("Please enter a valid input (1 or 2)")
                                continue;
                        except ValueError:
                            print("Please enter a valid input (1 or 2)")
                    
                    if actor_description_number ==  1:
                        m_actor_description = base_actors_df['actor_description'][base_index]
                    elif actor_description_number ==  2:
                        m_actor_description = ""
#                    m_actor_description = base_actors_df['actor_description'][base_index]
            else:
                if new_actors_df['actor_description'][new_index]:
                    print("Actor", base_actors_df['actor_name'][base_index], ' does not have description')
                    print("Actor", new_actors_df['actor_name'][new_index], " has description \'", new_actors_df['actor_description'][new_index])
                    print("Select the description of the merged actor [", m_actor_name, "]")
                    print("1- Do not add description to the merged actor")
                    print("2- ", new_actors_df['actor_description'][new_index])
                    while True:
                        actor_description_number = input("1 | 2 :")
                        try:
                            actor_description_number = int(actor_description_number)
                            if actor_description_number == 1 or actor_description_number == 2:
                                break;
                            else:
                                print("Please enter a valid input (1 or 2)")
                                continue;
                        except ValueError:
                            print("Please enter a valid input (1 or 2)")
                            
                    if actor_description_number ==  1:
                        m_actor_description = ""
                    elif actor_description_number ==  2:
                        m_actor_description = new_actors_df['actor_description'][new_index]
                else:
                    m_actor_description = ""
               


            # Merged Actor Importance
            if base_actors_df['actor_importance'][base_index]:
                if new_actors_df['actor_importance'][new_index]:
                    if not quantitativeImportanceValue(base_actors_df['actor_importance'][base_index], new_actors_df['actor_importance'][new_index]):
                        
                        print("Select the importance of the merged actor [", m_actor_name, "]")
                        print("1- ", base_actors_df['actor_importance'][base_index])
                        print("2- ", new_actors_df['actor_importance'][new_index])
                        while True:
                            actor_importance_number = input("1 | 2 :")
                            try:
                                actor_importance_number = int(actor_importance_number)
                                if actor_importance_number == 1 or actor_importance_number == 2:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2)")
                        
                        if actor_importance_number ==  1:
                            m_actor_importance = base_actors_df['actor_importance'][base_index]
                        elif actor_importance_number ==  2:
                            m_actor_importance = new_actors_df['actor_importance'][new_index]
                        traceConflict(m_actor_name, base_actors_df['actor_name'][base_index], base_actors_df['actor_importance'][base_index], new_actors_df['actor_name'][new_index], new_actors_df['actor_importance'][new_index], m_actor_importance, m_actor_ID, 'Actor Importance')
                    else:
                        m_actor_importance = base_actors_df['actor_importance'][base_index]
                else:
                    print("Actor", base_actors_df['actor_name'][base_index], " has importance value = \'",  base_actors_df['actor_importance'][base_index], "'")
                    print("Actor", new_actors_df['actor_name'][new_index], ' does not have importance value')
                    print("Select the importance value of the merged actor [", m_actor_name, "]")
                    print("1- ", base_actors_df['actor_importance'][base_index])
                    print("2- Do not add importance value to the merged actor")

                    while True:
                        actor_importance_number = input("1 | 2 :")
                        try:
                            actor_importance_number = int(actor_importance_number)
                            if actor_importance_number == 1 or actor_importance_number == 2:
                                break;
                            else:
                                print("Please enter a valid input (1 or 2)")
                                continue;
                        except ValueError:
                            print("Please enter a valid input (1 or 2)")

                    if actor_importance_number ==  1:
                        m_actor_importance = base_actors_df['actor_importance'][base_index]
                    elif actor_importance_number ==  2:
                        m_actor_importance = ""
            else:
                if new_actors_df['actor_importance'][new_index]:
                    print("Actor", base_actors_df['actor_name'][base_index], ' does not have importance value')
                    print("Actor", new_actors_df['actor_name'][new_index], " has importance value = ", new_actors_df['actor_importance'][new_index])
                    print("Select the importance value of the merged actor [", m_actor_name, "]")
                    print("1- Do not add importance value to the merged actor")
                    print("2- ", new_actors_df['actor_importance'][new_index])
                    while True:
                        actor_importance_number = input("1 | 2 :")
                        try:
                            actor_importance_number = int(actor_importance_number)
                            if actor_importance_number == 1 or actor_importance_number == 2:
                                break;
                            else:
                                print("Please enter a valid input (1 or 2)")
                                continue;
                        except ValueError:
                            print("Please enter a valid input (1 or 2)")
                            
                    if actor_importance_number ==  1:
                        m_actor_importance = ""
                    elif actor_importance_number ==  2:
                        m_actor_importance = new_actors_df['actor_importance'][new_index]    
#                    m_actor_importance = new_actors_df['actor_importance'][new_index]
                else:
                    m_actor_importance = ""


            # Merged Actor Metadata
            if base_actors_df['actor_metadata'][base_index]:
                if new_actors_df['actor_metadata'][new_index]:
                    # edit this condition later and add for it else
                    if base_actors_df['actor_metadata'][base_index] == new_actors_df['actor_metadata'][new_index]:
                        print("Select the metadata of the merged actor [", m_actor_name, "]")
                        print("1- ", base_actors_df['actor_metadata'][base_index])
                        print("2- ", new_actors_df['actor_metadata'][new_index])
                        print("3- Combine all:", base_actors_df['actor_metadata'][base_index] + ". " + new_actors_df['actor_metadata'][new_index])
                        while True:
                            actor_metadata_number = input("1 | 2 | 3 :")
                            try:
                                actor_metadata_number = int(actor_metadata_number)
                                if actor_metadata_number == 1 or actor_metadata_number == 2 or actor_metadata_number == 3:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2 or 3)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2 or 3)")
                        
                        if actor_metadata_number ==  1:
                            m_actor_metadata = base_actors_df['actor_metadata'][base_index]
                        elif actor_metadata_number ==  2:
                            m_actor_metadata = new_actors_df['actor_metadata'][new_index]
                        elif actor_metadata_number == 3:
                            m_actor_metadata = base_actors_df['actor_metadata'][base_index] + ". " + new_actors_df['actor_metadata'][new_index]
                        traceConflict(m_actor_name, base_actors_df['actor_name'][base_index], base_actors_df['actor_metadata'][base_index], new_actors_df['actor_name'][new_index], new_actors_df['actor_metadata'][new_index], m_actor_metadata, m_actor_ID, 'Actor Metadata')

                else:
                    print("Actor", base_actors_df['actor_name'][base_index], " has metadata: ",  base_actors_df['actor_metadata'][base_index])
                    print("Actor", new_actors_df['actor_name'][new_index], ' does not have metadata')
                    print("Select the metadata of the merged actor [", m_actor_name, "]")
                    print("1- ", base_actors_df['actor_metadata'][base_index])
                    print("2- Do not add metadata to the merged actor")

                    while True:
                        actor_metadata_number = input("1 | 2 :")
                        try:
                            actor_metadata_number = int(actor_metadata_number)
                            if actor_metadata_number == 1 or actor_metadata_number == 2:
                                break;
                            else:
                                print("Please enter a valid input (1 or 2)")
                                continue;
                        except ValueError:
                            print("Please enter a valid input (1 or 2)")

                    if actor_metadata_number ==  1:
                        m_actor_metadata = base_actors_df['actor_metadata'][base_index]
                    elif actor_metadata_number ==  2:
                        m_actor_metadata = ""
#                    m_actor_metadata = base_actors_df['actor_metadata'][base_index]

            else:
                if new_actors_df['actor_metadata'][new_index]:
                    print("Actor", base_actors_df['actor_name'][base_index], ' does not have metadata')
                    print("Actor", new_actors_df['actor_name'][new_index], " has metadata: ", new_actors_df['actor_metadata'][new_index])
                    print("Select the metadata of the merged actor [", m_actor_name, "]")
                    print("1- Do not add metadata to the merged actor")
                    print("2- ", new_actors_df['actor_metadata'][new_index])
                    while True:
                        actor_metadata_number = input("1 | 2 :")
                        try:
                            actor_metadata_number = int(actor_metadata_number)
                            if actor_metadata_number == 1 or actor_metadata_number == 2:
                                break;
                            else:
                                print("Please enter a valid input (1 or 2)")
                                continue;
                        except ValueError:
                            print("Please enter a valid input (1 or 2)")
                            
                    if actor_metadata_number ==  1:
                        m_actor_metadata = ""
                    elif actor_metadata_number ==  2:
                        m_actor_metadata = new_actors_df['actor_metadata'][new_index]    
                
#                    m_actor_metadata = new_actors_df['actor_metadata'][new_index]
                else:
                    m_actor_metadata = ""

        merged_actor_row = {'model_name': m_model_name,'actor_ID': m_actor_ID, 'actor_name': m_actor_name, 'actor_description': m_actor_description, 'actor_importance': m_actor_importance, 'actor_metadata': m_actor_metadata}
        merged_actors_df = merged_actors_df.append(merged_actor_row, ignore_index=True)

#        the_merged_actor_row = {'actor_1': base_actors_df['actor_name'][base_index], 'actor_2': new_actors_df['actor_name'][new_index]}
        
        the_merged_actor_row = {'actor_1': base_actors_df['actor_name'][base_index], 'actor_2': new_actors_df['actor_name'][new_index], 'similarity': matched_actors_similarity[m]}
        the_merged_actors = the_merged_actors.append(the_merged_actor_row, ignore_index=True)

        # Update the actor in the base model (elements)
        for b in range(len(base_model_df)):
            if base_model_df['actor_ID'][b] == base_actor:
                base_model_df.loc[b, ['actor_ID']] = matched_actors[m]
        # Update the actor in the base relations (parent and children)
        for br in range(len(base_relations_df)):
            if base_relations_df['parent_actor_ID'][br] == base_actor:
                base_relations_df.loc[br, ['parent_actor_ID']] = matched_actors[m]
            if base_relations_df['child_actor_ID'][br] == base_actor:
                base_relations_df.loc[br, ['child_actor_ID']] = matched_actors[m]

        # Update the actor in the new model (elements)
        for n in range(len(new_model_df)):
            if new_model_df['actor_ID'][n] == new_actor:
                new_model_df.loc[n, ['actor_ID']] = matched_actors[m]
        # Update the actor in the new relations (parent and children)
        for nr in range(len(new_relations_df)):
            if new_relations_df['parent_actor_ID'][nr] == new_actor:
                new_relations_df.loc[nr, ['parent_actor_ID']] = matched_actors[m]
            if new_relations_df['child_actor_ID'][nr] == new_actor:
                new_relations_df.loc[nr, ['child_actor_ID']] = matched_actors[m]
                         
                    
def startMatchingElements():
    # Dataframe to store the matched actors IDs and their matched Elements ID
    global matched_elements_df

    # Iterating through the merged actors' elements
    for ma in range(len(merged_actors_df)):
        # Get the elements from the two models of the merged actors
        base_elements_of_m_actor = pd.DataFrame(base_model_df.loc[base_model_df['actor_ID'] == merged_actors_df['actor_ID'][ma]])  
        new_elements_of_m_actor = pd.DataFrame(new_model_df.loc[new_model_df['actor_ID'] == merged_actors_df['actor_ID'][ma]])

        # Reset index for each actor's dataframe
        base_elements_of_m_actor = base_elements_of_m_actor.reset_index(drop=True)
        new_elements_of_m_actor = new_elements_of_m_actor.reset_index(drop=True)

        # Send them to matching function
        semanticMatchingElements(merged_actors_df['actor_ID'][ma], base_elements_of_m_actor, new_elements_of_m_actor)
    
    if base_dummy_actor:
        if new_dummy_actor:
            base_elements_of_dummy_actor = pd.DataFrame(base_model_df.loc[base_model_df['actor_ID'] == 'X#Y']).reset_index(drop=True)  
            new_elements_of_dummy_actor = pd.DataFrame(new_model_df.loc[new_model_df['actor_ID'] == 'X#Y']).reset_index(drop=True) 
            semanticMatchingElements('X#Y', base_elements_of_dummy_actor, new_elements_of_dummy_actor)
            
            
def elementsSimilarityValue():
    global all_elements_similarity_df
    all_elements_similarity_df = pd.DataFrame(columns=['m_actor_ID', 'm_actor_name', 'base_element_ID', 'base_element_name', 'new_element_ID', 'new_element_name', 'similarity_value'])
    
    if base_dummy_actor and new_dummy_actor:
        base_elements_vector_list = []
        new_elements_vector_list = []
        
        base_elements_of_dummy_actor = pd.DataFrame(base_model_df.loc[base_model_df['actor_ID'] == 'X#Y']).reset_index(drop=True)  
        new_elements_of_dummy_actor = pd.DataFrame(new_model_df.loc[new_model_df['actor_ID'] == 'X#Y']).reset_index(drop=True) 
        
        if not base_elements_of_dummy_actor.empty and not new_elements_of_dummy_actor.empty:
            for bd in range(len(base_elements_of_dummy_actor)):
                base_element_dummy_vector = SBERT.encode(base_elements_of_dummy_actor['preprocessed_name'][bd], convert_to_tensor=True)
                base_elements_vector_list.append(base_element_dummy_vector)

            for nd in range(len(new_elements_of_dummy_actor)):
                new_element_dummy_vector = SBERT.encode(new_elements_of_dummy_actor['preprocessed_name'][nd], convert_to_tensor=True)
                new_elements_vector_list.append(new_element_dummy_vector)

            # Calculate the similarity value using cosine similarity index
            for bv in range(len(base_elements_vector_list)):
                for nv in range(len(new_elements_vector_list)):
                    similarity_value = util.pytorch_cos_sim(base_elements_vector_list[bv], new_elements_vector_list[nv])
                    elements_similarity_row = {'m_actor_ID': 'X#Y', 'm_actor_name': 'X#YDUMMYACTOR', 'base_element_ID': base_elements_of_dummy_actor['ielement_ID'][bv], 'base_element_name': base_elements_of_dummy_actor['ielement_name'][bv], 'new_element_ID': new_elements_of_dummy_actor['ielement_ID'][nv], 'new_element_name': new_elements_of_dummy_actor['ielement_name'][nv], 'similarity_value': similarity_value.item()}
                    all_elements_similarity_df = all_elements_similarity_df.append(elements_similarity_row, ignore_index=True)

        

    for ma in range(len(merged_actors_df)):
        base_elements_vector_list = []
        new_elements_vector_list = []
        # Get the elements from the two models of the merged actors
        base_model_current_actor = pd.DataFrame(base_model_df.loc[base_model_df['actor_ID'] == merged_actors_df['actor_ID'][ma]])  
        new_model_current_actor = pd.DataFrame(new_model_df.loc[new_model_df['actor_ID'] == merged_actors_df['actor_ID'][ma]])
        base_model_current_actor = base_model_current_actor.reset_index(drop=True)
        new_model_current_actor = new_model_current_actor.reset_index(drop=True)

        
        if not base_model_current_actor.empty and not new_model_current_actor.empty:
            # Convert the base elements' names into vectors
            for b in range(len(base_model_current_actor)):
                base_element_vector = SBERT.encode(base_model_current_actor['preprocessed_name'][b], convert_to_tensor=True)
                base_elements_vector_list.append(base_element_vector)

            # Convert the new elements' names into vectors
            for n in range(len(new_model_current_actor)):
                new_element_vector = SBERT.encode(new_model_current_actor['preprocessed_name'][n], convert_to_tensor=True)
                new_elements_vector_list.append(new_element_vector)

            # Calculate the similarity value using cosine similarity index
            for bv in range(len(base_elements_vector_list)):
                for nv in range(len(new_elements_vector_list)):
                    similarity_value = util.pytorch_cos_sim(base_elements_vector_list[bv], new_elements_vector_list[nv])
                    elements_similarity_row = {'m_actor_ID': merged_actors_df['actor_ID'][ma], 'm_actor_name': merged_actors_df['actor_name'][ma], 'base_element_ID': base_model_current_actor['ielement_ID'][bv], 'base_element_name': base_model_current_actor['ielement_name'][bv], 'new_element_ID': new_model_current_actor['ielement_ID'][nv], 'new_element_name': new_model_current_actor['ielement_name'][nv], 'similarity_value': similarity_value.item()}
                    all_elements_similarity_df = all_elements_similarity_df.append(elements_similarity_row, ignore_index=True)

    all_elements_similarity_df = all_elements_similarity_df.sort_values('similarity_value', ascending=False)
    all_elements_similarity_df = all_elements_similarity_df.reset_index(drop=True)
    all_elements_similarity_df['similarity_value'] = np.around(all_elements_similarity_df['similarity_value'].astype(np.double),2)


def findElementsThreshold(mergingMethod):
    global elementsThreshold
    global input_model_a_name
    global input_model_b_name
    global base_dummy_actor
    global new_dummy_actor
    
    print_elements = False

    for ma in range(len(merged_actors_df)):
        rslt_df = all_elements_similarity_df[all_elements_similarity_df['m_actor_ID'] == merged_actors_df['actor_ID'][ma]]
        rslt_df = rslt_df.reset_index(drop=True)
        if len(rslt_df) > 0:
            print("Actor:", merged_actors_df['actor_name'][ma])
            print_elements = True
            rslt_df = rslt_df[['m_actor_name', 'base_element_name', 'new_element_name', 'similarity_value']]
            rslt_df.columns = ["Actor Name", str(input_model_a_name), str(input_model_b_name), "Similarity Value"]
    #         print(rslt_df.head(25))
            print(tabulate(rslt_df.head(25), headers = 'keys', tablefmt = 'psql'))
        
    if base_dummy_actor and new_dummy_actor:
        print("Intentional Elements with no Actors")
        rslt_df = all_elements_similarity_df[all_elements_similarity_df['m_actor_ID'] == 'X#Y']
        rslt_df = rslt_df.reset_index(drop=True)
        rslt_df = rslt_df[['m_actor_name', 'base_element_name', 'new_element_name', 'similarity_value']]
        rslt_df.columns = ["Actor Name", str(input_model_a_name), str(input_model_b_name), "Similarity Value"]
        print(tabulate(rslt_df.head(25), headers = 'keys', tablefmt = 'psql'))
       
    if (len(merged_actors_df) > 0 and print_elements) or (base_dummy_actor and new_dummy_actor):
        print("Specify the threshold value")
        while True:
            elementsThreshold = input()
            try:
                elementsThreshold = float(elementsThreshold)
                if elementsThreshold > 0 and elementsThreshold <= 1:
                    break;
                else:
                    print("Please enter a valid input (between 0 and 1)")
                    continue;
            except ValueError:
                    print("Please enter a valid input (int or float)")

    
def startMatchingElements():
    # Dataframe to store the matched actors IDs and their matched Elements ID
    global matched_elements_df
    matched_elements_df = pd.DataFrame(columns=['m_actor_ID', 'm_element_ID', 'm_similarity'])

    # Iterating through the merged actors' elements
    for ma in range(len(merged_actors_df)):
        # Get the elements from the two models of the merged actors
        base_elements_of_m_actor = pd.DataFrame(base_model_df.loc[base_model_df['actor_ID'] == merged_actors_df['actor_ID'][ma]])  
        new_elements_of_m_actor = pd.DataFrame(new_model_df.loc[new_model_df['actor_ID'] == merged_actors_df['actor_ID'][ma]])

        # Reset index for each actor's dataframe
        base_elements_of_m_actor = base_elements_of_m_actor.reset_index(drop=True)
        new_elements_of_m_actor = new_elements_of_m_actor.reset_index(drop=True)

        # Send them to matching function
        semanticMatchingElements(merged_actors_df['actor_ID'][ma], base_elements_of_m_actor, new_elements_of_m_actor)
    
    if base_dummy_actor:
        if new_dummy_actor:
            base_elements_of_dummy_actor = pd.DataFrame(base_model_df.loc[base_model_df['actor_ID'] == 'X#Y']).reset_index(drop=True)  
            new_elements_of_dummy_actor = pd.DataFrame(new_model_df.loc[new_model_df['actor_ID'] == 'X#Y']).reset_index(drop=True) 
            semanticMatchingElements('X#Y', base_elements_of_dummy_actor, new_elements_of_dummy_actor)
            
            
    
def semanticMatchingElements(actor_ID, base_model_df, new_model_df):
    
    global matched_elements_df
    global elements_similarity_df
    global elementsThreshold

    elements_similarity_df = pd.DataFrame(columns=['base_element_ID','new_element_ID', 'similarity_value'])
    base_elements_vector_list = []
    new_elements_vector_list = []
    
    # Convert the base elements' names into vectors
    for b in range(len(base_model_df)):
        base_element_vector = SBERT.encode(base_model_df['preprocessed_name'][b], convert_to_tensor=True)
        base_elements_vector_list.append(base_element_vector)

    # Convert the new elements' names into vectors
    for n in range(len(new_model_df)):
        new_element_vector = SBERT.encode(new_model_df['preprocessed_name'][n], convert_to_tensor=True)
        new_elements_vector_list.append(new_element_vector)

    # Calculate the similarity value using cosine similarity index
    for bv in range(len(base_elements_vector_list)):
        for nv in range(len(new_elements_vector_list)):
            similarity_value = util.pytorch_cos_sim(base_elements_vector_list[bv], new_elements_vector_list[nv])
            elements_similarity_row = {'base_element_ID': base_model_df['ielement_ID'][bv],'new_element_ID': new_model_df['ielement_ID'][nv], 'similarity_value': similarity_value.item()}
            elements_similarity_df = elements_similarity_df.append(elements_similarity_row, ignore_index=True)

    # Sort similarity values 
    elements_similarity_df = elements_similarity_df.sort_values('similarity_value', ascending=False)
    elements_similarity_df = elements_similarity_df.reset_index(drop=True)
    elements_similarity_df['similarity_value'] = np.around(elements_similarity_df['similarity_value'].astype(np.double),2)

    # Compare the similarity value with the threshold
    # for now it is a fixed threshold, later we will ask the user to specify it or will use some formula.
    loop_i = len(elements_similarity_df)
    # Variable to iterate through the similarity DF without exceeding the size
    counter = 0
    # Counter to iterate through the existing elements
    as_df = 0
    while counter < loop_i:
#         print("---", as_df)
#         print(elements_similarity_df['similarity_value'][as_df])
        if elements_similarity_df['similarity_value'][as_df] >= elementsThreshold:
            matchedElementsID = str(elements_similarity_df['base_element_ID'][as_df]) + '+' + str(elements_similarity_df['new_element_ID'][as_df])
            matched_elements_row = {'m_actor_ID': actor_ID, 'm_element_ID': matchedElementsID, 'm_similarity': elements_similarity_df['similarity_value'][as_df]}
            matched_elements_df = matched_elements_df.append(matched_elements_row, ignore_index=True)
            counter = counter + 1

            # if the two elements are matched, we shall remove them from the similarity value df
            base_index_to_drop = elements_similarity_df[(elements_similarity_df['base_element_ID'] == elements_similarity_df['base_element_ID'][as_df]) & (elements_similarity_df['new_element_ID'] != elements_similarity_df['new_element_ID'][as_df])].index
            elements_similarity_df.drop(base_index_to_drop, inplace=True)
            elements_similarity_df = elements_similarity_df.reset_index(drop=True)
            counter = counter + len(base_index_to_drop)

            new_index_to_drop = elements_similarity_df[(elements_similarity_df['new_element_ID'] == elements_similarity_df['new_element_ID'][as_df]) & (elements_similarity_df['base_element_ID'] != elements_similarity_df['base_element_ID'][as_df])].index
            elements_similarity_df.drop(new_index_to_drop, inplace=True)
            elements_similarity_df = elements_similarity_df.reset_index(drop=True)
            counter = counter + len(new_index_to_drop)
        else:
            counter = counter + 1
        as_df = as_df+1
    
    
        
def startMergingElements(mergingMethod):
    global merged_actors_df
    global merged_model_df
    global the_merged_elements

    for me in range(len(matched_elements_df)):
    # This step to start with parent elements, after merging we will be checking if there are not visited elements because they are not parents
#         if matched_elements_df['m_visited'][me] == 'false':

        m_model_name = 'merged_model'
        m_actor = matched_elements_df['m_actor_ID'][me]
        if m_actor == 'X#Y':
            m_actor_name = 'X#YDUMMYACTOR'
        else:
            m_actor_name =  merged_actors_df.loc[merged_actors_df['actor_ID'] == m_actor, 'actor_name'].iloc[0]
            
        matches = re.split('\+', matched_elements_df['m_element_ID'][me])
        base_element_ID = matches[0]
        new_element_ID = matches[1]

        m_element_ID = base_element_ID + '+' + new_element_ID
        # Get the entire row of the matched element using its ID and actor's ID
        base_element_df = pd.DataFrame(base_model_df.loc[(base_model_df['ielement_ID'] == base_element_ID) & (base_model_df['actor_ID'] == m_actor)])  
        new_element_df = pd.DataFrame(new_model_df.loc[(new_model_df['ielement_ID'] == new_element_ID) & (new_model_df['actor_ID'] == m_actor)])

        #print(base_element_df)
        #print(new_element_df)

        if not base_element_df.empty and not new_element_df.empty:
            if mergingMethod == "1":
                # This condition just to record the conflict and its automatic resolution
                if base_element_df['ielement_type'].item() != new_element_df['ielement_type'].item():
                    traceConflict(m_actor_name, base_element_df['ielement_name'].item(), base_element_df['ielement_type'].item(), new_element_df['ielement_name'].item(), new_element_df['ielement_type'].item(), base_element_df['ielement_type'].item(), m_element_ID, 'Element Type')

                # Get the attributes of the base element for the merged element
                m_element_type = base_element_df['ielement_type'].item()
                m_element_name = base_element_df['ielement_name'].item()
                m_element_description = base_element_df['ielement_description'].item()
                m_element_metadata = base_element_df['ielement_metadata'].item()
                m_element_importance = base_element_df['ielement_importance'].item()
                if not quantitativeImportanceValue(base_element_df['ielement_importance'].item(), new_element_df['ielement_importance'].item()):
                    traceConflict(m_actor_name, base_element_df['ielement_name'].item(), base_element_df['ielement_importance'].item(), new_element_df['ielement_name'].item(), new_element_df['ielement_importance'].item(), m_element_importance, m_element_ID, 'Element Importance')

                m_element_decomposition_type = base_element_df['ielement_decomposition_type'].item()
            elif mergingMethod == "2":
                # Check the type of the matched elements
                if base_element_df['ielement_type'].item() != new_element_df['ielement_type'].item():
                    print("Conflict in the type of the matched elements: [", base_element_df['ielement_name'].item(), "] with [", new_element_df['ielement_name'].item(), "]")
                    print("1- The element", base_element_df['ielement_name'].item(), "has the type", base_element_df['ielement_type'].item())
                    print("2- The element", new_element_df['ielement_name'].item(), "has the type", new_element_df['ielement_type'].item())  
                    print("Select the type of the matched elements: [", base_element_df['ielement_name'].item(), "] with [", new_element_df['ielement_name'].item(), "]")
                    print("1-", base_element_df['ielement_type'].item())
                    print("2-", new_element_df['ielement_type'].item())
                    while True: 
                        element_type_number = input("1 | 2 :")
                        try:
                            element_type_number = int(element_type_number)
                            if element_type_number == 1 or element_type_number == 2:
                                break;
                            else:
                                print("Please enter a valid input (1 or 2)")
                                continue;
                        except ValueError:
                            print("Please enter a valid input (1 or 2)")
                    if element_type_number ==  1:
                        m_element_type = base_element_df['ielement_type'].item()
                    elif element_type_number ==  2:
                        m_element_type = new_element_df['ielement_type'].item()
                    traceConflict(m_actor_name, base_element_df['ielement_name'].item(), base_element_df['ielement_type'].item(), new_element_df['ielement_name'].item(), new_element_df['ielement_type'].item(), m_element_type, m_element_ID, 'Element Type')

                else:
                    # Take any one of them
                    m_element_type = base_element_df['ielement_type'].item()
                    
                # Merged Element Name
                if int(matched_elements_df['m_similarity'][me]) != 1:
                    print("Select the name of the merged element of the matched elements [", base_element_df['ielement_name'].item(), "] with [", new_element_df['ielement_name'].item(), "]")
                    print("1- ", base_element_df['ielement_name'].item())
                    print("2- ", new_element_df['ielement_name'].item())
                    print("3- ", base_element_df['ielement_name'].item() + "/" + new_element_df['ielement_name'].item())
                    while True:
                        element_name_number = input("1 | 2 | 3 :")
                        try:
                            element_name_number = int(element_name_number)
                            if element_name_number == 1 or element_name_number == 2 or element_name_number == 3:
                                break;
                            else:
                                print("Please enter a valid input (1 or 2 or 3)")
                                continue;
                        except ValueError:
                            print("Please enter a valid input (1 or 2 or 3)")
                    
                    
                    if element_name_number ==  1:
                        m_element_name = base_element_df['ielement_name'].item()
                    elif element_name_number ==  2:
                        m_element_name = new_element_df['ielement_name'].item()
                    elif element_name_number == 3:
                        m_element_name = base_element_df['ielement_name'].item() + "/" + new_element_df['ielement_name'].item()
                    traceConflict(m_actor_name, base_element_df['ielement_name'].item(), base_element_df['ielement_name'].item(), new_element_df['ielement_name'].item(), new_element_df['ielement_name'].item(), m_element_name, m_element_ID, 'Element Name')

                else:
                    m_element_name = base_element_df['ielement_name'].item()
                
                # Merged Element Description
                if base_element_df['ielement_description'].item():
                    if new_element_df['ielement_description'].item():
                        # edit this condition later and add for it else
                        if base_element_df['ielement_description'].item() != new_element_df['ielement_description'].item():
                            print("Select the description of the merged element [", m_element_name, "]")
                            print("1- ",  base_element_df['ielement_description'].item())
                            print("2- ", new_element_df['ielement_description'].item())
                            print("3- Combine all:",  base_element_df['ielement_description'].item()+ ". "+ new_element_df['ielement_description'].item())
                            while True:
                                element_description_number = input("1 | 2 | 3 :")
                                try:
                                    element_description_number = int(element_description_number)
                                    if element_description_number == 1 or element_description_number == 2 or element_description_number == 3:
                                        break;
                                    else:
                                        print("Please enter a valid input (1 or 2 or 3)")
                                        continue;
                                except ValueError:
                                    print("Please enter a valid input (1 or 2 or 3)")
                            
                            if element_description_number ==  1:
                                m_element_description = base_element_df['ielement_description'].item()
                            elif element_description_number ==  2:
                                m_element_description = new_element_df['ielement_description'].item()
                            elif element_description_number == 3:
                                m_element_description = base_element_df['ielement_description'].item() + ". " + new_element_df['ielement_description'].item()
                            traceConflict(m_actor_name, base_element_df['ielement_name'].item(), base_element_df['ielement_description'].item(), new_element_df['ielement_name'].item(), new_element_df['ielement_description'].item(), m_element_description, m_element_ID, 'Element Description')
                        else: # identical description
                            m_element_description = base_element_df['ielement_description'].item()

                    else:
                        print("Intentional element ", base_element_df['ielement_name'].item(), " has description \'", base_element_df['ielement_description'].item(), "'")
                        print("Intentional element ", new_element_df['ielement_name'].item(), ' does not have description')
                        print("Select the description of the merged intentional element [", m_element_name, "]")
                        print("1- ", base_element_df['ielement_description'].item())
                        print("2- Do not add description to the merged intentional elements")

                        while True:
                            element_description_number = input("1 | 2 :")
                            try:
                                element_description_number = int(element_description_number)
                                if element_description_number == 1 or element_description_number == 2:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2)")

                        if element_description_number ==  1:
                            m_element_description = base_element_df['ielement_description'].item()
                        elif element_description_number ==  2:
                            m_element_description = ""
                else:
                    if new_element_df['ielement_description'].item():
                        print("Intentional element ", base_element_df['ielement_name'].item(), " does not have description")
                        print("Intentional element ", new_element_df['ielement_name'].item(), "  has description \'", new_element_df['ielement_description'].item(), "'")
                        print("Select the description of the merged intentional element [", m_element_name, "]")
                        print("1- Do not add description to the merged intentional elements")
                        print("2- ", new_element_df['ielement_description'].item())

                        while True:
                            element_description_number = input("1 | 2 :")
                            try:
                                element_description_number = int(element_description_number)
                                if element_description_number == 1 or element_description_number == 2:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2)")

                        if element_description_number ==  1:
                            m_element_description = ""
                        elif element_description_number ==  2:
                            m_element_description = new_element_df['ielement_description'].item()
                    else:
                        m_element_description = ""

                # Merged Element Importance
                if base_element_df['ielement_importance'].item():
                    if new_element_df['ielement_importance'].item():
                        if not quantitativeImportanceValue(base_element_df['ielement_importance'].item(), new_element_df['ielement_importance'].item()):
                            print("Select the importance of the merged element [", m_element_name, "]")
                            print("1- ", base_element_df['ielement_importance'].item())
                            print("2- ", new_element_df['ielement_importance'].item())
                            
                            while True:
                                element_importance_number = input("1 | 2 :")
                                try:
                                    element_importance_number = int(element_importance_number)
                                    if element_importance_number == 1 or element_importance_number == 2:
                                        break;
                                    else:
                                        print("Please enter a valid input (1 or 2)")
                                        continue;
                                except ValueError:
                                    print("Please enter a valid input (1 or 2)")
                            
                            if element_importance_number ==  1:
                                m_element_importance = base_element_df['ielement_importance'].item()
                            elif element_importance_number ==  2:
                                m_element_importance = new_element_df['ielement_importance'].item()
                            
                            traceConflict(m_actor_name, base_element_df['ielement_name'].item(), base_element_df['ielement_importance'].item(), new_element_df['ielement_name'].item(), new_element_df['ielement_importance'].item(), m_element_importance, m_element_ID, 'Element Importance')
                        else:
                            m_element_importance = base_element_df['ielement_importance'].item()
                    else:
                        print("Intentional element ", base_element_df['ielement_name'].item(), " has importance value =", base_element_df['ielement_importance'].item())
                        print("Intentional element ", new_element_df['ielement_name'].item(), ' does not have importance value')
                        print("Select the importance value of the merged intentional element [", m_element_name, "]")
                        print("1- ", base_element_df['ielement_importance'].item())
                        print("2- Do not add importance value to the merged intentional elements")

                        while True:
                            element_importance_number = input("1 | 2 :")
                            try:
                                element_importance_number = int(element_importance_number)
                                if element_importance_number == 1 or element_importance_number == 2:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2)")

                        if element_importance_number ==  1:
                            m_element_importance = base_element_df['ielement_importance'].item()
                        elif element_importance_number ==  2:
                            m_element_importance = ""
                else:
                    if new_element_df['ielement_importance'].item():
                        print("Intentional element ", base_element_df['ielement_name'].item(), " does not have importance value")
                        print("Intentional element ", new_element_df['ielement_name'].item(), "  has importance value =", new_element_df['ielement_importance'].item())
                        print("Select the importance value of the merged intentional element [", m_element_name, "]")
                        print("1- Do not add importance value to the merged intentional elements")
                        print("2- ", new_element_df['ielement_importance'].item())

                        while True:
                            element_importance_number = input("1 | 2 :")
                            try:
                                element_importance_number = int(element_importance_number)
                                if element_importance_number == 1 or element_importance_number == 2:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2)")

                        if element_importance_number ==  1:
                            m_element_importance = ""
                        elif element_importance_number ==  2:
                            m_element_importance = new_element_df['ielement_importance'].item()
                    else:
                        m_element_importance = ""



                # Merged Element Metadata
                if base_element_df['ielement_metadata'].item():
                    if new_element_df['ielement_metadata'].item():
                        # edit this condition later and add for it else
                        if base_element_df['ielement_metadata'].item() != new_element_df['ielement_metadata'].item():
                            print("Select the metadata of the merged element [", m_element_name, "]")
                            print("1- ", base_element_df['ielement_metadata'].item())
                            print("2- ", new_element_df['ielement_metadata'].item())
                            print("3- Combine all:", base_element_df['ielement_metadata'].item() + ". " + new_element_df['ielement_metadata'].item())
                            while True:
                                element_metadata_number = input("1 | 2 | 3 :")
                                try:
                                    element_metadata_number = int(element_metadata_number)
                                    if element_metadata_number == 1 or element_metadata_number == 2 or element_metadata_number == 3:
                                        break;
                                    else:
                                        print("Please enter a valid input (1 or 2 or 3)")
                                        continue;
                                except ValueError:
                                    print("Please enter a valid input (1 or 2 or 3)")
                            
                            if element_metadata_number ==  1:
                                m_element_metadata = base_element_df['ielement_metadata'].item()
                            elif element_metadata_number ==  2:
                                m_element_metadata = new_element_df['ielement_metadata'].item()
                            elif element_metadata_number == 3:
                                m_element_metadata = base_element_df['ielement_metadata'].item() + ". " + new_element_df['ielement_metadata'].item()
                            traceConflict(m_actor_name, base_element_df['ielement_name'].item(), base_element_df['ielement_metadata'].item(), new_element_df['ielement_name'].item(), new_element_df['ielement_metadata'].item(), m_element_metadata, m_element_ID, 'Element Metadata')
                        else:
                            m_element_metadata = base_element_df['ielement_metadata'].item()

                    else:
                        print("Intentional element ", base_element_df['ielement_name'].item(), " has metadata:", base_element_df['ielement_metadata'].item())
                        print("Intentional element ", new_element_df['ielement_name'].item(), ' does not have metadata')
                        print("Select the importance value of the merged intentional element [", m_element_name, "]")
                        print("1- ", base_element_df['ielement_metadata'].item())
                        print("2- Do not add metadata to the merged intentional elements")

                        while True:
                            element_metadata_number = input("1 | 2 :")
                            try:
                                element_metadata_number = int(element_metadata_number)
                                if element_metadata_number == 1 or element_metadata_number == 2:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2)")

                        if element_metadata_number ==  1:
                            m_element_metadata = base_element_df['ielement_metadata'].item()
                        elif element_metadata_number ==  2:
                            m_element_metadata = ""

                else:
                    if new_element_df['ielement_metadata'].item():
                        print("Intentional element ", base_element_df['ielement_name'].item(), " does not have metadata")
                        print("Intentional element ", new_element_df['ielement_name'].item(), "  has metadata:", new_element_df['ielement_metadata'].item())
                        print("Select the metadata of the merged intentional element [", m_element_name, "]")
                        print("1- Do not add metadata to the merged intentional elements")
                        print("2- ", new_element_df['ielement_metadata'].item())

                        while True:
                            element_metadata_number = input("1 | 2 :")
                            try:
                                element_metadata_number = int(element_metadata_number)
                                if element_metadata_number == 1 or element_metadata_number == 2:
                                    break;
                                else:
                                    print("Please enter a valid input (1 or 2)")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 or 2)")

                        if element_metadata_number ==  1:
                            m_element_metadata = ""
                        elif element_metadata_number ==  2:
                            m_element_metadata = new_element_df['ielement_metadata'].item()
                    else:
                        m_element_metadata = ""


                m_element_decomposition_type = '' #for now it will empty, then after inserting the relations, we will get the decomposition type if any

            merged_element_row = {'model_name': m_model_name,'actor_ID': m_actor, 'ielement_type': m_element_type, 'ielement_ID': m_element_ID, 'ielement_name': m_element_name, 'ielement_description': m_element_description, 'ielement_importance': m_element_importance, 'ielement_metadata': m_element_metadata, 'ielement_decomposition_type': m_element_decomposition_type}
            merged_model_df = merged_model_df.append(merged_element_row, ignore_index=True)
            
            the_merged_element_row = {'actor': m_actor_name, 'element_1': base_element_df['ielement_name'].item(), 'element_2': new_element_df['ielement_name'].item(), 'similarity': matched_elements_df['m_similarity'][me]}
            the_merged_elements = the_merged_elements.append(the_merged_element_row, ignore_index=True)

            updateNewID(m_element_ID, base_element_ID, new_element_ID)

# Function to update the merged element ID in the original models and relations
def updateNewID(m_ielement_ID, base_element_ID, new_element_ID):
    base_model_df.loc[base_model_df['ielement_ID'] == base_element_ID, 'ielement_ID'] = m_ielement_ID
    new_model_df.loc[new_model_df['ielement_ID'] == new_element_ID, 'ielement_ID'] = m_ielement_ID
                    
    base_relations_df.loc[base_relations_df['parent_element_ID'] == base_element_ID, 'parent_element_ID'] = m_ielement_ID
    new_relations_df.loc[new_relations_df['parent_element_ID'] == new_element_ID, 'parent_element_ID'] = m_ielement_ID

    base_relations_df.loc[base_relations_df['child_element_ID'] == base_element_ID, 'child_element_ID'] = m_ielement_ID
    new_relations_df.loc[new_relations_df['child_element_ID'] == new_element_ID, 'child_element_ID'] = m_ielement_ID
    
def traceConflict(actor_name, base_name, base_value, new_name, new_value, m_selected_value, m_ID, conflict_type):  
    global trace_conflict_df        
    tracedRow = {'m_ID': m_ID, 'conflict_type': conflict_type, 'actor_name': actor_name, 'base_name': base_name, 'base_value': base_value, 'new_name': new_name, 'new_value': new_value, 'm_selected_value': m_selected_value}
    trace_conflict_df = trace_conflict_df.append(tracedRow, ignore_index=True)
    
def traceError(m_ID, error_type, solution, description, actor_name):
    global trace_error_df
    tracedErrorRow = {'m_ID': m_ID, 'error_type': error_type, 'solution': solution, 'description': description, 'actor_name': actor_name}
    trace_error_df = trace_error_df.append(tracedErrorRow, ignore_index=True)
    
def processUnmatchedElements():
    global merged_model_df
    # Get the matched elements IDs    
    matchedElementsID = matched_elements_df['m_element_ID'].to_list()

    # Bring all IDs from the original DFs
    baseElementsIDs = base_model_df['ielement_ID'].to_list()
    newElementsIDs = new_model_df['ielement_ID'].to_list()

    unmatched_base_elements, unmatched_new_elements = findUnmatchedElements(matchedElementsID, baseElementsIDs, newElementsIDs)

    unmatched_base_elements_df = base_model_df.loc[base_model_df['ielement_ID'].isin(unmatched_base_elements)].reset_index(drop=True)
    unmatched_new_elements_df = new_model_df.loc[new_model_df['ielement_ID'].isin(unmatched_new_elements)].reset_index(drop=True)
    
    # If I use this line, the model name would be taken from the original models (not 'merged_model')
    merged_model_df = merged_model_df.append(unmatched_base_elements_df, ignore_index=True)
    merged_model_df = merged_model_df.append(unmatched_new_elements_df, ignore_index=True)

    
def mergeRelations(mergingMethod):
    global the_merged_links
    for br in range(len(base_relations_df)):
        base_relation_df = pd.DataFrame(base_relations_df.loc[[br]])
        for nr in range(len(new_relations_df)):
            new_relation_df = pd.DataFrame(new_relations_df.loc[[nr]])
            if base_relations_df['child_element_ID'][br] == new_relations_df['child_element_ID'][nr]:
                if base_relations_df['child_actor_ID'][br] == new_relations_df['child_actor_ID'][nr]:
                    if base_relations_df['parent_actor_ID'][br] == new_relations_df['parent_actor_ID'][nr]:
                        if base_relations_df['parent_element_ID'][br] == new_relations_df['parent_element_ID'][nr]:
                            m_relation_ID = base_relations_df['relation_ID'][br] + '+' + new_relations_df['relation_ID'][nr]
                            base_relation_parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == base_relations_df['parent_element_ID'][br], 'ielement_name'].iloc[0]
                            base_relation_child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == base_relations_df['child_element_ID'][br], 'ielement_name'].iloc[0]
                            
                            new_relation_parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == new_relations_df['parent_element_ID'][nr], 'ielement_name'].iloc[0]
                            new_relation_child_element = merged_model_df.loc[merged_model_df['ielement_ID'] ==  new_relations_df['child_element_ID'][nr], 'ielement_name'].iloc[0]
                            
                            if base_relations_df['parent_actor_ID'][br] == 'X#Y':
                                parent_actor_name = 'X#YDUMMYACTOR'
                            else: 
                                parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] == base_relations_df['parent_actor_ID'][br], 'actor_name'].iloc[0]
                            
                            if base_relations_df['child_actor_ID'][br] == 'X#Y':
                                child_actor_name = 'X#YDUMMYACTOR'
                            else:
                                child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] == base_relations_df['child_actor_ID'][br], 'actor_name'].iloc[0]

                            
                            the_merged_link_row = {'parent_element_1': base_relation_parent_element, 'link_1': base_relations_df['relation_type'][br], 'child_element_1':base_relation_child_element, 'parent_element_2': new_relation_parent_element, 'link_2': new_relations_df['relation_type'][nr], 'child_element_2': new_relation_child_element}
                            the_merged_links = the_merged_links.append(the_merged_link_row, ignore_index=True)
                                


                            if base_relations_df['relation_type'][br] == new_relations_df['relation_type'][nr]:
#                                 print("Same relation")
                                if base_relations_df['relation_type'][br] == 'contribution':
                                    if not quantitativeContributionValue(base_relations_df['contribution_value'][br], new_relations_df['contribution_value'][nr]):
                                        if mergingMethod == "1":
                                            # Get the type of the base element
                                            m_contribution_value = base_relations_df['contribution_value'][br]
                                        elif mergingMethod == "2":
                                            print("Conflict in the contribution value of the matched links: ")
                                            print("1- (", base_relation_child_element, ") contributes to (", base_relation_parent_element, ") with a contribution value =", base_relations_df['contribution_value'][br])
                                            print("2- (", new_relation_child_element, ") contributes to (", new_relation_parent_element, ") with a contribution value =", new_relations_df['contribution_value'][nr])
                                            print("Select the contribution value of the merged link")
                                            print("1-", base_relations_df['contribution_value'][br])
                                            print("2-", new_relations_df['contribution_value'][nr])
                                            while True:
                                                relation_number = input("1 | 2 :")
                                                try:
                                                    relation_number = int(relation_number)
                                                    if relation_number == 1 or relation_number == 2:
                                                        break;
                                                    else:
                                                        print("Please enter a valid input (1 or 2)")
                                                        continue;
                                                except ValueError:
                                                    print("Please enter a valid input (1 or 2)")


                                            if relation_number ==  1:
                                                m_contribution_value = base_relations_df['contribution_value'][br]
                                            elif relation_number ==  2:
                                                m_contribution_value = new_relations_df['contribution_value'][nr]
                                        traceConflict(parent_actor_name+" - "+child_actor_name, "("+base_relation_child_element+") contributes to ("+base_relation_parent_element+")", base_relations_df['contribution_value'][br], "("+new_relation_child_element+") contributes to ("+ new_relation_parent_element+")", new_relations_df['contribution_value'][nr], m_contribution_value, m_relation_ID, 'Contribution Value')

                                    else:
                                        m_contribution_value = base_relations_df['contribution_value'][br]
#                                    else:
#                                        m_contribution_value = base_relations_df['contribution_value'][br]
                                    insertMergedRelation(base_relation_df, 'contribution', '', m_contribution_value, m_relation_ID)
                                elif base_relations_df['relation_type'][br] == 'decomposition':
                                    if base_relations_df['decomposition_type'][br] != new_relations_df['decomposition_type'][nr]:
#                                         print("Trace conflict")
                                        if mergingMethod == "1":
                                            # Get the type of the base element
                                            m_decomposition_type = base_relations_df['decomposition_type'][br]
                                        elif mergingMethod == "2":
                                            print("Conflict in the decomposition type of the matched links: ")
                                            print("1- (", base_relation_parent_element, ") decomposed by (", base_relation_child_element, ") with a decomposition of type", base_relations_df['decomposition_type'][br])
                                            print("2- (", new_relation_parent_element, ") decomposed by (", new_relation_child_element, ") with a decomposition of type", new_relations_df['decomposition_type'][nr])
                                        
                                            print("Select the decomposition type of the merged link")
                                            print("1-", base_relations_df['decomposition_type'][br])
                                            print("2-", new_relations_df['decomposition_type'][nr])
                                            while True:
                                                relation_number = input("1 | 2 :")
                                                try:
                                                    relation_number = int(relation_number)
                                                    if relation_number == 1 or relation_number == 2:
                                                        break;
                                                    else:
                                                        print("Please enter a valid input (1 or 2)")
                                                        continue;
                                                except ValueError:
                                                    print("Please enter a valid input (1 or 2)")
                                            
                                            
                                            if relation_number ==  1:
                                                m_decomposition_type = base_relations_df['decomposition_type'][br]
                                            elif relation_number ==  2:
                                                m_decomposition_type = new_relations_df['decomposition_type'][nr]
                                        traceConflict(parent_actor_name+" - "+child_actor_name, "("+base_relation_parent_element+") decomposed by ("+base_relation_child_element+")", base_relations_df['decomposition_type'][br], "("+new_relation_parent_element+") decomposed by ("+new_relation_child_element+")", new_relations_df['decomposition_type'][nr], m_decomposition_type, m_relation_ID, 'Decomposition Type')

                                    else:
                                        m_decomposition_type = base_relations_df['decomposition_type'][br]
                                    insertMergedRelation(base_relation_df, 'decomposition', m_decomposition_type, '', m_relation_ID)
                                elif base_relations_df['relation_type'][br] == 'dependency':
                                    insertMergedRelation(base_relation_df, 'dependency', '', '', m_relation_ID)            
                            else:
#                                 print("Different relations")
                                if mergingMethod == "1":
                                    # Get the type of the base element
                                    m_relation_type = base_relations_df['relation_type'][br]
                                    m_decomposition_type = base_relations_df['decomposition_type'][br]
                                    m_contribution_value = base_relations_df['contribution_value'][br]
                                elif mergingMethod == "2":
                                    print("Conflict in the link type of the matched links: ")
                                    
                                    if base_relations_df['relation_type'][br] == 'contribution':
                                        print("1- (", base_relation_child_element, ") contributes to (", base_relation_parent_element, ") with a contribution value = ", base_relations_df['contribution_value'][br])
                                    elif base_relations_df['relation_type'][br] == 'decomposition':
                                        print("1- (", base_relation_parent_element, ") decomposed by (", base_relation_child_element, ") with a decomposition type: ", base_relations_df['decomposition_type'][br])
                                        
                                        
                                    if new_relations_df['relation_type'][nr] == 'contribution':
                                        print("2- (", new_relation_child_element, ") contributes to (", new_relation_parent_element, ") with a contribution value = ", new_relations_df['contribution_value'][nr])
                                    elif new_relations_df['relation_type'][nr] == 'decomposition':
                                        print("2- (", new_relation_parent_element, ") decomposed by (", new_relation_child_element, ") with a decomposition type: ", new_relations_df['decomposition_type'][nr])
                                    
                                        
                                    print("Select the type of the merged link")
                                    print("1-", base_relations_df['relation_type'][br])
                                    print("2-", new_relations_df['relation_type'][nr])
                                    while True:
                                        relation_number = input("1 | 2 :")
                                        try:
                                            relation_number = int(relation_number)
                                            if relation_number == 1 or relation_number == 2:
                                                break;
                                            else:
                                                print("Please enter a valid input (1 or 2)")
                                                continue;
                                        except ValueError:
                                            print("Please enter a valid input (1 or 2)")
                                            
                                    if relation_number ==  1:
                                        m_relation_type = base_relations_df['relation_type'][br]
                                        m_decomposition_type = base_relations_df['decomposition_type'][br]
                                        m_contribution_value = base_relations_df['contribution_value'][br]
                                    elif relation_number ==  2:
                                        m_relation_type = new_relations_df['relation_type'][nr]
                                        m_decomposition_type = new_relations_df['decomposition_type'][nr]
                                        m_contribution_value = new_relations_df['contribution_value'][nr]
                                traceConflict(parent_actor_name+" - "+child_actor_name, "("+base_relation_child_element+") linked to ("+base_relation_parent_element+")", base_relations_df['relation_type'][br], "("+new_relation_child_element+") linked to ("+new_relation_parent_element+")", new_relations_df['relation_type'][nr], m_relation_type, m_relation_ID, 'Link Type')

                                insertMergedRelation(base_relation_df, m_relation_type, m_decomposition_type, m_contribution_value, m_relation_ID)

                                
                                
def quantitativeContributionValue(base_contribution, new_contribution):
    base_converted = False 
    new_converted = False 
    
    qualitative_contribution = re.compile('hurt|break|make|help|someNegative|somePositive')

    if qualitative_contribution.match(str(base_contribution)):
        base_converted = True 

    if qualitative_contribution.match(str(new_contribution)):
        new_converted = True 

    if base_converted and new_converted:
        if base_contribution == new_contribution:
            return True
        else:
            return False
    elif base_converted:
        new_contribution = int(new_contribution)
        if base_contribution == 'hurt':
            if new_contribution <= -1 and new_contribution >= -49:
                return True
            else:
                return False
        elif base_contribution == 'someNegative':
            if new_contribution <= -50 and new_contribution >= -99:
                return True
            else:
                return False
        elif base_contribution == 'break':
            if new_contribution == -100:
                return True
            else:
                return False
        elif base_contribution == 'help':
            if new_contribution >= 1 and new_contribution <= 49:
                return True
            else:
                return False
        elif base_contribution == 'somePositive':
            if new_contribution >= 50 and new_contribution <= 99:
                return True
            else:
                return False
        elif base_contribution == 'make':
            if new_contribution == 100:
                return True
            else:
                return False
    elif new_converted:
        base_contribution = int(base_contribution)
        if new_contribution == 'hurt':
            if base_contribution <= -1 and base_contribution >= -49:
                return True
            else:
                return False
        elif new_contribution == 'someNegative':
            if base_contribution <= -50 and base_contribution >= -99:
                return True
            else:
                return False
        elif new_contribution == 'break':
            if base_contribution == -100:
                return True
            else:
                return False
        elif new_contribution == 'help':
            if base_contribution >= 1 and base_contribution <= 49:
                return True
            else:
                return False
        elif new_contribution == 'somePositive':
            if base_contribution >= 50 and base_contribution <= 99:
                return True
            else:
                return False
        elif new_contribution == 'make':
            if base_contribution == 100:
                return True
            else:
                return False


def quantitativeImportanceValue(base_importance, new_importance):
    base_converted = False 
    new_converted = False 
    
    qualitative_importance = re.compile('high|medium|low|none')

    if qualitative_importance.match(str(base_importance)):
        base_converted = True 

    if qualitative_importance.match(str(new_importance)):
        new_converted = True 

    if base_converted and new_converted:
        if base_importance == new_importance:
            return True
        else:
            return False
    elif base_converted:
        new_importance = int(new_importance)
        if base_importance == 'high':
            if new_importance >= 66 and new_importance <=100:
                return True
            else:
                return False
        elif base_importance == 'medium':
            if new_importance >= 33 and new_importance <=65:
                return True
            else:
                return False
        elif base_importance == 'low':
            if new_importance >= 1 and new_importance <=32:
                return True
            else:
                return False
        elif base_importance == 'none':
            if new_importance == 0:
                return True
            else:
                return False
    elif new_converted:
        base_importance = int(base_importance)
        if new_importance == 'high':
            if base_importance >= 66 and base_importance <=100:
                return True
            else:
                return False
        elif new_importance == 'medium':
            if base_importance >= 33 and base_importance <=65:
                return True
            else:
                return False
        elif new_importance == 'low':
            if base_importance >= 1 and base_importance <=32:
                return True
            else:
                return False
        elif new_importance == 'none':
            if base_importance == 0:
                return True
            else:
                return False


def insertMergedRelation(base_relation_df, m_relation_type, m_decomposition_type, m_contribution_value, m_relation_ID):
    global merged_relations_df
    m_parent_actor_ID = base_relation_df['parent_actor_ID'].item()
    m_parent_element_ID = base_relation_df['parent_element_ID'].item()
    m_child_actor_ID = base_relation_df['child_actor_ID'].item()
    m_child_element_ID = base_relation_df['child_element_ID'].item()
    merged_relation_row = {'relation_ID': m_relation_ID, 'parent_actor_ID': m_parent_actor_ID, 'parent_element_ID': m_parent_element_ID, 'relation_type': m_relation_type, 'child_actor_ID': m_child_actor_ID, 'child_element_ID': m_child_element_ID, 'decomposition_type': m_decomposition_type, 'contribution_value': m_contribution_value}
    merged_relations_df = merged_relations_df.append(merged_relation_row, ignore_index=True)
    
    
def processUnmatchedRelations():
    global merged_relations_df
    # Get the matched elements IDs    
    matchedRelationsID = merged_relations_df['relation_ID'].to_list()

    # Bring all IDs from the original DFs
    baseRelationsIDs = base_relations_df['relation_ID'].to_list()
    newRelationsIDs = new_relations_df['relation_ID'].to_list()

    unmatched_base_relations, unmatched_new_relations = findUnmatchedElements(matchedRelationsID, baseRelationsIDs, newRelationsIDs)

    unmatched_base_relations_df = base_relations_df.loc[base_relations_df['relation_ID'].isin(unmatched_base_relations)].reset_index(drop=True)
    unmatched_new_relations_df = new_relations_df.loc[new_relations_df['relation_ID'].isin(unmatched_new_relations)].reset_index(drop=True)

    # Insert unmatched relations to the merged relations
    merged_relations_df = merged_relations_df.append(unmatched_base_relations_df, ignore_index=True)
    merged_relations_df = merged_relations_df.append(unmatched_new_relations_df, ignore_index=True)
    
# Function to store the original siblings so we can use it later we checking the siblings
def storeOriginalSiblings():

    base_parents = base_relations_df['parent_element_ID'].unique()
    new_parents = new_relations_df['parent_element_ID'].unique()

    global base_original_siblings_df
    base_original_siblings_df = pd.DataFrame(columns=['parent_ID', 'element_ID'])
    for i in range(len(base_parents)):
        for j in range(len(base_relations_df)):
            if base_parents[i] == base_relations_df['parent_element_ID'][j]:
                sibling_row = {'parent_ID': base_parents[i], 'element_ID': base_relations_df['child_element_ID'][j]}
                base_original_siblings_df = base_original_siblings_df.append(sibling_row, ignore_index = True)



    global new_original_siblings_df
    new_original_siblings_df = pd.DataFrame(columns=['parent_ID', 'element_ID'])
    for i in range(len(new_parents)):
        for j in range(len(new_relations_df)):
            if new_parents[i] == new_relations_df['parent_element_ID'][j]:
                sibling_row = {'parent_ID': new_parents[i], 'element_ID': new_relations_df['child_element_ID'][j]}
                new_original_siblings_df = new_original_siblings_df.append(sibling_row, ignore_index = True)

#def checkDirectCycles(mergingMethod):
##    print("Inside direct cycles")
#    global merged_relations_df
#    global new_relations_df
#    
#    unique_parents_IDs = merged_relations_df['parent_element_ID'].unique().tolist()
#    unique_children_IDs = merged_relations_df['child_element_ID'].unique().tolist()
#
#    points_of_possible_cycles = list(set(unique_parents_IDs).intersection(unique_children_IDs))
#
#    for x in range(len(points_of_possible_cycles)):
#        links_to_break = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
#        new_links_rows = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
#
#        all_point_relations = merged_relations_df.loc[(merged_relations_df['parent_element_ID'] == points_of_possible_cycles[x]) | (merged_relations_df['child_element_ID'] == points_of_possible_cycles[x])]
#        point_parents = all_point_relations['parent_element_ID'].unique().tolist()
#        point_children = all_point_relations['child_element_ID'].unique().tolist()
#        if not point_parents is None and not point_children is None:
#            direct_cycles = list(set(point_parents).intersection(point_children))
#            if len(direct_cycles) > 0:
#                direct_cycles.remove(points_of_possible_cycles[x])
##            print("Possible direct cycles", direct_cycles)
#            if len(direct_cycles) > 0:
#                for dc in range(len(direct_cycles)):
#                    point_of_cycle_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == points_of_possible_cycles[x], 'ielement_name'].iloc[0]
#                    element_in_cycle_name = merged_model_df.loc[merged_model_df['ielement_ID'] == direct_cycles[dc], 'ielement_name'].iloc[0]
#
#                    print("A direct cycle between ", point_of_cycle_element_name, " and ", element_in_cycle_name)
#                    links_to_break = merged_relations_df.loc[((merged_relations_df['parent_element_ID'] == direct_cycles[dc]) & (merged_relations_df['child_element_ID'] == points_of_possible_cycles[x])) | ((merged_relations_df['child_element_ID'] == direct_cycles[dc]) & (merged_relations_df['parent_element_ID'] == points_of_possible_cycles[x]))]
#                    if not links_to_break.empty:
#                        if mergingMethod == '1':
#                            for l in range(len(links_to_break)):
#                                new_link_row = new_relations_df.loc[((new_relations_df['parent_element_ID'] == links_to_break.iloc[l]['parent_element_ID']) & (new_relations_df['relation_type'] == links_to_break.iloc[l]['relation_type']) & (new_relations_df['child_element_ID'] == links_to_break.iloc[l]['child_element_ID']))]
#                                new_link_row = new_link_row.reset_index(drop=True)
#                                new_links_rows = new_links_rows.append(new_link_row)
#                                new_links_rows = new_links_rows.reset_index(drop=True)
#                                # drop the link from the new relation
#                                new_relations_df.drop(new_relations_df[(new_relations_df['parent_element_ID'] == links_to_break.iloc[l]['parent_element_ID']) & (new_relations_df['relation_type'] == links_to_break.iloc[l]['relation_type']) & (new_relations_df['child_element_ID'] == links_to_break.iloc[l]['child_element_ID'])].index, inplace = True)
#                                new_relations_df = new_relations_df.reset_index(drop=True)
#
#                            if not new_links_rows.empty:
#                                for nl in range(len(new_links_rows)):
#                                    if new_links_rows['relation_ID'][nl] in merged_relations_df['relation_ID'].values:
##                                 new_link_to_drop = new_links_rows.sample()
##                                 link_ID = new_link_to_drop['relation_ID'].item()
#                                       
#                                        link_row_df = merged_relations_df[merged_relations_df['relation_ID'] == new_links_rows['relation_ID'][nl]]
#                                        parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['parent_element_ID'].item(), 'ielement_name'].iloc[0]
#                                        child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['child_element_ID'].item(), 'ielement_name'].iloc[0]
#                            
#                                        if link_row_df['parent_actor_ID'].item() == 'X#Y':
#                                            parent_actor_name = 'X#YDUMMYACTOR'
#                                        else:
#                                            parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['parent_actor_ID'].item(), 'actor_name'].iloc[0]
#                                            
#                                        if link_row_df['child_actor_ID'].item() == 'X#Y':   
#                                            child_actor_name = 'X#YDUMMYACTOR'
#                                        else:
#                                            child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['child_actor_ID'].item(), 'actor_name'].iloc[0]
#
#                    
#                    
##                                        parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['parent_actor_ID'].item(), 'actor_name'].iloc[0]
##                                        child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['child_actor_ID'].item(), 'actor_name'].iloc[0]
#
#                                        link_description = parent_element+" linked to "+child_element+", via the link "+link_row_df['relation_type'].item()
#                                        merged_relations_df.drop(merged_relations_df[merged_relations_df['relation_ID'] == new_links_rows['relation_ID'][nl]].index, inplace = True)
#                                        merged_relations_df = merged_relations_df.reset_index(drop=True)
#                                        traceError(new_links_rows['relation_ID'][nl], 'Direct Cycle', 'Drop Link', link_description, parent_actor_name+" - "+child_actor_name)
#
##                                        print("Dropped link:", new_links_rows['relation_ID'][nl])
##                             else:
##                                 mergingMethod = '2'
#                        if mergingMethod == '2':
#                            print("Select one of links to be removed for resolving the direct cycle")
#                            for l in range(len(links_to_break)):
#                                parent_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == links_to_break.iloc[l]['parent_element_ID'], 'ielement_name'].iloc[0]
#                                child_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == links_to_break.iloc[l]['child_element_ID'], 'ielement_name'].iloc[0]
#
#                                if links_to_break.iloc[l]['relation_type'] == 'decomposition':
#                                    print(l+1, "- Parent element: (", parent_element_name, ") Decomposed by Child Element: (", child_element_name, ") with", links_to_break.iloc[l]['decomposition_type'], "-Decomposition")
#                                elif links_to_break.iloc[l]['relation_type'] == 'contribution':
#                                    print(l+1, "- Child Element: (", child_element_name, ") Contributes to Parent Element: (", parent_element_name, ") with contribution value = ", links_to_break.iloc[l]['contribution_value'])
#                                elif links_to_break.iloc[l]['relation_type'] == 'dependency':
#                                    print(l+1, "- Parent Element: (", parent_element_name, ") Depends on Child Element: (", child_element_name, ")")
#                                    
#                            while True:
#                                link_number = input("Enter the link number to break: ")
#                                try:
#                                    link_number = int(link_number)
#                                    if link_number > 0 and link_number <= len(links_to_break):
#                                        break;
#                                    else:
#                                        print("Please enter a valid input (1 to "+str(len(links_to_break))+")")
#                                        continue;
#                                except ValueError:
#                                    print("Please enter a valid input (1 to "+str(len(links_to_break))+")")
##                            link_number = input("Enter the link number to break: ")
#                            link_number = int(link_number) - 1
#                            link_row = links_to_break.iloc[[link_number]]
#                            link_ID = link_row['relation_ID'].item()
#                            link_row_df = merged_relations_df[merged_relations_df['relation_ID'] == link_ID]
#                            parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['parent_element_ID'].item(), 'ielement_name'].iloc[0]
#                            child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['child_element_ID'].item(), 'ielement_name'].iloc[0]
#                            
#                            parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['parent_actor_ID'].item(), 'actor_name'].iloc[0]
#                            child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['child_actor_ID'].item(), 'actor_name'].iloc[0]
#
#                            
#                            
#                            link_description = parent_element+" linked to "+child_element+", via the link "+link_row_df['relation_type'].item()
#                            
#                            merged_relations_df.drop(merged_relations_df[merged_relations_df['relation_ID'] == link_ID].index, inplace = True)
#                            merged_relations_df = merged_relations_df.reset_index(drop=True)
#                            traceError(link_ID, 'Direct Cycle', 'Drop Link', link_description, parent_actor_name+" - "+child_actor_name)
#
##                            print("Dropped link:", link_ID)

def checkDirectCycles(mergingMethod):
    global merged_relations_df
    global new_relations_df
    
    unique_parents_IDs = merged_relations_df['parent_element_ID'].unique().tolist()
    unique_children_IDs = merged_relations_df['child_element_ID'].unique().tolist()

    points_of_possible_cycles = list(set(unique_parents_IDs).intersection(unique_children_IDs))

    for x in range(len(points_of_possible_cycles)):
        links_to_break = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
        new_links_rows = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])

        all_point_relations = merged_relations_df.loc[(merged_relations_df['parent_element_ID'] == points_of_possible_cycles[x]) | (merged_relations_df['child_element_ID'] == points_of_possible_cycles[x])]
        point_parents = all_point_relations['parent_element_ID'].unique().tolist()
        point_children = all_point_relations['child_element_ID'].unique().tolist()
        if not point_parents is None and not point_children is None:
            direct_cycles = list(set(point_parents).intersection(point_children))
            if len(direct_cycles) > 0:
                direct_cycles.remove(points_of_possible_cycles[x])
              
            
#                 print(direct_cycles, len(direct_cycles))
            
#             print("with the elements", direct_cycles)
            if len(direct_cycles) > 0:
                for dc in range(len(direct_cycles)):
                    point_of_cycle_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == points_of_possible_cycles[x], 'ielement_name'].iloc[0]
                    element_in_cycle_name = merged_model_df.loc[merged_model_df['ielement_ID'] == direct_cycles[dc], 'ielement_name'].iloc[0]

                    links_to_break = merged_relations_df.loc[((merged_relations_df['parent_element_ID'] == direct_cycles[dc]) & (merged_relations_df['child_element_ID'] == points_of_possible_cycles[x])) | ((merged_relations_df['child_element_ID'] == direct_cycles[dc]) & (merged_relations_df['parent_element_ID'] == points_of_possible_cycles[x]))]
                    if not links_to_break.empty:
                        if mergingMethod == '1':
                            for l in range(len(links_to_break)):
                                new_link_row = new_relations_df.loc[((new_relations_df['parent_element_ID'] == links_to_break.iloc[l]['parent_element_ID']) & (new_relations_df['relation_type'] == links_to_break.iloc[l]['relation_type']) & (new_relations_df['child_element_ID'] == links_to_break.iloc[l]['child_element_ID']))]
                                new_link_row = new_link_row.reset_index(drop=True)
                                new_links_rows = new_links_rows.append(new_link_row)
                                new_links_rows = new_links_rows.reset_index(drop=True)
                                # drop the link from the new relation
                                new_relations_df.drop(new_relations_df[(new_relations_df['parent_element_ID'] == links_to_break.iloc[l]['parent_element_ID']) & (new_relations_df['relation_type'] == links_to_break.iloc[l]['relation_type']) & (new_relations_df['child_element_ID'] == links_to_break.iloc[l]['child_element_ID'])].index, inplace = True)
                                new_relations_df = new_relations_df.reset_index(drop=True)
#                             print("***", new_links_rows)
                            if not new_links_rows.empty:
                                for nl in range(len(new_links_rows)):
                                    if new_links_rows['relation_ID'][nl] in merged_relations_df['relation_ID'].values:
#                                 new_link_to_drop = new_links_rows.sample()
#                                 link_ID = new_link_to_drop['relation_ID'].item()
                                        link_row_df = merged_relations_df[merged_relations_df['relation_ID'] == new_links_rows['relation_ID'][nl]]
                                        parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['parent_element_ID'].item(), 'ielement_name'].iloc[0]
                                        child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['child_element_ID'].item(), 'ielement_name'].iloc[0]
                                        
                                        if link_row_df['parent_actor_ID'].item() == 'X#Y':
                                            parent_actor_name = 'X#YDUMMYACTOR'
                                        else:
                                            parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['parent_actor_ID'].item(), 'actor_name'].iloc[0]
                                            
                                        if link_row_df['child_actor_ID'].item() == 'X#Y':   
                                            child_actor_name = 'X#YDUMMYACTOR'
                                        else:
                                            child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['child_actor_ID'].item(), 'actor_name'].iloc[0]

                                        link_description = parent_element+" linked to "+child_element+", via the link "+link_row_df['relation_type'].item()
                                        merged_relations_df.drop(merged_relations_df[merged_relations_df['relation_ID'] == new_links_rows['relation_ID'][nl]].index, inplace = True)
                                        merged_relations_df = merged_relations_df.reset_index(drop=True)
        #                                 print("UPDATES RELATIONS DF")
        #                                 print(merged_relations_df['relation_ID'])
#                                         traceConflict('', '', '', '', link_description, new_links_rows['relation_ID'][nl], 'dropped_link')
                                        traceError(new_links_rows['relation_ID'][nl], 'Direct Cycle', 'Drop Link', link_description, parent_actor_name+"-"+child_actor_name)
#                             else:
#                                 mergingMethod = '2'
                        if mergingMethod == '2':
                            print("A direct cycle between ", point_of_cycle_element_name, " and ", element_in_cycle_name)

                            print("Select one of the links to be removed for resolving the cycle")
                            for l in range(len(links_to_break)):
                                parent_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == links_to_break.iloc[l]['parent_element_ID'], 'ielement_name'].iloc[0]
                                child_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == links_to_break.iloc[l]['child_element_ID'], 'ielement_name'].iloc[0]

                                if links_to_break.iloc[l]['relation_type'] == 'decomposition':
                                    print(l+1, "- Parent element: (", parent_element_name, ") Decomposed by Child Element: (", child_element_name, ") with", links_to_break.iloc[l]['decomposition_type'], "-Decomposition")
                                elif links_to_break.iloc[l]['relation_type'] == 'contribution':
                                    print(l+1, "- Child Element: (", child_element_name, ") Contributes to Parent Element: (", parent_element_name, ") with contribution value = ", links_to_break.iloc[l]['contribution_value'])
                                elif links_to_break.iloc[l]['relation_type'] == 'dependency':
                                    print(l+1, "- Parent Element: (", parent_element_name, ") Depends on Child Element: (", child_element_name, ")")

                            while True:
                                link_number = input("Enter the link number to break: ")
                                try:
                                    link_number = int(link_number)
                                    if link_number > 0 and link_number <= len(links_to_break):
                                        break;
                                    else:
                                        print("Please enter a valid input (1 to "+str(len(links_to_break))+")")
                                        continue;
                                except ValueError:
                                    print("Please enter a valid input (1 to "+str(len(links_to_break))+")")
#                            link_number = input("Enter the link number to break: ")
                            
                            link_number = int(link_number) - 1
                            link_row = links_to_break.iloc[[link_number]]
                            link_ID = link_row['relation_ID'].item()
                            
                            link_row_df = merged_relations_df[merged_relations_df['relation_ID'] == link_ID]
                            parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['parent_element_ID'].item(), 'ielement_name'].iloc[0]
                            child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['child_element_ID'].item(), 'ielement_name'].iloc[0]
                              
                            if link_row_df['parent_actor_ID'].item() == 'X#Y':
                                parent_actor_name = 'X#YDUMMYACTOR'
                            else:
                                parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['parent_actor_ID'].item(), 'actor_name'].iloc[0]

                            if link_row_df['child_actor_ID'].item() == 'X#Y':   
                                child_actor_name = 'X#YDUMMYACTOR'
                            else:
                                child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['child_actor_ID'].item(), 'actor_name'].iloc[0]

                                            
#                             parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['parent_actor_ID'].item(), 'actor_name'].iloc[0]
#                             child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['child_actor_ID'].item(), 'actor_name'].iloc[0]

                            
                            link_description = parent_element+" linked to "+child_element+", via the link "+link_row_df['relation_type'].item()
                            
                            merged_relations_df.drop(merged_relations_df[merged_relations_df['relation_ID'] == link_ID].index, inplace = True)
                            merged_relations_df = merged_relations_df.reset_index(drop=True)
#                             traceConflict('', '', '', '', link_description, link_ID, 'dropped_link')
                            traceError(link_ID, 'Direct Cycle', 'Drop Link', link_description, parent_actor_name+"-"+child_actor_name)
                            
                            
#def checkIndirectCycles(mergingMethod):
#    global merged_relations_df
#    global new_relations_df
#    
#    unique_parents_IDs = merged_relations_df['parent_element_ID'].unique().tolist()
#    unique_children_IDs = merged_relations_df['child_element_ID'].unique().tolist()
#
#    points_of_possible_cycles = list(set(unique_parents_IDs).intersection(unique_children_IDs))
#
#    for x in range(len(points_of_possible_cycles)):
#        relation_copy_1 = merged_relations_df.copy()
#        relation_copy_2 = merged_relations_df.copy()
#        links_to_break = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
#        new_links_rows = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
#
#        # Get all parents and children of possible point of cycle
#        parents_IDs = getAllParents(points_of_possible_cycles[x], [], relation_copy_1)
#        children_IDs = getAllChildren(points_of_possible_cycles[x], [], relation_copy_2)
#
#        if not parents_IDs is None and not children_IDs is None:
#            # Get the elements causing the cycles
#            cycle_location = list(set(parents_IDs).intersection(children_IDs))
#
#            # Get the relations DF that causing the cycles
#            for c in range(len(cycle_location)):
#                for d in range(len(cycle_location)-1):
#                    links_df = merged_relations_df.loc[((merged_relations_df['parent_element_ID'] == cycle_location[c]) & (merged_relations_df['child_element_ID'] == cycle_location[d+1])) | ((merged_relations_df['child_element_ID'] == cycle_location[c]) & (merged_relations_df['parent_element_ID'] == cycle_location[d+1]))]
#                    links_df = links_df.reset_index(drop=True)
#                    links_to_break = links_to_break.append(links_df)
#                    links_to_break = links_to_break.reset_index(drop=True)
#            links_to_break = links_to_break.drop_duplicates().reset_index(drop=True)   
#            if not links_to_break.empty:
#                new_link_broken = False
#                if mergingMethod == '1':
#                    for l in range(len(links_to_break)):
#                        # The link to break exists in the merged model and it is from the non-base model
#                        new_link_row = new_relations_df.loc[((new_relations_df['parent_actor_ID'] == links_to_break.iloc[l]['parent_actor_ID']) & (new_relations_df['parent_element_ID'] == links_to_break.iloc[l]['parent_element_ID']) & (new_relations_df['relation_type'] == links_to_break.iloc[l]['relation_type']) & (new_relations_df['parent_actor_ID'] == links_to_break.iloc[l]['parent_actor_ID']) &  (new_relations_df['child_element_ID'] == links_to_break.iloc[l]['child_element_ID']))]
#                        new_link_row = new_link_row.reset_index(drop=True)
#
#                        if not new_link_row.empty:
#                            # drop the link from the new relation
#                            new_relations_df.drop(new_relations_df[(new_relations_df['parent_element_ID'] == links_to_break.iloc[l]['parent_element_ID']) & (new_relations_df['relation_type'] == links_to_break.iloc[l]['relation_type']) & (new_relations_df['child_element_ID'] == links_to_break.iloc[l]['child_element_ID'])].index, inplace = True)
#                            new_relations_df = new_relations_df.reset_index(drop=True)
#                            if new_link_row['relation_ID'].item() in merged_relations_df['relation_ID'].values:
#                                new_link_broken = True
#                                mergingMethod = '1'
#                                parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == new_link_row['parent_element_ID'].item(), 'ielement_name'].iloc[0]
#                                child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == new_link_row['child_element_ID'].item(), 'ielement_name'].iloc[0]
#                                
##                                parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  new_link_row['parent_actor_ID'].item(), 'actor_name'].iloc[0]
##                                child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  new_link_row['child_actor_ID'].item(), 'actor_name'].iloc[0]
#                                if new_link_row['parent_actor_ID'].item() == 'X#Y':
#                                    parent_actor_name = 'X#YDUMMYACTOR'
#                                else:
#                                    parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  new_link_row['parent_actor_ID'].item(), 'actor_name'].iloc[0]
#
#                                if new_link_row['child_actor_ID'].item() == 'X#Y':
#                                    child_actor_name = 'X#YDUMMYACTOR'
#                                else:
#                                    child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  new_link_row['child_actor_ID'].item(), 'actor_name'].iloc[0]
#
#
#                                link_description = parent_element+" linked to "+child_element+", via the link "+new_link_row['relation_type'].item()
#
#                                merged_relations_df.drop(merged_relations_df[merged_relations_df['relation_ID'] == new_link_row['relation_ID'].item()].index, inplace = True)
#                                merged_relations_df = merged_relations_df.reset_index(drop=True)
#
#                                traceError(new_link_row['relation_ID'].item(), 'Indirect Cycle', 'Drop Link', link_description, parent_actor_name+" - "+child_actor_name)
#
#                            if continueCheckingCycles(points_of_possible_cycles[x]):
#                                continue 
#                            else:
#                                break
#                # to check that the cycle has been resolved by dropping a link from the new model
#                if not new_link_broken:
#                    print("There is a cycle could not be resolved automatically")
#                    mergingMethod = '2'
#                            
#
#                if mergingMethod == '2':
##                    if not new_link_broken:
##                        print("There is a cycle could not be resolved automatically")
#                    cycle_exists = True 
#                    while cycle_exists:
#                        print("Select one of links to be removed for resolving the indirect cycle")
#                        for l in range(len(links_to_break)):
#                            parent_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == links_to_break.iloc[l]['parent_element_ID'], 'ielement_name'].iloc[0]
#                            child_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == links_to_break.iloc[l]['child_element_ID'], 'ielement_name'].iloc[0]
#
#                            if links_to_break.iloc[l]['relation_type'] == 'decomposition':
#                                print(l+1, "- Parent element: (", parent_element_name, ") Decomposed by Child Element: (", child_element_name, ") with", links_to_break.iloc[l]['decomposition_type'], "-Decomposition")
#                            elif links_to_break.iloc[l]['relation_type'] == 'contribution':
#                                print(l+1, "- Child Element: (", child_element_name, ") Contributes to Parent Element: (", parent_element_name, ") with contribution value = ", links_to_break.iloc[l]['contribution_value'])
#                            elif links_to_break.iloc[l]['relation_type'] == 'dependency':
#                                print(l+1, "- Parent Element: (", parent_element_name, ") Depends on Child Element: (", child_element_name, ")")
#
#                                
#                                
#                                
#                        while True:
#                            link_number = input("Enter the link number to break: ")
#                            try:
#                                link_number = int(link_number)
#                                if link_number > 0 and link_number <= len(links_to_break):
#                                    break;
#                                else:
#                                    print("Please enter a valid input (1 to "+str(len(links_to_break))+")")
#                                    continue;
#                            except ValueError:
#                                print("Please enter a valid input (1 to "+str(len(links_to_break))+")")
#
##                        link_number = input("Enter the link number to break: ")
#                        link_number = int(link_number) - 1
#                        link_row = links_to_break.iloc[[link_number]]
#                        link_ID = link_row['relation_ID'].item()
#
#                        link_row_df = merged_relations_df[merged_relations_df['relation_ID'] == link_ID]
#                        parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['parent_element_ID'].item(), 'ielement_name'].iloc[0]
#                        
#                        child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['child_element_ID'].item(), 'ielement_name'].iloc[0]
#                        
##                        
#                        if link_row_df['parent_actor_ID'].item() == 'X#Y':
#                            parent_actor_name = 'X#YDUMMYACTOR'
#                        else:
#                            parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['parent_actor_ID'].item(), 'actor_name'].iloc[0]
#
#                        if link_row_df['child_actor_ID'].item() == 'X#Y':
#                            child_actor_name = 'X#YDUMMYACTOR'
#                        else:
#                            child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['child_actor_ID'].item(), 'actor_name'].iloc[0]
#
#
#                        link_description = parent_element+" linked to "+child_element+", via the link "+link_row_df['relation_type'] 
#
#                        merged_relations_df.drop(merged_relations_df[merged_relations_df['relation_ID'] == link_ID].index, inplace = True)
#                        merged_relations_df = merged_relations_df.reset_index(drop=True)
#                        traceError(link_ID, 'Direct Cycle', 'Drop Link', link_description, parent_actor_name+" - "+child_actor_name)
#                        if continueCheckingCycles(points_of_possible_cycles[x]):
#                            cycle_exists = True 
#                            links_to_break.drop(links_to_break[links_to_break['relation_ID'] == link_ID].index, inplace=True)
#                            links_to_break = links_to_break.reset_index(drop=True)
#                        else:
#                            cycle_exists = False


def checkIndirectCycles(mergingMethod):
    global merged_relations_df
    global new_relations_df
    
    unique_parents_IDs = merged_relations_df['parent_element_ID'].unique().tolist()
    unique_children_IDs = merged_relations_df['child_element_ID'].unique().tolist()

    points_of_possible_cycles = list(set(unique_parents_IDs).intersection(unique_children_IDs))
#     print("***", points_of_possible_cycles)

    for x in range(len(points_of_possible_cycles)):
#         print("Possible cycle at: ", points_of_possible_cycles[x])
        relation_copy_1 = merged_relations_df.copy()
        relation_copy_2 = merged_relations_df.copy()
        links_to_break = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
        new_links_rows = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])

        # Get all parents and children of possible point of cycle
        parents_IDs = getAllParents(points_of_possible_cycles[x], [], relation_copy_1)
        children_IDs = getAllChildren(points_of_possible_cycles[x], [], relation_copy_2)

        if not parents_IDs is None and not children_IDs is None:
            # Get the elements causing the cycles
            cycle_location = list(set(parents_IDs).intersection(children_IDs))
#             if len(cycle_location) > 0:
#                 print("A cycle between the elements", cycle_location)
            # Get the relations DF that causing the cycles
            for c in range(len(cycle_location)):
                for d in range(len(cycle_location)-1):
#                     print("LOCATION:", cycle_location[c])
                    links_df = merged_relations_df.loc[((merged_relations_df['parent_element_ID'] == cycle_location[c]) & (merged_relations_df['child_element_ID'] == cycle_location[d+1])) | ((merged_relations_df['child_element_ID'] == cycle_location[c]) & (merged_relations_df['parent_element_ID'] == cycle_location[d+1]))]
                    links_df = links_df.reset_index(drop=True)
                    links_to_break = links_to_break.append(links_df)
                    links_to_break = links_to_break.reset_index(drop=True)
#                     print("---", links_to_break)
            links_to_break = links_to_break.drop_duplicates().reset_index(drop=True)   
            if not links_to_break.empty:
                new_link_broken = False
                if mergingMethod == '1':
                    for l in range(len(links_to_break)):
                        # The link to break exists in the merged model and it is from the non-base model
                        new_link_row = new_relations_df.loc[((new_relations_df['parent_actor_ID'] == links_to_break.iloc[l]['parent_actor_ID']) & (new_relations_df['parent_element_ID'] == links_to_break.iloc[l]['parent_element_ID']) & (new_relations_df['relation_type'] == links_to_break.iloc[l]['relation_type']) & (new_relations_df['parent_actor_ID'] == links_to_break.iloc[l]['parent_actor_ID']) &  (new_relations_df['child_element_ID'] == links_to_break.iloc[l]['child_element_ID']))]
                        new_link_row = new_link_row.reset_index(drop=True)

                        if not new_link_row.empty:
                            # drop the link from the new relation
                            new_relations_df.drop(new_relations_df[(new_relations_df['parent_element_ID'] == links_to_break.iloc[l]['parent_element_ID']) & (new_relations_df['relation_type'] == links_to_break.iloc[l]['relation_type']) & (new_relations_df['child_element_ID'] == links_to_break.iloc[l]['child_element_ID'])].index, inplace = True)
                            new_relations_df = new_relations_df.reset_index(drop=True)
                            if new_link_row['relation_ID'].item() in merged_relations_df['relation_ID'].values:
                                new_link_broken = True
                                mergingMethod = '1'
#                                 link_row_df = merged_relations_df[merged_relations_df['relation_ID'] == new_link_row['relation_ID'].item()]
                                parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == new_link_row['parent_element_ID'].item(), 'ielement_name'].iloc[0]
                                child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == new_link_row['child_element_ID'].item(), 'ielement_name'].iloc[0]

#                                 parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  new_link_row['parent_actor_ID'].item(), 'actor_name'].iloc[0]
#                                 child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  new_link_row['child_actor_ID'].item(), 'actor_name'].iloc[0]


                                if new_link_row['parent_actor_ID'].item() == 'X#Y':
                                    parent_actor_name = 'X#YDUMMYACTOR'
                                else:
                                    parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  new_link_row['parent_actor_ID'].item(), 'actor_name'].iloc[0]

                                if new_link_row['child_actor_ID'].item() == 'X#Y':
                                    child_actor_name = 'X#YDUMMYACTOR'
                                else:
                                    child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  new_link_row['child_actor_ID'].item(), 'actor_name'].iloc[0]

                                link_description = parent_element+" linked to "+child_element+", via the link "+new_link_row['relation_type'].item()

                                merged_relations_df.drop(merged_relations_df[merged_relations_df['relation_ID'] == new_link_row['relation_ID'].item()].index, inplace = True)
                                merged_relations_df = merged_relations_df.reset_index(drop=True)

#                                 traceConflict('', '', '', '', link_description, new_link_row['relation_ID'].item(), 'dropped_link')
                                traceError(new_link_row['relation_ID'].item(), 'Indirect Cycle', 'Drop Link', link_description, parent_actor_name+"-"+child_actor_name)

                            if continueCheckingCycles(points_of_possible_cycles[x]):
                                continue 
                            else:
                                break
                        # to check that the cycle has been resolved by dropping a link from the new model
                if not new_link_broken and mergingMethod == '1':
                    print("There is a cycle could not be resolved automatically")
                    mergingMethod = '2'
                            
#                     else:
#                         mergingMethod = '2'
                if mergingMethod == '2':
                    cycle_exists = True 
                    while cycle_exists:
                        print("An indirect cycle between:")
                        for l in range(len(links_to_break)):
                            parent_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == links_to_break.iloc[l]['parent_element_ID'], 'ielement_name'].iloc[0]
                            child_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == links_to_break.iloc[l]['child_element_ID'], 'ielement_name'].iloc[0]

                            if links_to_break.iloc[l]['relation_type'] == 'decomposition':
                                print(l+1, "- Parent element: (", parent_element_name, ") Decomposed by Child Element: (", child_element_name, ") with", links_to_break.iloc[l]['decomposition_type'], "-Decomposition")
                            elif links_to_break.iloc[l]['relation_type'] == 'contribution':
                                print(l+1, "- Child Element: (", child_element_name, ") Contributes to Parent Element: (", parent_element_name, ") with contribution value = ", links_to_break.iloc[l]['contribution_value'])
                            elif links_to_break.iloc[l]['relation_type'] == 'dependency':
                                print(l+1, "- Parent Element: (", parent_element_name, ") Depends on Child Element: (", child_element_name, ")")
                                
                        print("Select one of the links to be removed for resolving the cycle")

                        
                        while True:
                            link_number = input("Enter the link number to break: ")
                            try:
                                link_number = int(link_number)
                                if link_number > 0 and link_number <= len(links_to_break):
                                    break;
                                else:
                                    print("Please enter a valid input (1 to "+str(len(links_to_break))+")")
                                    continue;
                            except ValueError:
                                print("Please enter a valid input (1 to "+str(len(links_to_break))+")")
#                            link_number = input("Enter the link number to break: ")
                        
                        link_number = int(link_number) - 1
                        link_row = links_to_break.iloc[[link_number]]
                        link_ID = link_row['relation_ID'].item()

                        link_row_df = merged_relations_df[merged_relations_df['relation_ID'] == link_ID]
                        parent_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['parent_element_ID'].item(), 'ielement_name'].iloc[0]
                        child_element = merged_model_df.loc[merged_model_df['ielement_ID'] == link_row_df['child_element_ID'].item(), 'ielement_name'].iloc[0]
                        
                        if link_row_df['parent_actor_ID'].item() == 'X#Y':
                            parent_actor_name = 'X#YDUMMYACTOR'
                        else:
                            parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['parent_actor_ID'].item(), 'actor_name'].iloc[0]
                        
                        if link_row_df['child_actor_ID'].item() == 'X#Y':
                            child_actor_name = 'X#YDUMMYACTOR'
                        else:
                            child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  link_row_df['child_actor_ID'].item(), 'actor_name'].iloc[0]

                        link_description = parent_element+" linked to "+child_element+", via the link "+link_row_df['relation_type'].item()

                        merged_relations_df.drop(merged_relations_df[merged_relations_df['relation_ID'] == link_ID].index, inplace = True)
                        merged_relations_df = merged_relations_df.reset_index(drop=True)
#                         traceConflict('', '', '', '', link_description, link_ID, 'dropped_link')
                        traceError(link_ID, 'Indirect Cycle', 'Drop Link', link_description, parent_actor_name+"-"+child_actor_name)

                        if continueCheckingCycles(points_of_possible_cycles[x]):
                            cycle_exists = True 
                            links_to_break.drop(links_to_break[links_to_break['relation_ID'] == link_ID].index, inplace=True)
                            links_to_break = links_to_break.reset_index(drop=True)
                        else:
                            cycle_exists = False
                            
def continueCheckingCycles(possible_cycle_point):
    relation_copy_1 = merged_relations_df.copy()
    relation_copy_2 = merged_relations_df.copy()

    # Get all parents and children of possible point of cycle
    parents_IDs = getAllParents(possible_cycle_point, [], relation_copy_1)
    children_IDs = getAllChildren(possible_cycle_point, [], relation_copy_2)
    if not parents_IDs is None and not children_IDs is None:
        cycle_location = list(set(parents_IDs).intersection(children_IDs))
        if len(cycle_location) > 0:
            return True
    else:
        return False    
    
    
# Function to get all parents of an element (till the root)
def getAllParents(child_ID, parents, relations_df):
    element_parents = pd.DataFrame(relations_df.loc[relations_df['child_element_ID'] == child_ID])
    element_parents.reset_index(drop=True)
    
    relations_df.drop(relations_df[relations_df['child_element_ID'] == child_ID].index, inplace = True)
    relations_df.reset_index(drop=True)
#     print("###", element_parents)
    
    if not element_parents.empty:
        parents_list = element_parents['parent_element_ID'].to_list()
        for p in range(len(parents_list)):
            parent_ID = parents_list[p]
            parents.append(parent_ID)
            getAllParents(parent_ID, parents, relations_df)
            
    if len(parents) != 0:
        parents = uniqueList(parents)
        return parents
    
# Function to get all children of an element (till the leaf)
def getAllChildren(parent_ID, children, relations_df):
    element_children = pd.DataFrame(relations_df.loc[relations_df['parent_element_ID'] == parent_ID])
    element_children.reset_index(drop=True)  
    
    relations_df.drop(relations_df[relations_df['parent_element_ID'] == parent_ID].index, inplace = True)
    relations_df.reset_index(drop=True)
#     print("###", element_children)
    
    if not element_children.empty:
        children_list = element_children['child_element_ID'].to_list()
        for c in range(len(children_list)):
            child_ID = children_list[c]
            children.append(child_ID)
            getAllChildren(child_ID, children, relations_df)
            
    if len(children) != 0:
        children = uniqueList(children)
        return children
    
# Get unique elements of list
def uniqueList(a_list):
    # insert the list to the set
    list_set = set(a_list)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list

def checkSiblingsRelations(mergingMethod):
    parents = merged_relations_df['parent_element_ID'].unique()
#     print("PARENTS")
#     print(parents)
    global t 
    for p in range(len(parents)):
#         print("Working on parent", parents[p])
        # Get the siblings based on parent ID
        siblings = pd.DataFrame(merged_relations_df.loc[merged_relations_df['parent_element_ID'] == parents[p]])
        siblings_relations = siblings['relation_type'].unique().tolist()
        siblings_IDs = siblings['child_element_ID'].to_list()
        current_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == parents[p], 'ielement_name'].iloc[0]

#         print("==== Siblings IDS", siblings_IDs)
        if len(siblings_relations) > 0: #Siblings have the same relation type
            # for now no need to check the contribution values
            # unless we created some formula to make their summation equals 100
            if 'decomposition' in siblings_relations:
                decomposition_type = siblings['decomposition_type'].unique().tolist()
                while("" in decomposition_type):
                    decomposition_type.remove("")
                
                if len(decomposition_type) > 1: #siblings have different decomposition values
#                     print("TWO DECOMPOSITION", decomposition_type)
                    if mergingMethod == "1": # Automatic approach
                        elementsToTempIDs = []
                        # Check if the parent is merged (I have to look into the parent if merged because there could be merged elements from different merged parent)
                        if parents[p].find("+") != -1:
                            # Split the siblings based on relation
                            base_siblings_type_df, new_siblings_type_df = splitSiblingsByRelation(siblings, decomposition_type, 'decomposition_type', parents[p])
                            base_decomposition_type = (base_siblings_type_df['decomposition_type'].unique().tolist())[0]
                            new_decomposition_type = (new_siblings_type_df['decomposition_type'].unique().tolist())[0]
                            for nst in range(len(new_siblings_type_df)):
                                # Check if at least one is merged and it is originally from the new model siblings
                                if mergedOriginalSiblings(base_siblings_type_df, new_siblings_type_df.iloc[nst], 'decomposition_type'):
#                                     print("YES we will change the relation type")
#                                     print("----", new_siblings_type_df.iloc[nst]['child_element_ID'])
#                                    toChangeIndex = merged_relations_df.index[(merged_relations_df['child_element_ID'] == new_siblings_type_df.iloc[nst]['child_element_ID']) & (merged_relations_df['decomposition_type'] != base_decomposition_type)]
    
                                    toChangeIndex = merged_relations_df.index[(merged_relations_df['child_element_ID'] == new_siblings_type_df.iloc[nst]['child_element_ID']) & (merged_relations_df['child_actor_ID'] == new_siblings_type_df.iloc[nst]['child_actor_ID']) & (merged_relations_df['decomposition_type'] != base_decomposition_type)]

                                    for ti in toChangeIndex:
                                        parent_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == merged_relations_df['parent_element_ID'][ti], 'ielement_name'].iloc[0]
                                        child_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == merged_relations_df['child_element_ID'][ti], 'ielement_name'].iloc[0]
                        
                                        if merged_relations_df['parent_actor_ID'][ti] == 'X#Y':
                                            parent_actor_name = 'X#YDUMMYACTOR'
                                        else:
                                            parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  merged_relations_df['parent_actor_ID'][ti], 'actor_name'].iloc[0]
                                            
                                        if merged_relations_df['child_actor_ID'][ti] == 'X#Y':   
                                            child_actor_name = 'X#YDUMMYACTOR'
                                        else:
                                            child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  merged_relations_df['child_actor_ID'][ti], 'actor_name'].iloc[0]

                            
                                        traceError(merged_relations_df['child_element_ID'][ti], 'Multiple Decomposition Types', 'Unify decomposition types', 'Change '+new_decomposition_type+' to '+base_decomposition_type+' of the decomposition link between the parent '+parent_element_name+' and the child '+child_element_name, parent_actor_name+" - "+child_actor_name)
                                
                                        merged_relations_df['decomposition_type'][ti] = base_decomposition_type
                                else:
                                    elementsToTempIDs.append(new_siblings_type_df.iloc[nst]['child_element_ID'])

                        if len(elementsToTempIDs) > 0:
                            elements_to_temp_df = pd.DataFrame(new_siblings_type_df.loc[(new_siblings_type_df['child_element_ID'].isin(elementsToTempIDs))])

                            top_relation_df, bottom_relations_df = getReferenceDF(siblings, 'decomposition', base_decomposition_type,  elements_to_temp_df, new_decomposition_type)

                            reference_element_df = pd.DataFrame(merged_model_df.loc[(merged_model_df['ielement_ID'] == top_relation_df['child_element_ID'].item()) & (merged_model_df['ielement_ID'].isin(siblings_IDs))])

                            # ID for the new temporary element
                            t = t + 1
                            temp_ID = "TEMP"+str(t)

                            addTemporaryElement(top_relation_df, reference_element_df, temp_ID)

                            updateTempParent(bottom_relations_df, temp_ID, parents[p])
                    # End of the automatic approach
                    elif mergingMethod == "2": # Interactive approach
                        if parents[p].find("+") != -1:
                            decomposition_type_1 = decomposition_type[0]
                            decomposition_type_2 = decomposition_type[1]
                            
                            # Split the siblings based on decomposition type
                            base_siblings_type_df = pd.DataFrame(siblings.loc[siblings['decomposition_type'] == decomposition_type_1])
                            new_siblings_type_df = pd.DataFrame(siblings.loc[siblings['decomposition_type'] == decomposition_type_2])

                            base_decomposition_type = (base_siblings_type_df['decomposition_type'].unique().tolist())[0]
#                             print(new_siblings_type_df['decomposition_type'])
                            new_decomposition_type = (new_siblings_type_df['decomposition_type'].unique().tolist())[0]
    
                            base_element_name = merged_model_df.loc[merged_model_df['ielement_ID'].isin(base_siblings_type_df['child_element_ID'].to_list()), 'ielement_name']
                            new_element_name = merged_model_df.loc[merged_model_df['ielement_ID'].isin(new_siblings_type_df['child_element_ID'].to_list()), 'ielement_name']
                            

                            print("The intentional element (", current_element_name, ") has children with multiple decomposition types")
                            print("1- The elements", base_element_name.to_list(), "linked via a decomposition of type", (base_siblings_type_df['decomposition_type'].unique().tolist())[0])
                            print("2- The elements", new_element_name.to_list(), "linked via a decomposition of type", (new_siblings_type_df['decomposition_type'].unique().tolist())[0])
                            
#                            print("Conflict in the decomposition type among siblings: ")
#                            print("1- The elements", base_siblings_type_df['child_element_ID'].to_list(), "linked to", (base_siblings_type_df['parent_element_ID'].unique().tolist())[0], "with a decomposition of type", (base_siblings_type_df['decomposition_type'].unique().tolist())[0])
#                            print("2- The elements", new_siblings_type_df['child_element_ID'].to_list(), "linked to", (new_siblings_type_df['parent_element_ID'].unique().tolist())[0], "with a decomposition of type", (new_siblings_type_df['decomposition_type'].unique().tolist())[0])
                            print("Would you like to unify the decomposition type or add a temporary element?")
                            print("1- Unify the decomposition types")
                            print("2- Add temporary element")
                            while True:
                                conflict_solution_choice = input("1 | 2 :")
                                try:
                                    conflict_solution_choice = int(conflict_solution_choice)
                                    if conflict_solution_choice == 1 or conflict_solution_choice == 2:
                                        break;
                                    else:
                                        print("Please enter a valid input (1 or 2)")
                                        continue;
                                except ValueError:
                                    print("Please enter a valid input (1 or 2)")
                            
                            
#                            conflict_solution_choice = input("1 | 2 :")
                            if conflict_solution_choice == 1: # Unify the type
                                print("Which decomposition type to retain?")

                                print("1-", base_decomposition_type)
                                print("2-", new_decomposition_type)
                                while True:
                                    type_choice = input("1 | 2 :")
                                    try:
                                        type_choice = int(type_choice)
                                        if type_choice == 1 or type_choice == 2:
                                            break;
                                        else:
                                            print("Please enter a valid input (1 or 2)")
                                            continue;
                                    except ValueError:
                                        print("Please enter a valid input (1 or 2)")
                                
#                                type_choice = input("1 | 2 :")
                                if type_choice == 1:
                                    toChangeIndex = merged_relations_df.index[(merged_relations_df['child_element_ID'].isin(new_siblings_type_df['child_element_ID'].to_list())) & (merged_relations_df['decomposition_type'] != base_decomposition_type)]

                                    for ti in toChangeIndex:
                                        parent_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == merged_relations_df['parent_element_ID'][ti], 'ielement_name'].iloc[0]
                                        child_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == merged_relations_df['child_element_ID'][ti], 'ielement_name'].iloc[0]
                            
                            
                                        if merged_relations_df['parent_actor_ID'][ti] == 'X#Y':
                                            parent_actor_name = 'X#YDUMMYACTOR'
                                        else:
                                            parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  merged_relations_df['parent_actor_ID'][ti], 'actor_name'].iloc[0]
                                            
                                        if merged_relations_df['child_actor_ID'][ti] == 'X#Y':   
                                            child_actor_name = 'X#YDUMMYACTOR'
                                        else:
                                            child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  merged_relations_df['child_actor_ID'][ti], 'actor_name'].iloc[0]

                            
                                        traceError(merged_relations_df['child_element_ID'][ti], 'Multiple Decomposition Types', 'Unify decomposition types', 'Change '+new_decomposition_type+' to '+base_decomposition_type+' of the decomposition link between the parent '+parent_element_name+' and the child '+child_element_name, parent_actor_name+" - "+child_actor_name)
                                    
                                        merged_relations_df['decomposition_type'][ti] = base_decomposition_type
                                elif type_choice == 2:
                                    toChangeIndex = merged_relations_df.index[(merged_relations_df['child_element_ID'].isin(base_siblings_type_df['child_element_ID'].to_list())) & (merged_relations_df['decomposition_type'] != new_decomposition_type)]
                                    for ti in toChangeIndex:
                                        parent_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == merged_relations_df['parent_element_ID'][ti], 'ielement_name'].iloc[0]
                                        child_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == merged_relations_df['child_element_ID'][ti], 'ielement_name'].iloc[0]
                                        
                                        
                                        if merged_relations_df['parent_actor_ID'][ti] == 'X#Y':
                                            parent_actor_name = 'X#YDUMMYACTOR'
                                        else:
                                            parent_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  merged_relations_df['parent_actor_ID'][ti], 'actor_name'].iloc[0]
                                            
                                        if merged_relations_df['child_actor_ID'][ti] == 'X#Y':   
                                            child_actor_name = 'X#YDUMMYACTOR'
                                        else:
                                            child_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  merged_relations_df['child_actor_ID'][ti], 'actor_name'].iloc[0]

                            
                                        traceError(merged_relations_df['child_element_ID'][ti], 'Multiple Decomposition Types', 'Unify decomposition types', 'Change '+base_decomposition_type+' to '+new_decomposition_type+' of the decomposition link between the parent '+parent_element_name+' and the child '+child_element_name, parent_actor_name+" - "+child_actor_name)                                  

                                        merged_relations_df['decomposition_type'][ti] = new_decomposition_type
                            elif conflict_solution_choice == 2: # Add temporary element
                                print("Which decomposition type will be assigned to the temporary element?")
                                print("1-", base_decomposition_type)
                                print("2-", new_decomposition_type)
                                while True:
                                    type_choice = input("1 | 2 :")
                                    try:
                                        type_choice = int(type_choice)
                                        if type_choice == 1 or type_choice == 2:
                                            break;
                                        else:
                                            print("Please enter a valid input (1 or 2)")
                                            continue;
                                    except ValueError:
                                        print("Please enter a valid input (1 or 2)")
#                                type_choice = input("1 | 2 :")
                                if type_choice == 1:
                                    top_relation_df, bottom_relations_df = getReferenceDF(siblings, 'decomposition', new_decomposition_type,  base_siblings_type_df, base_decomposition_type)
                                elif type_choice == 2:
                                    top_relation_df, bottom_relations_df = getReferenceDF(siblings, 'decomposition', base_decomposition_type,  new_siblings_type_df, new_decomposition_type)

#                                reference_element_df = pd.DataFrame(merged_model_df.loc[(merged_model_df['ielement_ID'] == top_relation_df['child_element_ID'].item()) & (merged_model_df['ielement_ID'].isin(siblings_IDs))])
                            
                                top_relation_IDs = top_relation_df['child_element_ID'].tolist()
                                reference_elements_df = pd.DataFrame(merged_model_df.loc[(merged_model_df['ielement_ID'].isin(top_relation_IDs)) & (merged_model_df['ielement_ID'].isin(siblings_IDs))])
                                if len(reference_elements_df) > 1:
                                    reference_element_types = reference_elements_df['ielement_type'].unique().tolist()
                                    # There are more than one type of the elements connected via the retained decomposition type
                                    if len(reference_element_types) > 1:
                                        print("What is the type of the temporary intentional elements?")
                                        for r in range(len(reference_element_types)):
                                            print(r+1, "- ", reference_element_types[r])
#                                        element_type_number = input("Enter the number of the intentional element type: ")
                                        
                                        while True:
                                            element_type_number = input("Enter the number of the intentional element type: ")
                                            try:
                                                element_type_number = int(element_type_number) - 1
                                                if element_type_number >= 0 and element_type_number < len(reference_element_types):
                                                    break;
                                                else:
                                                    print("Please enter a valid input (between 1 and ", len(reference_element_types))
                                                    continue;
                                            except ValueError:
                                                print("Please enter a valid input (between 1 and ", len(reference_element_types))
                                        
                                        
#                                        element_type_number = int(element_type_number) - 1   
                                        element_type = reference_element_types[element_type_number]
                                        
                                        reference_element_df = pd.DataFrame(reference_elements_df.loc[(reference_elements_df['ielement_type'] == element_type)])
                                        reference_element_df = reference_element_df.head(1)
                                    else:
                                        reference_element_df = reference_elements_df.head(1)
                                else:
                                    reference_element_df = reference_elements_df.head(1)
                                
                                top_relation_df = top_relation_df.head(1)

                                # ID for the new temporary element
                                t = t + 1
                                temp_ID = "TEMP"+str(t)

                                addTemporaryElement(top_relation_df, reference_element_df, temp_ID)

                                updateTempParent(bottom_relations_df, temp_ID, parents[p])
                                
def splitSiblingsByRelation(siblingsDF, relation_types, differences, parent_ID):
    base_siblings_type_df = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
    new_siblings_type_df = pd.DataFrame(columns=['relation_ID','parent_actor_ID','parent_element_ID', 'relation_type', 'child_actor_ID', 'child_element_ID', 'decomposition_type', 'contribution_value'])
    base_relation_type = ''
    
    # Copy it so the original relation_types won't be affected when removing elements
    relations_to_check = list(relation_types)
    
    # Get the base relations of the current parent
    current_base_relations = pd.DataFrame(base_relations_df.loc[base_relations_df['parent_element_ID'] == parent_ID])

    # Get siblings that are from the base model
    base_siblings_type_df = pd.DataFrame(siblingsDF.loc[siblingsDF['child_element_ID'].isin(current_base_relations['child_element_ID'].to_list())])
    
    # Get the relation type of the base siblings
    base_relation_type = base_siblings_type_df[differences].unique().tolist()
    
    base_relation_type = base_relation_type[0]
   
    # Get the new relation type by removing the base relation type
    relations_to_check.remove(base_relation_type)
    new_relation_type = relations_to_check[0]
       
    # Get the new siblings of the current parent
    current_new_relations = pd.DataFrame(new_relations_df.loc[new_relations_df['parent_element_ID'] == parent_ID])

    # Get siblings from the new model and based on the relation type 
    new_siblings_type_df = pd.DataFrame(siblingsDF.loc[(siblingsDF['child_element_ID'].isin(current_new_relations['child_element_ID'].to_list())) & (siblingsDF[differences] == new_relation_type)])
 

    return base_siblings_type_df, new_siblings_type_df

def mergedOriginalSiblings(base_siblings_type_df, new_sibling_type_df, difference):
    mergedSibling = False
    # Get the base siblings IDs
    base_siblings_IDs = base_siblings_type_df['child_element_ID'].to_list()
        
    # Get the parents of the new elements
    new_sibling_ID = new_sibling_type_df['child_element_ID']

    new_element_parent = pd.DataFrame(new_original_siblings_df.loc[new_original_siblings_df['element_ID'] == new_sibling_ID, 'parent_ID'].unique())

    # Check that any element from the original base siblings is merged
    for i in range(len(base_siblings_IDs)):
        if base_siblings_IDs[i].find('+') != -1:
            sibling_to_check = (base_siblings_IDs[i].split('+'))[-1]
#            print(sibling_to_check)
            merged_element_parent = pd.DataFrame(new_original_siblings_df.loc[new_original_siblings_df['element_ID'] == sibling_to_check, 'parent_ID'])
    
            # Check that if the merged element's parent is parent of the new siblings
            if (elem in merged_element_parent for elem in new_element_parent):
                mergedSibling = True
#                 print("Yes they are siblings")
            else:
                print(" ")
#                 print("Not original siblings")
    return mergedSibling

def getReferenceDF(siblingsDF, top_relation_type, top_relation_value, bottom_relation_elements_df, bottom_relation_value):
#     print("TOP RELATION VALUE", top_relation_value)
    if top_relation_type == "contribution":
        top_relation_df = pd.DataFrame(siblingsDF.loc[siblingsDF['relation_type'] == 'contribution'])
    elif top_relation_type == "decomposition":
        top_relation_df = pd.DataFrame(siblingsDF.loc[siblingsDF['decomposition_type'] == top_relation_value])
        
    # Get one element of the current parent\relation DF to use it as a reference
#    top_relation_df = top_relation_df.head(1)
    
    if bottom_relation_value != '':
        bottom_relations_df = pd.DataFrame(bottom_relation_elements_df.loc[bottom_relation_elements_df['decomposition_type'] == bottom_relation_value])
    else: 
        bottom_relations_df = pd.DataFrame(bottom_relation_elements_df.loc[bottom_relation_elements_df['relation_type'] == 'contribution'])


    return top_relation_df, bottom_relations_df


def addTemporaryElement(top_relation_df, reference_element_df, temp_element_ID):
    global merged_model_df
    global merged_relations_df
    
    # Add the new temporary element
    # For now we are adding empty element attributes, maybe later we can use NLP to get some text to be used for the temporary element, or ask the user to fill it
    merged_element_row = {'model_name': 'merged_model','actor_ID': reference_element_df['actor_ID'].item(), 'ielement_type': reference_element_df['ielement_type'].item(), 'ielement_ID': temp_element_ID, 'ielement_name': "Temporary Element "+temp_element_ID, 'ielement_description': '', 'ielement_importance': '', 'ielement_metadata': '', 'ielement_decomposition_type': reference_element_df['ielement_type'].item()}
    merged_model_df = merged_model_df.append(merged_element_row, ignore_index=True)
    
    if top_relation_df['relation_type'].item() == 'contribution':
        # If the new temporary element contributes to the parent, we set the contribution value = 25
        # Later we might have some calculations for that
        temp_contribution_value = 25
    else:
        temp_contribution_value = ''
    
    # Add the relation connects the temporary element to the original parent element
    merged_relation_row = {'relation_ID': "R"+temp_element_ID, 'parent_actor_ID': top_relation_df['parent_actor_ID'].item(), 'parent_element_ID': top_relation_df['parent_element_ID'].item(), 'relation_type': top_relation_df['relation_type'].item(), 'child_actor_ID': top_relation_df['child_actor_ID'].item(), 'child_element_ID': temp_element_ID, 'decomposition_type': top_relation_df['decomposition_type'].item(), 'contribution_value': temp_contribution_value}
    merged_relations_df = merged_relations_df.append(merged_relation_row, ignore_index=True)
    
# Update the parent ID for elements that will be connected via the temporary element (due to the different relations)
def updateTempParent(to_change_relations_df, temp_element_ID, parent_ID):
    to_change_IDs = to_change_relations_df['child_element_ID'].to_list()
    for mr in range(len(merged_relations_df)):
        if (merged_relations_df['child_element_ID'][mr] in to_change_IDs and merged_relations_df['parent_element_ID'][mr] == parent_ID):
            parent_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == merged_relations_df['parent_element_ID'][mr], 'ielement_name'].iloc[0]
            child_element_name = merged_model_df.loc[merged_model_df['ielement_ID'] == merged_relations_df['child_element_ID'][mr], 'ielement_name'].iloc[0]
            
            if merged_relations_df['parent_actor_ID'][mr] == 'X#Y':
                current_actor_name = 'X#YDUMMYACTOR'
            else:
                current_actor_name = merged_actors_df.loc[merged_actors_df['actor_ID'] ==  merged_relations_df['parent_actor_ID'][mr], 'actor_name'].iloc[0]
                                                                   
            traceError(temp_element_ID, 'Multiple Decomposition Types', 'Add temporary parent', 'Add temporarily element connecting the child '+child_element_name+' to the parent '+parent_element_name, current_actor_name)
            merged_relations_df['parent_element_ID'][mr] = temp_element_ID 

def cleanIDs():
    # Remove the plus sign from the merged model
    for i in range(len(merged_actors_df)):
        merged_actors_df['actor_ID'][i] = re.sub('[+]', '', merged_actors_df['actor_ID'][i])

    for i in range(len(merged_model_df)):
        merged_model_df['actor_ID'][i] = re.sub('[+]', '', merged_model_df['actor_ID'][i])
        merged_model_df['ielement_ID'][i] = re.sub('[+]', '', merged_model_df['ielement_ID'][i])

    for i in range(len(merged_relations_df)):
        merged_relations_df['parent_actor_ID'][i] = re.sub('[+]', '', merged_relations_df['parent_actor_ID'][i])
        merged_relations_df['parent_element_ID'][i] = re.sub('[+]', '', merged_relations_df['parent_element_ID'][i])
        merged_relations_df['child_actor_ID'][i] = re.sub('[+]', '', merged_relations_df['child_actor_ID'][i])
        merged_relations_df['child_element_ID'][i] = re.sub('[+]', '', merged_relations_df['child_element_ID'][i])
        merged_relations_df['relation_ID'][i] = re.sub('[+]', '', merged_relations_df['relation_ID'][i])

    for i in range(len(trace_conflict_df)):
        trace_conflict_df['m_ID'][i] = re.sub('[+]', '', trace_conflict_df['m_ID'][i])
    global mergedActorsIDs
    mergedActorsIDs = merged_actors_df['actor_ID'].to_list()
    
    
def DFtoTGRL():
    mergedActorsIDs.append('X#Y')
    global tgrlList
    tgrlList = []
    global input_model_a_name
    global input_model_b_name
    # process dummy actors differently
    tgrlList.append("grl mergedModel {")
    for i in range(len(mergedActorsIDs)):
        currentMergedActor = pd.DataFrame(merged_actors_df.loc[merged_actors_df['actor_ID'] == mergedActorsIDs[i]])
        if mergedActorsIDs[i] != 'X#Y':
            tgrlList.append('actor '+ mergedActorsIDs[i] + " {")
            if currentMergedActor['actor_name'].item() != "":
                tgrlList.append('name = \"' + currentMergedActor['actor_name'].item() + '\";')
            if currentMergedActor['actor_description'].item() != "": 
                tgrlList.append('description = \"' + currentMergedActor['actor_description'].item() + '\";')
            if currentMergedActor['actor_importance'].item() != "": 
                tgrlList.append('importance = ' + str(currentMergedActor['actor_importance'].item()) + ';')   
            if currentMergedActor['actor_metadata'].item() != "": 
                tgrlList.append('metadata ' + currentMergedActor['actor_metadata'].item())
        elementsOfMergedActor = pd.DataFrame(merged_model_df.loc[merged_model_df['actor_ID'] == mergedActorsIDs[i]])
        elementsOfMergedActor = elementsOfMergedActor.reset_index(drop=True)
        if not elementsOfMergedActor.empty:
            for me in range(len(elementsOfMergedActor)):
                tgrlList.append(elementsOfMergedActor['ielement_type'][me]+ " " + elementsOfMergedActor['ielement_ID'][me] + " {")
                if elementsOfMergedActor['ielement_type'][me] == 'belief':
                    if elementsOfMergedActor['ielement_name'][me] != "":
                        tgrlList.append('name = \"' + elementsOfMergedActor['ielement_description'][me] + '\";')
                    if elementsOfMergedActor['ielement_description'][me] != "":
                        tgrlList.append('description = \"' + elementsOfMergedActor['ielement_name'][me] + '\";')
                else:   
                    if elementsOfMergedActor['ielement_name'][me] != "":
                        tgrlList.append('name = \"' + elementsOfMergedActor['ielement_name'][me] + '\";')
                    if elementsOfMergedActor['ielement_description'][me] != "":
                        tgrlList.append('description = \"' + elementsOfMergedActor['ielement_description'][me] + '\";')
                if elementsOfMergedActor['ielement_importance'][me] != "":
                    tgrlList.append('importance = ' + str(elementsOfMergedActor['ielement_importance'][me]) + ';') 
                if elementsOfMergedActor['ielement_metadata'][me] != "":
                    tgrlList.append('metadata ' + elementsOfMergedActor['ielement_metadata'][me])  
                decompositionType = getDecompositionType(elementsOfMergedActor['ielement_ID'][me])
                if decompositionType != "":
                    tgrlList.append('decompositionType = ' + str(decompositionType) + ';')
                tgrlList.append('}') #closing the intentional element
        relationsOfMergedActor = pd.DataFrame(merged_relations_df.loc[merged_relations_df['parent_actor_ID'] == mergedActorsIDs[i]])
        relationsOfMergedActor = relationsOfMergedActor.reset_index(drop=True)
        if not relationsOfMergedActor.empty:
            for rm in range(len(relationsOfMergedActor)):
                if mergedActorsIDs[i] != 'X#Y':
                    if relationsOfMergedActor['parent_actor_ID'][rm] == relationsOfMergedActor['child_actor_ID'][rm]:
                        childActor = ""
                    elif relationsOfMergedActor['child_actor_ID'][rm] == 'X#Y':
                        childActor = ""
                    else:
                        childActor = relationsOfMergedActor['child_actor_ID'][rm]+"."
                else:
                    if relationsOfMergedActor['child_actor_ID'][rm] == 'X#Y':
                        childActor = ""
                    else:
                        childActor = relationsOfMergedActor['child_actor_ID'][rm]+"."

                if relationsOfMergedActor['relation_type'][rm] == 'decomposition':
                    relationType = 'decomposedBy'
                    relation = relationsOfMergedActor['parent_element_ID'][rm] + " "+ relationType + " " + childActor+ relationsOfMergedActor['child_element_ID'][rm]
                elif relationsOfMergedActor['relation_type'][rm] == 'contribution':
                    relationType = 'contributesTo'
                    relation = childActor + relationsOfMergedActor['child_element_ID'][rm] + " "+ relationType + " " + relationsOfMergedActor['parent_element_ID'][rm]
                elif relationsOfMergedActor['relation_type'][rm] == 'dependency':
                    relationType = 'dependsOn'
                    relation = relationsOfMergedActor['parent_element_ID'][rm] + " "+ relationType + " " + childActor + relationsOfMergedActor['child_element_ID'][rm]

                if relationType == 'contributesTo':
                    contributionValue = str(relationsOfMergedActor['contribution_value'][rm])
                    if contributionValue.lstrip('-+').isdigit():
                        contributionValue = int(contributionValue)
                        if contributionValue < 0 and contributionValue >= -25:
                            contributionValue = 'hurt'
                        elif contributionValue < -25 and contributionValue >= -75:
                            contributionValue = 'someNegative';
                        elif contributionValue < -75 and contributionValue >= 100:
                            contributionValue = 'break';
                    tgrlList.append(relation + " {" + str(contributionValue) + ";};")
                else:
                    tgrlList.append(relation + ";")
        if mergedActorsIDs[i] != 'X#Y':
            tgrlList.append('}') #closing the actor
    tgrlList.append('}') #closing the model
#     print(tgrlList)

    mergedModel_file_name = 'integratedModel_'+str(input_model_a_name)+'_'+str(input_model_b_name)+'.xgrl'
#    with open('mergedModel.xgrl', 'w') as filehandle:
    with open(mergedModel_file_name, 'w') as filehandle:
        for listitem in tgrlList:
            filehandle.write('%s\n' % listitem)
            
    
def getDecompositionType(elementID):
    currentElementRelations = pd.DataFrame(merged_relations_df.loc[merged_relations_df['parent_element_ID'] == elementID])
    currentElementRelations = currentElementRelations.reset_index(drop=True)
    if not currentElementRelations.empty:
        relationType = currentElementRelations.loc[currentElementRelations['relation_type'] == 'decomposition', 'decomposition_type']
        if not relationType.empty:
            relationType = (relationType.unique().tolist())[0]
            return relationType
        else:
            return ""
    else:
        return ""
    
        
def downloadMergedModel():
    DFtoTGRL()
    return redirect(request.referrer)

def downloadConflictCases():
    global trace_conflict_df
    global trace_error_df
    global input_model_a_name
    global input_model_b_name
    resolved_conflicts_errors = []
    
    resolved_conflicts_errors.append(trace_conflict_df)
    resolved_conflicts_errors.append(trace_error_df)

    sheets = ['Conflict Cases', 'Error Cases']


    conflicts_errors_fileName = 'conflict_error_cases_'+str(input_model_a_name)+"_"+str(input_model_b_name)+'.xlsx'
    
    dfs_tabs(resolved_conflicts_errors, sheets, conflicts_errors_fileName)
    
#    conflict_file_name = 'conflict_cases_'+str(input_model_a_name)+"_"+str(input_model_b_name)+'.xlsx'
#    writer = pd.ExcelWriter(conflict_file_name)
#    trace_conflict_df.columns = ['Merged Construct ID', 'Conflict Type', str(input_model_a_name)+": Construct", str(input_model_a_name)+": Construct Value", str(input_model_b_name)+": Construct", str(input_model_b_name)+": Construct Value", 'Selected Value']
#    trace_conflict_df.to_excel(writer)
#    writer.save()
