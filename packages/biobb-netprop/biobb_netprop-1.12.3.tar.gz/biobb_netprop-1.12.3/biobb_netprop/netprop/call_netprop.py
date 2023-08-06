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
class CallGuild(BiobbObject):
    """
    | biobb_netprop Call NetProp

    Args:        
        input_file_path1 (str): Hippie Database. Accepted formats: txt.
        input_file_path2 (str): Hippie Genes
        input_netprop_dir (str): Guild path
        output_file_path (str): Description for the output file path. File type: txt. Accepted formats: txt.
        properties (dic):
            * **algorithm** (*string*) - Choosing the reference algorithm for GUILD to be used, can be **s** for NetScore, or **z** for NetZScore.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_netprop.netprop.call_netprop import call_netprop

            prop = { 
                'algorithm': 's'
            }
            CallGuild(input_file_path1='/path/to/HippieDatabase',
                    output_file_path='/path/to/GuildAlgo,
                    input_file_path2='/path/to/HippieGenes',
                    properties=prop)

    """

    # Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, input_file_path1, input_file_path2, input_netprop_dir, output_path,
                properties = None, **kwargs) -> None:
        properties = properties or {}

        super().__init__(properties)

        # Input/Output files
        self.io_dict = { 
                'in': { 'input_file_path1': input_file_path1, 'input_file_path2': input_file_path2, 'input_netprop_dir': input_netprop_dir }, 
                'out': { 'output_path': output_path } 
        }

        # Include all relevant properties here as 
        self.algorithm = properties.get('algorithm','')
        self.properties = properties

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`CallGuild <disgenet.call_netprop.CallGuild>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)
        
        netprop(self.algorithm, self.io_dict['in']['input_netprop_dir'], self.io_dict['in']['input_file_path1'], self.io_dict['in']['input_file_path2'], self.io_dict['out']['output_path'], self.out_log, self.global_log)

        return 0

def call_netprop(input_file_path1: str, input_file_path2: str, input_netprop_dir: str, output_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`CallGuild <disgenet.call_netprop.CallGuild>` class and
    execute the :meth:`launch() <disgenet.call_netprop.CallGuild>` method."""

    return CallGuild(input_file_path1=input_file_path1, 
                    input_file_path2=input_file_path2,
                    input_netprop_dir=input_netprop_dir,
                    output_path=output_path,
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Description for the template module.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c','--config', required=True, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i','--input_interactome', required=True, help='Description for the first input file path.')
    required_args.add_argument('-n','--input_nodes', required=True, help='Description for the first input file path.')
    required_args.add_argument('-o','--output_path', required=True, help='Description for the output file path. Accepted formats: zip.')
    required_args.add_argument('-g','--input_netprop_dir', required=True, help='Description for the first input file path.')
    args = parser.parse_args()
    args.config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    call_netprop(input_file_path1=args.input_nodes,
             input_file_path2=args.input_interactome,
             input_netprop_dir=args.input_netprop_dir, 
             output_path=args.output_path, 
             properties=properties)

if __name__ == '__main__':
    main()

# 12. Complete documentation strings
