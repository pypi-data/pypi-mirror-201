#!/usr/bin/env python3

"""Module containing the BioBBs DisGeNET class and the command line interface."""
import argparse
import shutil
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_netprop.netprop.common import *


# 1. Rename class as required
class DADisgenet(BiobbObject):
    """
    | biobb_netprop Disease Attribute Disgenet
    | This class is for downloading a Disease Attribute request from DisGeNET database.
    | Wrapper for the DisGeNET database `https://www.disgenet.org` and the  DisGeNET REST API ´https://www.disgenet.org/api/´ for downloading available collections of genes and variants associated data to human diseases.

    Args:
        output_file_path (str): Path to the output file, that can be in format TSV, JSON or XML. 
        properties (dict - Python dict containing the properties for the API interrogation, considering also the credentials of the user to the database):
            * **diseaseName** (*str*) - Disease name recognized by the database.
            * **disease_id** (*str*) - Disease id or a list of disease ids separated by commas.
            * **source** (*str*) - Source of the associations (CURATED, INFERRED, ANIMAL_MODELS, ALL, BEFREE, CGI, CLINGEN, CLINVAR, CTD_human, CTD_mouse, CTD_rat, GENOMICS_ENGLAND, GWASCAT, GWASDB, HPO, LHGDN, MGD, ORPHANET, PSYGENET, RGD, UNIPROT).
            * **max_dsi** (*str*) - Max value of DSI range for the gene.
            * **min_dsi** (*str*)  - Min value of DSI range for the gene.
            * **min_dpi** (*str*) - Min value of DPI range for the gene.
            * **max_dpi** (*str*) - Max value of DPI range for the gene.
            * **max_pli** (*str*) -  Max value of pLI range for the gene.
            * **min_pli** (*str*) -  Min value of pLI range for the gene.
            * **format** (*str*) - Format output file.
            * **limit** (*str*) - Number of disease to retrieve.

    Examples:
        This is a use example of how to use the building block from Python:

            from biobb_netprop.netprop.da_disgenet import da_disgenet

            prop = {
                'disease_id':'disease_id',
                'source': 'source', 
                'min_dsi': 'min_dsi',
                'max_dsi': 'max_dsi',
                'min_dpi': 'min_dpi',
                'max_dpi': 'max_dpi',
                'min_pli': 'min_pli',
                'max_pli':'max_pli', 
                'format': 'format',
                'limit': 'limit'
            }
            da_disgenet(
                    input_file_path='path/to/inputFile',
                    output_file_path='/path/to/associationsFile',
                    properties=prop)

    Info:
            retrieve_by can be:
                disease, diseaseName, source, mappings, similarity

    """

    # 2. Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, input_file_path, output_file_path, properties = None, **kwargs) -> None:
        properties = properties or {}

        super().__init__(properties)

        # Input/Output files
        self.io_dict = { 
                'in': {'input_file_path': input_file_path}, 
                'out': { 'output_file_path': output_file_path } 
        }

        # Properties specific for BB
        bb_properties = {}

        self.email = properties.get('email', None)
        self.password = properties.get('password', None)
        
        bb_properties["retrieve_by"] = properties.get('retrieve_by', None)
        bb_properties["diseaseName"] = properties.get('diseaseName', None)
        bb_properties["disease_id"] = properties.get('disease_id', None)
        bb_properties["source"] = properties.get('source', "ALL")
        bb_properties["vocabulary"] = properties.get('vocabulary', None)
        bb_properties["type"] = properties.get('disease_type', None)
        bb_properties["disease_class"] = properties.get('disease_class', None)
        bb_properties["format"] = properties.get('format', "json")
        bb_properties["limit"] = properties.get('limit', None)
        bb_filtered = {k: v for k, v in bb_properties.items() if v is not None}
        bb_properties.clear()
        bb_properties.update(bb_filtered)
        self.properties = bb_properties

        # Check the properties

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`GDA_disgenet <disgenet.GDA_disgenet.GDA_disgenet>` object."""
        
        # Setup Biobb and Check properties
        if self.check_restart(): return 0
        self.stage_files()
        
        if self.properties.get('retrieve_by'):
            print (self.properties.get('retrieve_by'))
            response = da_session("disease", self.properties.get('retrieve_by'), self.properties, self.out_log, self.global_log)
        else:
            raise SystemExit("Fundamental argument is missing, check the input parameter.")
        print ('response:', response)
        print ('input:', self.io_dict["in"]["input_file_path"])
        new_keys, request = extension_request(response, self.properties.get('retrieve_by'), self.properties)
        print (self.properties)
        print ('request: ', request)
        auth_session(request, new_keys, 'maria.ferri@bsc.es', 'mferri2021', self.io_dict['out']['output_file_path'].split('.')[0], self.out_log, self.global_log)
        file = self.io_dict['out']['output_file_path'].split('.')[0]
        print (file)
        if os.path.isfile(file+".json"):
            #print (self.io_dict["out"]["output_csv_path"]+".json")
            convert_file(file+".json", file, ".csv", self.out_log, self.global_log)
        return 0

def da_disgenet(input_file_path: str, output_file_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`DADisgenet <disgenet.da_disgenet.DADisgenet>` class and
    execute the :meth:`launch() <disgenet.da_disgenet.DADisgenet>` method."""

    return DADisgenet(
                    input_file_path=input_file_path,
                    output_file_path=output_file_path,
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='This class is a wrapper for an associations call of teh DisGeNET database REST API.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # 10. Include specific args of each building block following the examples. They should match step 2
    required_args = parser.add_argument_group('required arguments')
    
    required_args.add_argument('-input_file_path', required=True, help='Retrieval factor necessary to define the search of the associations; gene, uniprot entry, disease, source, evidence by disease, evidence by gene available choices.')
    required_args.add_argument('-output_file_path', required=True, help='Description for the output file path. Accepted formats: json, csv or html.')

    args = parser.parse_args()
    args.config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    da_disgenet(
             input_file_path=input_file_path,
             output_file_path=output_file_path, 
             properties=properties)

if __name__ == '__main__':
    main()
