#!/usr/bin/env python3

"""Module containing the Generate model class and the command line interface."""
import os
import shutil
import argparse
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class Generate_model(BiobbObject):
    """
    | biobb_bioml Generate model
    | Wrapper class for the bioml Generate model module.
    | Generate the models from the ensemble.
    
    Args:
        input_excel (str): The file to where the selected features are saved in excel format. File type: input. Accepted formats: XLSX (edam:format_3620)
        input_hyperparameter (str): Hyperparameter file. File type: input. Accepted formats: XLSX (edam:format_3620).
        sheets (str): Names or index of the selected sheets for both features and hyperparameters and the index of the models in this format-> sheet (name, index):index model1,index model2 without the spaces. If only index or name of the sheets, it is assumed that all kfold models are selected. It is possible to have kfold indices in one sheet and in another ones without. File type: input. Accepted formats: STRING (edam:format_2560).
        label (str): The path to the labels of the training set in a csv format. File type: input. Accepted formats: CSV (edam:format_3752).
        output_model (str): The directory for the generated models. File type: output. Accepted formats: ZIP (edam:format_3987).
        properties (dict):
            * **num_thread** (*int*) - (10) The number of threads to use for the parallelization of outlier detection.
            * **scaler** (*str*) - ("robust") Choose one of the scaler available in scikit-learn, defaults to RobustScaler.
            * **label** (*str*) - (None) The path to the labels of the training set in a csv format.
            * **outliers** (*str*) - (None) A list of outliers if any, the name should be the same as in the excel file with the filtered features, you can also specify the path to a file in plain text format, each record should be in a new line.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.generate_model import generate_model
            prop = { num_thread: 10,
                    scaler: 'robust',
                    outliers: 'training_features/outliers.csv'}
                    
            generate_model(input_excel='training_features/selected_features.xlsx',
                            input_hyperparameter='training_features/hyperparameters.xlsx',
                            sheets='features:0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16',
                            label='training_features/labels.csv',
                            output_model = 'models.zip',
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
    def __init__(self, input_excel: str, input_hyperparameter: str, sheets: str, label: str, output_model: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_excel": input_excel, "input_hyperparameter": input_hyperparameter, "sheets": sheets, "label": label},
            "out": {"output_model": output_model}
        }

        # Properties specific for BB
        self.num_thread = properties.get('num_thread', None)
        self.scaler = properties.get('scaler', None)
        self.outliers = properties.get('outliers', None)

        # Properties common in all BB

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`generate_model <bioml.generate_model.generate_model>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m BioML.generate_model',
                    '--excel', self.stage_io_dict["in"]["input_excel"],
                    '--hyperparameter_path', self.stage_io_dict["in"]["input_hyperparameter"],
                    '--sheets', self.stage_io_dict["in"]["sheets"],
                    '--label', self.stage_io_dict["in"]["label"],
                    '--model_output', self.stage_io_dict["out"]["output_model"].rstrip('.zip')]

        if self.num_thread:
            self.cmd.append('--num_thread')
            self.cmd.append(self.num_thread)
        if self.scaler:
            self.cmd.append('--scaler')
            self.cmd.append(self.scaler)
        if self.outliers:
            self.cmd.append('--outliers')
            self.cmd.append(self.outliers)

        # Run Biobb block
        self.run_biobb()

        # Zip output
        to_zip = []
        to_zip.append(self.stage_io_dict["out"]["output_model"].rstrip('.zip'))
        to_zip.append(self.stage_io_dict["unique_dir"])
        com.zip_list(self.stage_io_dict["out"]["output_model"], to_zip)

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), ""])
        self.remove_tmp_files()

        return self.return_code


def generate_model(input_excel: str, input_hyperparameter: str, sheets: str, label: str, output_model: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`generate_model <bioml.generate_model.Generate_model>` class and
        execute the :meth:`launch() <bioml.generate_model.generate_model.launch>` method."""
    return Generate_model(input_excel=input_excel, input_hyperparameter=input_hyperparameter, sheets=sheets, output_model=output_model, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl genera_model module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_excel', required=True)
    required_args.add_argument('--input_hyperparameter', required=True)
    required_args.add_argument('--sheets', required=True)
    required_args.add_argument('--label', required=True)
    required_args.add_argument('--output_model', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    generate_model(input_excel=args.input_excel, input_hyperparameter=args.input_hyperparameter, sheets=args.sheets, label=args.label, output_model=args.output_model, properties=properties)


if __name__ == '__main__':
    main()