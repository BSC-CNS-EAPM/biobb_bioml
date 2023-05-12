#!/usr/bin/env python3

"""Module containing the Feature selection class and the command line interface."""
import os
import shutil
import argparse
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger



class Generate_mode(BiobbObject):
    """
    | biobb_bioml Generate model
    | Wrapper class for the `bioml Generate model <>`_ module.
    | Generate the models from the ensemble.
    
    Args:
        input_excel (str): The file to where the selected features are saved in excel format.
        output_model (str): The directory for the generated model. Default: "models".
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **hyperparameter_path** (*str*) - ("training_features/hyperparameters.xlsx") Path to the hyperparameter file.
            * **num_thread** (*int*) - (10) The number of threads to use for the parallelization of outlier detection.
            * **scaler** (*str*) - ("robust") "Choose one of the scaler available in scikit-learn, defaults to RobustScaler. Option: ("robust", "standard", "minmax").
            * **label** (*str*) - (None) The path to the labels of the training set in a csv format.
            * **sheets** (*str*) - (None) Names or index of the selected sheets for both features and hyperparameters and the index of the models in this format-> sheet (name, index):index model1,index model2 "
                            without the spaces. If only index or name of the sheets, it is assumed that all kfold models
                            are selected. It is possible to have one sheet with kfold indices but in another ones
                            without
            * **outliers** (*str*) - (None) A list of outliers if any, the name should be the same as in the excel file with the filtered features, you can also specify the path to a file in plain text format, each record should be in a new line

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.ensemble import ensemble
            prop = { hyperparameter_path: 'training_features/hyperparameters.xlsx', 
                    num_thread: 10, 
                    scaler: 'robust'}
                    
            generate_mode(input_excel='training_features/selected_features.xlsx',
                            output_model = 'models',
                            properties=prop)

    Info:
        * wrapped_software:
            * name: BioMl generate model
            * version: >0.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """
    def __init__(self, input_excel: str, output_model: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_excel": input_excel},
            "out": {"output_model": output_model}
        }

        # Properties specific for BB
        self.hyperparameter_path = properties.get('hyperparameter_path', 'training_features/hyperparameters.xlsx')
        self.num_thread = properties.get('num_thread', 10)
        self.scaler = properties.get('scaler', 'robust')
        self.label = properties.get('label', None)
        self.sheets = properties.get('sheets', None)
        self.outliers = properties.get('outliers', None)


        # Properties common in all BB

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`generate_mode <bioml.generate_mode.generate_mode>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()


        if self.container_path:
            shutil.copytree("", Path(self.stage_io_dict.get("unique_dir")).joinpath(Path("").name))
            file1 = str(Path(self.container_volume_path).joinpath(Path(file1).name, Path(file1).name))

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m generate_mode',
                    '--features', self.stage_io_dict["in"]["input_features"]]
        
        if self.hyperparameter_path:
            self.cmd.append('--hyperparameters')
            self.cmd.append(self.hyperparameter_path)
        if self.num_thread:
            self.cmd.append('--num_thread')
            self.cmd.append(self.num_thread)
        if self.scaler:
            self.cmd.append('--scaler')
            self.cmd.append(self.scaler)
        if self.label:
            self.cmd.append('--label')
            self.cmd.append(self.label)
        if self.sheets:
            self.cmd.append('--sheets')
            self.cmd.append(self.sheets)
        if self.outliers:
            self.cmd.append('--outliers')
            self.cmd.append(self.outliers)

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        if self.container_path:
            file1 = str(Path(self.stage_io_dict.get("unique_dir")).joinpath(Path(file1).name, Path(file1).name))

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), ""])
        self.remove_tmp_files()

        return self.return_code


def generate_mode(input_excel: str, output_model: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`generate_mode <bioml.generate_mode.Generate_mode>` class and
        execute the :meth:`launch() <bioml.generate_mode.generate_mode.launch>` method."""
    return Generate_mode(input_excel=input_excel, output_model=output_model, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl generate_mode module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_excel', required=True)
    required_args.add_argument('--output_model', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    generate_mode(input_excel=args.input_excel, output_model=args.output_model, properties=properties)


if __name__ == '__main__':
    main()