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
class VADisgenet(BiobbObject):
    """
    | biobb_netprop Variant Attribute Disgenet
    | This class is for downloading a Variant Attribute request from DisGeNET database.
    | Wrapper for the DisGeNET database `https://www.disgenet.org` and the  DisGeNET REST API ´https://www.disgenet.org/api/´ for downloading available collections of genes and variants associated data to human diseases.

    Args:

        output_file_path (str): Path to the output file, that can be in format TSV, JSON or XML. 
        properties (dict - Python dict containing the properties for the API interrogation, considering also the credentials of the user to the database):
            
            * **gene_id** (*str*) - Number identification for a gene or a list of genes separated by commas recognized by the database.
            * **variant_id** (*str*) - Uniprot id or a list of variant ids separated by commas.
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

            from biobb_netprop.netprop.ga_disgenet import ga_disgenet

            prop = { 
                'variant_id': 'variant_id',
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
            va_disgenet(
                    input_file_path='path/to/inputFile',
                    output_file_path='/path/to/associationsFile',
                    properties=prop)

    Info:

    """

    # Adapt input and output file paths as required. Include all files, even optional ones
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
        bb_properties["gene_id"] = properties.get('gene_id', None)
        bb_properties["variant_id"] = properties.get('variant_id', None)
        bb_properties["source"] = properties.get('source', "ALL")
        bb_properties["min_dsi"] = properties.get('min_dsi', None)
        bb_properties["max_dsi"] = properties.get('max_dsi', None)
        bb_properties["max_dpi"] = properties.get('max_dpi', None)
        bb_properties["min_dpi"] = properties.get('min_dpi', None)
        bb_properties["max_pli"] = properties.get('max_pli', None)
        bb_properties["min_pli"] = properties.get('min_pli', None)
        bb_properties["format"] = properties.get('format', "json")
        bb_properties["limit"] = properties.get('limit', None)
        bb_filtered = {k: v for k, v in bb_properties.items() if v is not None}
        bb_properties.clear()
        bb_properties.update(bb_filtered)
        self.properties = bb_properties

        # Check the properties

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`VADisgenet <disgenet.va_disgenet.VADisgenet>` object."""
        
        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()
        
        #check mandatory params that is gene_id
        if self.properties.get('retrieve_by'):
            print (self.properties.get('retrieve_by'))
            response = ga_va_session("variant", self.properties.get('retrieve_by'), self.properties, self.out_log, self.global_log)
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


def va_disgenet(input_file_path: str, output_file_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`VADisgenet <disgenet.va_disgenet.VADisgenet>` class and
    execute the :meth:`launch() <disgenet.va_disgenet.VADisgenet>` method."""

    return VADisgenet(
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
    va_disgenet(
             input_file_path=input_file_path,
             output_file_path=output_file_path,
             properties=properties)

if __name__ == '__main__':
    main()
