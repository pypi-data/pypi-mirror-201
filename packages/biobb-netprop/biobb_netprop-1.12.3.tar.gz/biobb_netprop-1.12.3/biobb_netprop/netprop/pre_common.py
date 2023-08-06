""" Common functions for package netprop """
import os
import pandas as pd
import igraph as ig
import json
import requests
import subprocess
import urllib.request
from pathlib import Path, PurePath
from biobb_common.tools import file_utils as fu


def check_output(path, argument, out_log, classname):
    """ Checks output file """
    if PurePath(path).parent and not Path(PurePath(path).parent).exists():
        fu.log(classname + ': Unexisting %s folder, exiting' % argument, out_log)
        raise SystemExit(classname + ': Unexisting %s folder' % argument)
    file_extension = PurePath(path).suffix
    if not is_valid_file(file_extension[1:], argument):
        fu.log(classname + ': Format %s in %s file is not compatible' % (file_extension[1:], argument), out_log)
        raise SystemExit(classname + ': Format %s in %s file is not compatible' % (file_extension[1:], argument))
    return path

def check_mandatory_property(properties, name, out_log, classname):
    #check if the retrieve_by option is definied in the property, so to see if the required one is present
    """ Checks mandatory properties """
    for key in properties.keys():
        print (key)
        print ('name:', name)
        if str(name) in key:
        #if the property in the keys, check if the value is not null
            fu.log(classname + ': Parameter %s required present' % name, out_log)
            continue
        else:
            fu.log(classname + ': Unexisting %s property, exiting' % name, out_log)
            raise SystemExit(classname + ': Unexisting %s property' % name)
    return True


def is_valid_dir(output_path, out_log, global_log):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

def is_valid_file(ext, argument):
    formats = {
            'output_sif': ['sif'],
            'output_csv': ['csv']
            }
    return ext in formats[argument]

def gda_session(association_type, retrieve_by, properties, out_log = None, global_log=None):
    for key in properties.keys():
        if retrieve_by+'_id' in key:
            identificator = key
            #Source case can be either gene_id or disease_id
        elif 'id' in key:
            identificator = key
    print ('idnetificator:', identificator)
    if retrieve_by:
        if retrieve_by == "disease" and properties.get("vocabulary"):
            request = os.path.join(association_type, retrieve_by, properties.get("vocabulary").strip(), properties[identificator])
        elif retrieve_by == "source" and properties.get("source"):
                #none of them is defined
            request = os.path.join(association_type, retrieve_by, properties.get("source").strip())
        elif retrieve_by == "uniprot":
            request = os.path.join(association_type+"/gene", retrieve_by, properties[identificator])
        elif retrieve_by == "evidences":
            #can have 3 different choices, variant, disease and gene (would be in the id property!)
            spx = identificator.split('id')[0]
            request = os.path.join(association_type, retrieve_by+"/"+spx, properties[identificator])
        else:
            request = os.path.join(association_type, retrieve_by, properties.get(identificator))
    else:
        raise SystemError('Error in the input parameter, check the specifics for each session requested.')
    fu.log("Request: %s" %(request), out_log)
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
            #format_output = properties['format']
            #if format_output == "json":
            fu.log("Output file format: json", out_log, global_log)
            response_json = gda_response.json()
            file_json = write_output_json(response_json, 'json', output_path)
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

def parse_hippie(hippie_db, hippie_genes, hippie_score, output_sif, out_log, global_log):
    """ Creates pd dataframe from Hippie Network and Hippie Genes """
    hippie = pd.read_csv(hippie_db, sep='\t',low_memory=False)
    hippie.columns=[x.replace(" ", "_") for x in hippie.columns]
    edges=hippie[hippie.Confidence_Value >= hippie_score ] 
    edges['ID_Interactor_A']=edges['ID_Interactor_A'].apply(lambda x: x.replace('entrez gene:',''))
    edges['ID_Interactor_B']=edges['ID_Interactor_B'].apply(lambda x: x.replace('entrez gene:',''))
    genes=pd.read_csv(hippie_genes,sep='\t')
    genes.GeneID=genes.GeneID.apply(lambda x: convert_to_str(x))
    #keep only the genes present in the human genes database
    edges = edges[(edges.ID_Interactor_A.isin(genes.GeneID.tolist()))&(edges.ID_Interactor_B.isin(genes.GeneID.tolist()))]
    #build a list of single genes to be used as nodes
    nodes=pd.DataFrame(set(edges.ID_Interactor_A.tolist()).union(edges.ID_Interactor_B.tolist()),columns=['Nodes'])
    graph_full=ig.Graph.DataFrame(edges, directed=False, vertices=nodes)
