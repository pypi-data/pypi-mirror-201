#!/usr/bin/env python3

"""Module containing the Template class and the command line interface."""
import argparse
import pandas as pd
import numpy as np
import igraph as ig
import os
import shutil
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


# 1. Rename class as required
class Template(BiobbObject):
    """
    | biobb_template Template
    | Short description for the `template <http://templatedocumentation.org>`_ module in Restructured Text (reST) syntax. Mandatory.
    | Long description for the `template <http://templatedocumentation.org>`_ module in Restructured Text (reST) syntax. Optional.

    Args:        
        input_file_path1 (str): Description for the first input file path. File type: input. `Sample file <https://urlto.sample>`_. Accepted formats: top (edam:format_3881).
        input_file_path2 (str) (Optional): Description for the second input file path (optional). File type: input. `Sample file <https://urlto.sample>`_. Accepted formats: dcd (edam:format_3878).
        output_file_path (str): Description for the output file path. File type: output. `Sample file <https://urlto.sample>`_. Accepted formats: zip (edam:format_3987).
        properties (dic):
            * **boolean_property** (*bool*) - (True) Example of boolean property.
            * **executable_binary_property** (*str*) - ("zip") Example of executable binary property.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_template.template.template import template

            prop = { 
                'boolean_property': True 
            }
            template(input_file_path1='/path/to/myTopology.top',
                    output_file_path='/path/to/newCompressedFile.zip',
                    input_file_path2='/path/to/mytrajectory.dcd',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: Zip
            * version: >=3.0
            * license: BSD 3-Clause
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    # 2. Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, input_file_path1, output_file_path, 
                input_file_path2, input_file_path3,  properties = None, **kwargs) -> None:
        properties = properties or {}

        # 2.0 Call parent class constructor
        super().__init__(properties)

        # 2.1 Modify to match constructor parameters
        # Input/Output files
        self.io_dict = { 
            'in': { 'input_file_path1': input_file_path1, 'input_file_path2': input_file_path2, 'input_file_path3': input_file_path3 }, 
            'out': { 'output_file_path': output_file_path } 
        }

        # 3. Include all relevant properties here as 
        # self.property_name = properties.get('property_name', property_default_value)

        # Properties specific for BB
        self.curated = properties.get('curated', False)
        self.algorithm = properties.get('algorithm', 's')
        self.disease = properties.get('disease', '')
        self.hippie_score = properties.get('hippie_score', 0.0)
        self.disgenet_score = properties.get('disgenet_score', 0.0)
        self.scoring_mode = properties.get('scoring_mode', 'dis')
        self.properties = properties

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Template <template.template.Template>` object."""

        # 4. Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # 5. Include here all mandatory input files
        # Copy input_file_path1 to temporary folder
        shutil.copy(self.io_dict['in']['input_file_path1'], self.tmp_folder)
#        shutil.copy(self.io_dict['in']['input_file_path2'], self.tmp_folder)
#        shutil.copy(self.io_dict['in']['input_file_path3'], self.tmp_folder)

        # 6. Prepare the command line parameters as instructions list
        instructions = ['-j']
        if self.algorithm:
            instructions.append('-a')
            fu.log('Appending mandatory algorithm prop', self.out_log, self.global_log)
        elif self.disease:
            instructions.append('-d')
            fu.log('Appending mandatory disease code', self.out_log, self.global_log)
        elif self.hippie_score:
            instruction.append('-hs')
            fu.log('Appending optional Hippie Score', self.out_log, self.global_log)
        elif self.hippie_score:
            instruction.append('-ds')
            fu.log('Appending optional Disgenet Score', self.out_log, self.global_log)
        elif self.hippie_score:
            instruction.append('-m')
            fu.log('Appending optional scoring mode', self.out_log, self.global_log)
        elif self.hippie_score:
            instruction.append('-c')
            fu.log('Appending optional curated opt', self.out_log, self.global_log)

        # 7. Build the actual command line as a list of items (elements order will be maintained)
        self.cmd = [self.executable_binary_property,
               ' '.join(instructions), 
               self.io_dict['out']['output_file_path'],
               str(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict['in']['input_file_path1']).name))]
        fu.log('Creating command line with instructions and required arguments', self.out_log, self.global_log)

        # 8. Repeat for optional input files if provided
        if self.io_dict['in']['input_file_path2']:
            # Copy input_file_path2 to temporary folder
            shutil.copy(self.io_dict['in']['input_file_path2'], self.tmp_folder)
            # Append optional input_file_path2 to cmd
            self.cmd.append(str(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict['in']['input_file_path2']).name)))
            fu.log('Appending optional argument to command line', self.out_log, self.global_log)
        elif self.io_dict['in']['input_file_path3']:
            # Copy input_file_path2 to temporary folder
            shutil.copy(self.io_dict['in']['input_file_path3'], self.tmp_folder)
            # Append optional input_file_path2 to cmd
            self.cmd.append(str(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict['in']['input_file_path3']).name)))
            fu.log('Appending optional argument to command line', self.out_log, self.global_log)

        # 9. Uncomment to check the command line 
        print(' '.join(cmd))

        # Run Biobb block
        self.run_biobb()

        # Remove temporary file(s)
        if self.remove_tmp: 
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return self.return_code

def template(input_file_path1: str, output_file_path: str, input_file_path2: str, input_file_path3: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`Template <template.template.Template>` class and
    execute the :meth:`launch() <template.template.Template.launch>` method."""

    return Template(input_file_path1=input_file_path1, 
                    output_file_path=output_file_path,
                    input_file_path2=input_file_path2,
                    input_file_path3=input_file_path3,
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Description for the template module.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # 10. Include specific args of each building block following the examples. They should match step 2
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_file_path1', required=True, help='Description for the first input file path.')
    parser.add_argument('--input_file_path2', required=False, help='Description for the second input file path.')
    parser.add_argument('--input_file_path3', required=False, help='Description for the second input file path.')
    required_args.add_argument('--output_file_path', required=True, help='Description for the output file path. Accepted formats: zip.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # 11. Adapt to match Class constructor (step 2)
    # Specific call of each building block
    template(input_file_path1=args.input_file_path1, 
             output_file_path=args.output_file_path, 
             input_file_path2=args.input_file_path2,
             input_file_path3=args.input_file_path3,
             properties=properties)

if __name__ == '__main__':
    main()

# 12. Complete documentation strings
