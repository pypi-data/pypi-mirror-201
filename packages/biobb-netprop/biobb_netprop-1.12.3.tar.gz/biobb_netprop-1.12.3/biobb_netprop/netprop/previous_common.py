#Common functions for the codes in this directory
#Function to check if the output paths exist
#Function to check if the required prop is there (different for each request)
#Function to launch the request 

#!/usr/bin/env python3

#Initial script for questioning the Disgenet API and see how it works. 
#Local instantiation
import os
import requests
import argparse
import getpass
import json
import pandas as pd
import igraph as ig
import warnings
warnings.filterwarnings("ignore")

#import xml.etree.ElementTree as ET
from pathlib import Path, PurePath
from biobb_common.tools import file_utils as fu


def check_output_path(path, option, output, ext, out_log, classname):
    #Function to check the existing output file path
    if option and not path:
        return None
    if PurePath(path).parent and not Path(PurePath(path).parent).exists():
        fu.log(classname + ': Unexisting %s folder, check the input params' % output, out_log)
        raise SystemExit(classname + ': Unexisting %s folder' % output)
    if not check_extension(ext, output):
        fu.log(classname + ': Fromat %s for %s file is not compatible' % (ext, output))
        raise SystemExit(classname + ': Format %s for %s is not compatible' % (ext, output))

    return path

def check_extension(ext, output):
    #Function to check if the format chosen by the user is allowed
    formats = {
            'json',
            'tsv', 
            'xml',
            'txt',
            'csv'
            }
    return ext in formats

#as input once, but I have also to check into the properties dict 
def check_mandatory_property(properties, name, out_log, classname):
    #check if the retrieve_by option is definied in the property, so to see if the required one is present
    """ Checks mandatory properties """
    for key in properties.keys():
        print (key)
        if name in key:
        #if the property in the keys, check if the value is not null
            fu.log(classname + ': Parameter %s required present' % name, out_log)
            continue
        else:
            fu.log(classname + ': Unexisting %s property, exiting' % name, out_log)
            raise SystemExit(classname + ': Unexisting %s property' % name)
    return True


def gda_vda_session(association_type, retrieve_by, properties, out_log = None, global_log=None):
    for key in properties.keys():
        if retrieve_by+'id' in key:
            identificator = key
            #Source case can be either gene_id or disease_id
        elif 'id' in key:
            identificator = key
    if retrieve_by:
        if retrieve_by == "disease" and properties.get("vocabulary"):
            request = os.path.join(association_type, retrieve_by, properties.get("vocabulary").strip(), properties[identificator])
        elif retrieve_by == "source" and properties.get("source"):
                #none of them is defined
            request = os.path.join(association_type, retrieve_by, properties.get("source").strip())
        elif retrieve_by == "uniprot":
            request = os.path.join(association_type+"/gene", retrieve_by, properties.get(identificator))
        elif retrieve_by == "evidences":
            #can have 3 different choices, variant, disease and gene (would be in the id property!)
            spx = identificator.split('id')[0]
            request = os.path.join(association_type, retrieve_by+"/"+spx, properties.get(identificator))
        else:
            request = os.path.join(association_type, retrieve_by, properties.get(identificator))
    else:
        raise SystemError('Error in the input parameter, check the specifics for each session requested.')
    fu.log("Request: %s" %(request), out_log)
    return request 
    
def dda_session(retrieve_by, properties, out_log = None, global_log=None):
    for key in properties.keys():
        if "id" in key:
            identificator = key
    #Retrieve methods can be two: or by the genes, or by the variants
    if retrieve_by == "genes" or retrieve_by == "variants":
        if properties.get("vocabulary"):
            request = os.path.join("dda", retrieve_by+"/disease", properties.get("vocabulary"), properties[identificator])
        else:
            request = os.path.join("dda", retrieve_by+"/disease", properties[identificator])
    else:
        return SystemError('Retrieval specifics are not allowed, check the specifics for each session requested.')
    fu.log("Request: %s" %(request), out_log)
    return request

def ga_va_session(association_type, retrieve_by, properties, out_log = None, global_log=None):
    for key in properties.keys():
        if retrieve_by+'id' in key:
            identificator = key
    if retrieve_by:
        if association_type == "gene" and retrieve_by == "uniprot":
            request = os.path.join(association_type, retrieve_by,  properties[identificator])
        elif retrieve_by == "source":
            if not properties.get("source"):
                raise SystemExit("Attributes searched by source, but missing parameter: check input.")
            else:
                request = os.path.join(association_type, retrieve_by, properties.get("source").strip())
        elif association_type == retrieve_by:
            request = os.path.join(association_type,properties[identificator])
        else:
            request = os.path.join(association_type, retrieve_by, properties[identificator])
    else:
        raise SystemError('Error in the input parameter, check the specifics for each session requested.')

    fu.log("Request: %s" %(request), out_log)
    return request 