#    graph_full.ecount(),graph_full.vcount()#(104249, 13631)
    simplified_graph=ig.Graph.simplify(graph_full)
#    simplified_graph.ecount(),graph_full.vcount()#(101820, 13631)
    aux=ig.Graph.clusters(simplified_graph)#list the clusters of the graph 
    largest_cluster_index=list(aux.sizes()).index(max(list(aux.sizes()))) # gives the cluster number with the largest connected component
    nodes_in_largest_cluster=aux[largest_cluster_index]# returns the genes in the LCC
    gc1=ig.Graph.induced_subgraph(simplified_graph,nodes_in_largest_cluster) # creates a subgraph with the genes in the LCC
#    gc1.vcount(), gc1.ecount() # 13443  101755

    #store the edges in the dataframe and replace the node id (number of the node from (0-N) with edge name (entrez of the given gene
    ve=gc1.get_vertex_dataframe()
    ed=gc1.get_edge_dataframe()
    ed['source'].replace(ve['name'], inplace=True)
    ed['target'].replace(ve['name'], inplace=True)

    ed.insert(1,'scores',1) #insert the score column between edges for netprop
    ed.to_csv(output_sif,index=False,header=False, sep=' ')#save the file 

def convert_to_str(integer):
    return str(integer)

def maknodes(interactome_sif, gda_result, disease_id, gda_score, scoring_mode, output_nodes, out_log, global_log, curated=False):
    ppi_network_edges = pd.read_csv(interactome_sif, sep=' ')
    ppi_network_edges.columns=['source','score','target']
    GdaDataset = pd.read_csv(gda_result, sep='\t')
    GeneColumn='geneid'
    ScoreColumn='gene_dsi'
    DisColumn='diseaseid'

#    if curated=='True':
#        GdaDataset=pd.read_csv("./biobb_netprop/disc4all-data-fra/datasets/curated_gda.tsv",sep='\t')
#        GeneColumn='Gene_id'
#        ScoreColumn='Score_gda'
#        DisColumn='Disease_id'
#    else:
#        GdaDataset=pd.read_csv("./biobb_netprop/disc4all-data-fra/datasets/all_gda.tsv",sep='\t')
#        GeneColumn='geneId'
#        ScoreColumn='score'
#        DisColumn='diseaseId'
    #GdaDataset=GdaDataset[(GdaDataset[ScoreColumn]>=gda_score)&(GdaDataset[DisColumn]==disease_id)] 
    seeds=GdaDataset[[GeneColumn, ScoreColumn]]
    seeds=seeds[(seeds[GeneColumn].isin(ppi_network_edges.source) | (seeds[GeneColumn].isin(ppi_network_edges.target)))]
    nodes=pd.DataFrame(set(ppi_network_edges.source.tolist() + ppi_network_edges.target.tolist()),columns=[GeneColumn])
    nodes_wo_seeds=pd.DataFrame([node for node in nodes[GeneColumn].tolist() if node not in seeds[GeneColumn].tolist()],columns=[GeneColumn])
    nodes_wo_seeds[ScoreColumn]=0
    if scoring_mode=='dis':
        nodes=pd.concat([seeds,nodes_wo_seeds])
        nodes.to_csv(output_nodes, sep=' ', index=False, header=False)
    elif scoring_mode=='norm_dis':
        nodes=pd.concat([seeds,nodes_wo_seeds])
        ScoreMax=nodes[ScoreColumn].max()
        ScoreMin=nodes[ScoreColumn].min()
        nodes[ScoreColumn]=nodes[ScoreColumn].apply(lambda x: (x-ScoreMin)/(ScoreMax-ScoreMin))
        nodes.to_csv(output_nodes, sep=' ', index=False, header=False)
    elif scoring_mode == 'binary':
        nodes=pd.concat([seeds,nodes_wo_seeds])
        nodes[ScoreColumn]=[1 if score > 0 else 0 for score in nodes[ScoreColumn].tolist()]
        nodes.to_csv(output_nodes, sep=' ', index=False, header=False)

