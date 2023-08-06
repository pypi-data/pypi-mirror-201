#!/usr/bin/env python3

"""Module containing the Template class and the command line interface."""
import argparse
import pandas as pd
import numpy as np
#import igraph as ig
import os
import shutil
from pathlib import PurePath
from biobb_netprop.netprop.common import *
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


# 1. Rename class as required
class ParseHippie(BiobbObject):
    """
    | biobb_template Parse Hippie

    Args:        
        input_file_path1 (str): Hippie Database. Accepted formats: txt.
        input_file_path2 (str): Hippie Genes
        output_file_path (str): Description for the output file path. File type: output. `Sample file <https://urlto.sample>`_. Accepted formats: zip (edam:format_3987).
        properties (dic):
            * **input_file_path1** (*string*): Path for the HIPPIE database downloaded locally.
            * **input_file_path2** (*string*): Path for the HIPPIE genes to be parsed in the HIPPIE PPi database.
            * **output_sif_path** (*string*): Path for the resulting panda dataframe from the HIPPIE PPi parsing. File type: csv, json, tsv, xml. [sample file](https://urlto.sample). Accepted formats: sif.
    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_netprop.netprop.parsehippie import parsehippie

            prop = { 
                'boolean_property': True 
            }
            template(input_file_path1='/path/to/hippieDatabase.txt',
                    input_file_path2='/path/to/hippieGenes.txt',
                    output_sif_path2='/path/to/myinteractome.sif',
                    properties=prop)


    """

    # 2. Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, input_file_path1, input_file_path2, output_sif_path, properties = None, **kwargs) -> None:
        properties = properties or {}

        super().__init__(properties)

        # Input/Output files
        self.io_dict = { 
                'in': { 'input_file_path1': input_file_path1, 'input_file_path2': input_file_path2 }, 
                'out': { 'output_sif_path': output_sif_path } 
        }

        # Properties specific for BB
        self.hippie_score = properties.get('hippie_score', 0.0)
        self.disgenet_score = properties.get('disgenet_score', 0.0)
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
        parse_hippie(self.io_dict['in']['input_file_path1'], self.io_dict['in']['input_file_path2'], self.hippie_score, self.io_dict['out']['output_sif_path'], self.out_log, self.global_log) 

        return 0

def parsehippie(input_file_path1: str, output_sif_path: str, input_file_path2: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`Template <template.template.Template>` class and
    execute the :meth:`launch() <template.template.Template.launch>` method."""

    return ParseHippie(input_file_path1=input_file_path1, 
                    output_sif_path=output_sif_path,
                    input_file_path2=input_file_path2,
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Description for the template module.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c','--config', required=True, help='Configuration file')

    # 10. Include specific args of each building block following the examples. They should match step 2
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i','--input_db', required=True, help='Description for the first input file path.')
    parser.add_argument('-g','--input_genes', required=True, help='Description for the second input file path.')
    required_args.add_argument('-o','--output_sif_path', required=True, help='Description for the output file path. Accepted formats: zip.')

    args = parser.parse_args()
    args.config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    parsehippie(input_file_path1=args.input_db, 
             output_sif_path=args.output_sif_path, 
             input_file_path2=args.input_genes,
             properties=properties)

if __name__ == '__main__':
    main()
