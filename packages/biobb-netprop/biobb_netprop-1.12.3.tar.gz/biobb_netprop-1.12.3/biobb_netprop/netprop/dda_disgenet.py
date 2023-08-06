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


#  Rename class as required
class DDADisgenet(BiobbObject):
    """
    | biobb_netprop Disease Association Disgenet
    | This class is for downloading a Disease Disease Associations file from DisGeNET database.
    | Wrapper for the DisGeNET database `https://www.disgenet.org` and the  DisGeNET REST API ´https://www.disgenet.org/api/´ for downloading available collections of genes and variants associated data to human diseases.

    Args:
        output_file_path (str): Path to the output file, that can be in format TSV, JSON or XML. 
        properties (dict - Python dict containing the properties for the API interrogation, considering also the credentials of the user to the database):
            * **source** (*str*) - Source of the associations (CURATED, INFERRED, ANIMAL_MODELS, ALL, BEFREE, CGI, CLINGEN, CLINVAR, CTD_human, CTD_mouse, CTD_rat, GENOMICS_ENGLAND, GWASCAT, GWASDB, HPO, LHGDN, MGD, ORPHANET, PSYGENET, RGD, UNIPROT).
            * **disease_vocabulary** (*str*) - Disease vocabulary (icd9cm, icd10, mesh, omim, do, efo, nci, hpo, mondo, ordo).
            * **pvalue** (*str*) -  Pvalue of the disease-disease score range.
            * **format** (*str*) - Format output file.
            * **limit** (*str*) - Number of disease to retrieve.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python:

            from biobb_netprop.netprop.dda_disgenet import dda_disgenet

            prop = { 
                'disease_id': 'C0002395',
                'source': 'source', 
                'pvalue':'pvalue',
                'vocabulary':'vocabulary',
                'format': 'format',
                'limit': 'limit'
            }
            dda_disgenet(
                    input_file_path='/path/to/inputFile'
                    output_file_path='/path/to/associationsFile',
                    properties=prop)

    Info:

        retrieve_by can be equal to:
                genes, variants

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

        # 3. Include all relevant properties here as 
        # self.property_name = properties.get('property_name', property_default_value)

        # Properties specific for BB
        bb_properties = {}

        self.email = properties.get('email', None)
        self.password = properties.get('password', None)

        bb_properties["retrieve_by"] = properties.get('retrieve_by', None)
        bb_properties["disease_id"]=properties.get('disease_id', None)
        bb_properties["source"] = properties.get('source', "ALL")
        bb_properties["pvalue"] = properties.get('pvalue', None)
        bb_properties["format"] = properties.get('format', "json")
        bb_properties["limit"] = properties.get('limit', None)
        bb_filtered = {k: v for k, v in bb_properties.items() if v is not None}
        bb_properties.clear()
        bb_properties.update(bb_filtered)
        self.properties = bb_properties

        # Check the properties

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`DDADisgenet <disgenet.dda_disgenet.DDADisgenet>` object."""
        
        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()
        
        #check mandatory params that is gene_id
        print (self.properties)
        #check_mandatory_property(self.properties, "retrieve_by", self.out_log, self.__class__.__name__)
        if self.properties.get('retrieve_by') and self.properties.get('limit'):
            print (self.properties.get('retrieve_by'))
            response = dda_session(self.properties.get('retrieve_by'), self.properties, self.out_log, self.global_log)
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
        #if os.path.isfile(file+".json"):
            #print (self.io_dict["out"]["output_csv_path"]+".json")
        #    convert_file(file+".json", file, ".csv", self.out_log, self.global_log)
        return 0         

def dda_disgenet(input_file_path: str, output_file_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`DDADisgenet <disgenet.dda_disgenet.DDADisgenet>` class and
    execute the :meth:`launch() <disgenet.dda_disgenet.DDADisgenet.launch>` method."""

    return DDADisgenet(
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
    dda_disgenet(
             input_file_path=input_file_path,
             output_file_path=output_file_path,
             properties=properties)

if __name__ == '__main__':
    main()