def maknodes1(interactome_sif, gda_result, disease_id, gda_score, scoring_mode, dataset_path, output_nodes, out_log, global_log, curated=False):
    print ('Path:', os.getcwd())
    ppi_network_edges = pd.read_csv(interactome_sif, sep=' ')
    ppi_network_edges.columns=['source','score','target']
    if os.path.exists(dataset_path):
        if curated=='True':
            print ('PATH', os.path.join(dataset_path,"curated_gda.tsv"))
            GdaDataset=pd.read_csv(os.path.join(dataset_path,"curated_gda.tsv"),sep='\t')
            GeneColumn='Gene_id'
            ScoreColumn='Score_gda'
            DisColumn='Disease_id'
        else:
            print ('PATH', os.path.join(dataset_path,"all_gda.tsv"))
            GdaDataset=pd.read_csv(os.path.join(dataset_path,"all_gda.tsv"),sep='\t')
            GeneColumn='geneId'
            ScoreColumn='score'
            DisColumn='diseaseId'
        GdaDataset=GdaDataset[(GdaDataset[ScoreColumn]>=gda_score)&(GdaDataset[DisColumn]==disease_id)]
    else:
        raise ValueError('Dataset path not correct, {} not redirecting to GDA dataset.'.format(dataset_path))
    seeds=GdaDataset[[GeneColumn, ScoreColumn]]
    seeds=seeds[(seeds[GeneColumn].isin(ppi_network_edges.source) | (seeds[GeneColumn].isin(ppi_network_edges.target)))]
    nodes=pd.DataFrame(set(ppi_network_edges.source.tolist() + ppi_network_edges.target.tolist()),columns=[GeneColumn])
    nodes_wo_seeds=pd.DataFrame([node for node in nodes[GeneColumn].tolist() if node not in seeds[GeneColumn].tolist()],columns=[GeneColumn])
    nodes_wo_seeds[ScoreColumn]=0
    if scoring_mode=='dis':
        nodes=pd.concat([seeds,nodes_wo_seeds])
        nodes.to_csv(output_nodes, sep=' ', index=False, header=False)
    elif scoring_mode=='norm_dis':
        nodes=pd.concat([seeds,nodes_wo_seeds])
        ScoreMax=nodes[ScoreColumn].max()
        ScoreMin=nodes[ScoreColumn].min()
        nodes[ScoreColumn]=nodes[ScoreColumn].apply(lambda x: (x-ScoreMin)/(ScoreMax-ScoreMin))
        nodes.to_csv(output_nodes, sep=' ', index=False, header=False)
    elif scoring_mode == 'binary':
        nodes=pd.concat([seeds,nodes_wo_seeds])
        nodes[ScoreColumn]=[1 if score > 0 else 0 for score in nodes[ScoreColumn].tolist()]
        nodes.to_csv(output_nodes, sep=' ', index=False, header=False)



def run_netscore(netprop_ex, nodes, interactome, output_path, r=3, i=2):
    print ('bash -c " %s/./netprop_x64 -s s -n %s -e %s -o %s -r %s -i %s"' % (netprop_ex, nodes, interactome, output_path,r,i))
    subprocess.run('bash -c " %s/./netprop_x64 -s s -n %s -e %s -o %s -r %s -i %s"' % (netprop_ex, nodes, interactome, output_path,r,i),shell=True)
#source actovate netpropmaster &&
def create_randomized_networks(netprop_ex, interactome, output_path, n=100):
    subprocess.call('bash -c "python %s %s %s"' %(netprop_ex,interactome,n),
                   shell=True)
    subprocess.run('mv %s.* %s'%(interactome, output_path),shell=True)
def run_netzcore(netprop_ex, nodes, interactome, rand_interactomes, output_path,i=5):
    subprocess.run('bash -c "%s/./netprop_x64 -s z -n %s -e %s -o %s -i %s -d %s -x 100"' % (netprop_ex, nodes, interactome, output_path,i,rand_interactomes),shell=True)

def netprop(algorithm, path_netprop, nodes, interactome, output_path, out_log, global_log):
    if algorithm == "s":
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            run_netscore(path_netprop, nodes, interactome, output_path+"/output_netScore")
    elif algorithm == "z":
        rand_net = path_netprop+"/RandomizedNetworks/"
        if not os.path.exists(rand_net):
            os.makedirs(rand_net)
        if len(os.listdir(rand_net))==0:
            rand_interactomes = create_randomize_networks(path_netprop+"/src/create_random_networks_for_netzcore.py", interactome)
        run_netzcore(path_netprop, nodes, interactome, rand_interactomes, output_path)

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