def da_session(association_type, retrieve_by, properties, out_log = None, global_log=None):
    for key in properties.keys():
        if retrieve_by+'id' in key:
            identificator = key
        elif 'id' in key:
            identificator = key
    #Looking for disease_id
    if retrieve_by:
        if retrieve_by == "disease":
            if properties.get("vocabulary"):
                request = os.path.join(association_type, properties["vocabulary"], properties[identificator])
            else:
                request = os.path.join(association_type, properties[identificator])
            # disease/{disease}
        elif retrieve_by == "mappings":
            if properties.get("vocabulary"): #If mappings and vocabulary
                request = os.path.join(association_type, retrieve_by, properties["vocabulary"], properties[identificator])
            elif properties.get("diseaseName"):
                request = os.path.join(association_type, retrieve_by+"/name", properties["diseaseName"])
        elif retrieve_by == "similarity":
            request = os.path.join(association_type, retrieve_by, properties[identificator])
        else:
            #retrieve_by == source
            request = os.path.join(association_type, retrieve_by, properties[retrieve_by])
    else:
        raise SystemError("Disease attributes search parameter are not acceptable; please look at the documentation.")
    return request


def extension_request(request, retrieve_by, properties = None, out_log = None, global_log=None):
    #Not to include all the properties that are already present in the request
    new_keys={}
    for k in properties.keys():
        #fu.log("Prop %s" %(properties.keys()))
        if any(sub in str(k) for sub in request.split('/')): 
            continue
        elif any(str(sub) in str(properties[k]) for sub in request.split('/')):
            continue
        else:
            new_keys[k] = properties[k]
    fu.log("New Keys %s" % (new_keys), out_log) 
    ext=""
    for p, prop in enumerate(new_keys):
        fu.log("Prop %s and p %s" %(p, prop), out_log)
        if p != len(new_keys) - 1:
            #fu.log('Different key %s' % (prop), out_log)
            ext += str(prop) + "=" + str(new_keys.get(prop)) + "&"
        else:
            ext += str(prop) + "=" + str(new_keys.get(prop))         
    #fu.log("ext %s" %(ext), out_log)
    if ext == "":
        pass
    else:
        request += "?"+ext
        fu.log("Final req %s" %(request), out_log)

    return new_keys, request

def auth_session(request, properties, email, password, output_path, out_log=None, global_log=None):
#    auth_params = {"email": args.email,"password": args.password}
    #email = getpass.getpass('E-mail:')
    #password = getpass.getpass('Password:')
    #print (request, properties, email, password, output_path)
    if not email:
        raise SystemError ("Credentials not provided, please check configuration.")
    else:
        auth_params = {"email":email,"password":password}
        api_host = "https://www.disgenet.org/api"
        api_key = None 
        s = requests.Session()
        try: 
            r = s.post(api_host+"/auth/", json=auth_params)
            if(r.status_code == 200):
            #Lets store the api key in a new variable and use it again in new requests
                json_response = r.json()
                api_key = json_response.get("token")
                print("This is your user API key: {}".format(api_key)) #Comment this line if you don't want your API key to show up in the terminal
            else:
                print(r.status_code)
                print(r.text)
        except requests.exceptions.RequestException as req_ex:
            print(req_ex)
            print("Something went wrong with the request.")
    #return api_key
        if api_key:
        #Add the api key to the requests headers of the requests Session object in order to use the restricted endpoints.
            s.headers.update({"Authorization": "Bearer %s" % api_key}) 
        #Lets get all the diseases associated to a gene eg. APP (EntrezID 351) and restricted by a source.
        #request = str(api_host+'/'+association_type+'/'+retrieve_by+'/'+properties[retrieve_by])
            req = api_host +'/' +str(request)
        #fu.log("Request %s " % req, out_log)
        #fu.log("Request %s " % request, out_log)
        #fu.log ("Prop %s" % properties, out_log)
            gda_response = s.get(req, params=properties)
            fu.log("Request %s launched, compiling" % req, out_log)
        #response_txt = gda_response.text
        #response_json = gda_response.json()
            format_output = properties['format']
            #if format_output == "json":
            fu.log("Output file format: %s" % (format_output), out_log, global_log)
            response_json = gda_response.json()
            file_json = write_output_json(response_json, format_output, output_path)
            #elif format_output == "tsv":
            #    fu.log("Output file format: %s" % (format_output), out_log, global_log)
            #    response_txt = gda_response.text
            #    write_output_txt(response_txt, format_output, output_path)
            #else: 
            #    fu.log("Output file format: %s" % (format_output), out_log, global_log)
            #    response_content = gda_response.content
            #    write_output_xml(response_content, format_output, output_path)
            fu.log("File json: %s" % (file_json), out_log, global_log)
            #fu.log("Format %s" % (format_output), out_log, global_log)
        
        if s:
            s.close()

