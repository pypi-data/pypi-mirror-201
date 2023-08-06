#!/usr/bin/env python3

"""Module containing the Template class and the command line interface."""
import argparse
import pandas as pd
import numpy as np
import os
import shutil
from pathlib import PurePath
from biobb_netprop.netprop.common import *
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


# 1. Rename class as required
class MakNodes(BiobbObject):
    """
    | biobb_netprop Making Nodes

    Args:        
        input_file_path1 (str): Interactome file, coming out of previous step. Accepted formats: sif.
        input_file_path2 (str): GDA retrieved from DisGenet.
        input_dataset_path (str): Database of PPI taken as a reference for nodes positioning.Accepted formats: txt.
        output_file_path (str): Text file containing the nodes to give as input to the PPI Network algorithm. File type: txt. 
        properties (dic):
            * **curated** (*bool*) - (True) Choosing the curated or not database version
            * **disease_id** (*str*) - ("sample") Disease ID used in DisGenet retrieval.
            * **disgenet_score** (*str*) - (0.0) Score that was used in the DiGenet retrieval.
            * **scoring_mode** (*str*) - ("sample") Defining the Scoring system to be used to rate the PPI Network.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_netprop.netprop.MakNodes import maknodes

            prop = { 
                'boolean_property': True,
                'disease_id': CA0002,
                'disgenet_score': 0.2,
                'scoring_mode': 's'
            }
            nodes(input_file_path1='/path/to/myInteractome.sif',
                    input_file_path2='/path/to/myDisGenetresults',
                    input_database_path='/path/to/Database',
                    output_file_path='/path/to/nodesFile.txt'
                    properties=prop)

    Info:
        * wrapped_software:
            * name: networkx
            * version: >=3.0
            * license: BSD 3-Clause
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    # 2. Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, input_file_path1, input_file_path2, input_file_dataset, output_sif_path, properties = None, **kwargs) -> None:
        properties = properties or {}
        super().__init__(properties)

        # Input/Output files
        self.io_dict = { 
            'in': { 'input_file_path1': input_file_path1 , 'input_file_path2': input_file_path2, 'input_file_dataset': input_file_dataset}, 
            'out': { 'output_sif_path': output_sif_path } 
        }


        # Properties specific for BB
        self.curated = properties.get('curated', False)
        self.disease = properties.get('disease', '')
        self.disgenet_score = properties.get('disgenet_score', 0.0)
        self.scoring_mode = properties.get('scoring_mode', 'dis')
        self.properties = properties

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Template <template.template.Template>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        check_output(self.io_dict['out']['output_sif_path'], "output_sif", self.out_log,self.__class__.__name__)
        maknodes1(self.io_dict['in']['input_file_path1'], self.io_dict['in']['input_file_path2'], self.disease, self.disgenet_score, self.scoring_mode, self.io_dict['in']['input_file_dataset'], self.io_dict['out']['output_sif_path'], self.out_log, self.global_log, curated=self.curated) 

        return 0

def maknodes(input_file_path1: str, input_file_path2: str, input_file_dataset: str, output_sif_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`MakNodes <disgenet.maknodes.MakNodes>` class and
    execute the :meth:`launch() <disgenet.maknodes.MakNodes>.launch>` method."""

    return MakNodes(input_file_path1=input_file_path1,
                input_file_path2=input_file_path2,
                input_file_dataset=input_file_dataset,
                output_sif_path=output_sif_path,
                properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Description for the template module.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c','--config', required=True, help='Configuration file')

    # 10. Include specific args of each building block following the examples. They should match step 2
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i','--input_interactome', required=True, help='Description for the first input file path.')
    required_args.add_argument('-g','--input_gda', required=True, help='Description for the first input file path.')
    required_args.add_argument('-d','--dataset_path', required=True, help='Description for the dataset input file path.')
    required_args.add_argument('-o','--output_sif_path', required=True, help='Description for the output file path. Accepted formats: zip.')

    args = parser.parse_args()
    args.config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    maknodes(input_file_path1=args.input_interactome,
             input_file_path2=args.input_gda,
             input_file_dataset=args.dataset_path,
             output_sif_path=args.output_sif_path, 
             properties=properties)

if __name__ == '__main__':
    main()