#output: response.json() for json format, response.text for tsv format, xml 
def convert_file(output_file_tc, output_file_c, format_file, out_log=None, global_log=None):
    fu.log("To convert: %s " % (output_file_tc))
    jsondata = open(output_file_tc)
    jdata = json.load(jsondata)
    df = pd.DataFrame.from_records(jdata)
    #fu.log("pd %s" %(df.T))
    #header = ["diseaseid", "variantid", "score"]
    df.to_csv(output_file_c+format_file, index=False, sep='\t', mode="a")

def write_output_json(response, format_output_file, output_path, out_log=None, global_log=None):
    #Function to write the file and download it in the format that is chosen by the user
    output_file = output_path+"."+format_output_file
    with open(output_file, "w", encoding='utf-8') as output: 
        json.dump(response, output, ensure_ascii=False, indent=4)
    
    return (output_file)
        
def write_output_txt(response, format_output_file, output_path, out_log=None, global_log=None):
    if format_output_file == "tsv":
        output_file = output_path+".csv"
    with open(output_file, "w", encoding='utf-8') as output:
        fu.log("Output file format: %s" % (format_output_file), out_log, global_log)
        output.write(response)

def write_output_xml(response, format_output_file, output_path, out_log=None, global_log=None):
    output_file = output_path+"."+format_output_file
    with open(output_file, "wb") as output:
        fu.log("Output file format: %s" % (format_output_file), out_log, global_log)
        output.write(response)



# # PARSE HIPPIE INTERACTOME

# 1. Parse the database
# 2. checks if there's some genes that are deprecated
# 3. build a network
# 4. simplifies the network by removing the duplicated elements and edges
# 5. takes the biggest cluster in the network and get rid of all non connected element in the graph

def parse_hippie(output_file, save_out=None, out_log=None, global_log=None):
    
    hippie=pd.read_csv("http://cbdm-01.zdv.uni-mainz.de/~mschaefer/hippie/HIPPIE-current.mitab.txt",sep='\t')
    #Parse the columns headers
    hippie.columns=[x.replace(" ", "_") for x in hippie.columns]
    edges=hippie[hippie.Confidence_Value>0.65]
    edges['ID_Interactor_A']=edges['ID_Interactor_A'].apply(lambda x: x.replace('entrez gene:',''))
    edges['ID_Interactor_B']=edges['ID_Interactor_B'].apply(lambda x: x.replace('entrez gene:',''))

    genes=pd.read_csv("https://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz",sep='\t')

    def convert_to_str(integer):
        return str(integer)
    genes.GeneID=genes.GeneID.apply(lambda x: convert_to_str(x))

    #keep only the genes present in the human genes database
    edges = edges[(edges.ID_Interactor_A.isin(genes.GeneID.tolist()))&(edges.ID_Interactor_B.isin(genes.GeneID.tolist()))]

    #build a list of single genes to be used as nodes
    nodes=pd.DataFrame(set(edges.ID_Interactor_A.tolist()).union(edges.ID_Interactor_B.tolist()),columns=['Nodes'])

    graph_full=ig.Graph.DataFrame(edges, directed=False, vertices=nodes)
    graph_full.ecount(),graph_full.vcount()#(104249, 13631)

    simplified_graph=ig.Graph.simplify(graph_full)
    simplified_graph.ecount(),graph_full.vcount()#(101820, 13631)

    aux=ig.Graph.clusters(simplified_graph)#list the clusters of the graph 
    largest_cluster_index=list(aux.sizes()).index(max(list(aux.sizes()))) # gives the cluster number with the largest connected component
    nodes_in_largest_cluster=aux[largest_cluster_index]# returns the genes in the LCC

    gc1=ig.Graph.induced_subgraph(simplified_graph,nodes_in_largest_cluster) # creates a subgraph with the genes in the LCC
    gc1.vcount(), gc1.ecount() # 13443  101755

    #store the edges in the dataframe and replace the node id (number of the node from (0-N) with edge name (entrez of the given gene
    ve=gc1.get_vertex_dataframe()
    ed=gc1.get_edge_dataframe()
    ed['source'].replace(ve['name'], inplace=True)
    ed['target'].replace(ve['name'], inplace=True)

    ed.insert(1,'scores',1) #insert the score column between edges for netprop
    
    if save_out:
        ed.to_csv(output_file,index=False,header=False, sep=' ')
        #save the file 

    return ed, gc1
#if __name__=='__main__':
#        parse_hippie(save_out=True)

