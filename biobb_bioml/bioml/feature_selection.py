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



class Feature_selection(BiobbObject):
    """
    | biobb_bioml Feature selection
    | Wrapper class for the `bioml Feature selection <>`_ module.
    | Preprocess and Select the best features.
    
    Args:
        input_features (str): The path to the training features that contains both ifeature and possum in csv format. `Sample file <>`_. Accepted formats: fasta (edam:format_1929).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **label** (*str*) - (None) The path to the labels of the training set in a csv format if not in the features, if present in the features csv use the flag to specify the label column name
            * **feature_range** (*str*) - ("20:none:10") Specify the minimum and maximum of number of features in start:stop:step format or a single integer. Stop can be none then the default value will be (n_samples / 2)".
            * **num_thread** (*int*) - (10) The number of threads to use for parallelizing the feature selection.
            * **variance_threshold** (*float*) - (7) It will influence the features to be eliminated the larger the less restrictive.
            * **scaler** (*str*) - ("robust") Choose one of the scaler available in scikit-learn, defaults to RobustScaler. Options: ("robust", "standard", "minmax").
            * **excel** (*str*) - ("training_features/selected_features.xlsx") The file path to where the selected features will be saved in excel format.
            * **kfold_parameters** (*str*) - ("5:0.2") The parameters for the kfold in num_split:test_size format.
            * **rfe_steps** (*int*) - (40) The number of steps for the RFE algorithm, the more step the more precise but also more time consuming be used to select specific columns from all the generated features for the new data.
            * **plot** (*bool*) - (True) Default to true, plot the feature importance using shap.
            * **plot_num_features** (*int*) - (20) How many features to include in the plot.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.ensemble import ensemble
            prop = { features: 'training_features/every_features.csv', 
                    feature_range: '20:none:10', 
                    num_thread: 10, 
                    variance_threshold: 7,
                    scaler: 'robust',
                    possum_out: 'possum_features',
                    filtered_out: 'training_features',
                    excel: 'training_features/selected_features.xlsx',
                    kfold_parameters: '5:0.2',
                    rfe_steps: 40,
                    plot: True,
                    plot_num_features: 20}
                    
            feature_selection(input_features='input.fasta',
                            properties=prop)

    Info:
        * wrapped_software:
            * name: BioMl feature extraction
            * version: >0.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """
    def __init__(self, input_features: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_features": input_features},
            "out": {}
        }

        # Properties specific for BB
        self.label = properties.get('label', None)
        self.feature_range = properties.get('feature_range', '20:none:10')
        self.num_thread = properties.get('num_thread', 10)
        self.variance_threshold = properties.get('variance_threshold', 7)
        self.scaler = properties.get('scaler', 'robust')
        self.excel = properties.get('excel', 'training_features/selected_features.xlsx')
        self.kfold_parameters = properties.get('kfold_parameters', '5:0.2')
        self.rfe_steps = properties.get('rfe_steps', 40)
        self.plot = properties.get('plot', True)
        self.plot_num_features = properties.get('plot_num_features', 20)

        # Properties common in all BB

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`feature_selection <bioml.feature_selection.feature_selection>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()


        if self.container_path:
            shutil.copytree("", Path(self.stage_io_dict.get("unique_dir")).joinpath(Path("").name))
            file1 = str(Path(self.container_volume_path).joinpath(Path(file1).name, Path(file1).name))

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m feature_selection',
                    '--features', self.stage_io_dict["in"]["input_features"]]
        
        if self.label:
            self.cmd.append(f"--label {self.label}")
        if self.feature_range:
            self.cmd.append(f"--feature_range {self.feature_range}")
        if self.num_thread:
            self.cmd.append(f"--num_thread {self.num_thread}")
        if self.variance_threshold:
            self.cmd.append(f"--variance_threshold {self.variance_threshold}")
        if self.scaler:
            self.cmd.append(f"--scaler {self.scaler}")
        if self.excel:
            self.cmd.append(f"--excel {self.excel}")
        if self.kfold_parameters:
            self.cmd.append(f"--kfold_parameters {self.kfold_parameters}")
        if self.rfe_steps:
            self.cmd.append(f"--rfe_steps {self.rfe_steps}")
        if self.plot:
            self.cmd.append(f"--plot {self.plot}")
        if self.plot_num_features:
            self.cmd.append(f"--plot_num_features {self.plot_num_features}")


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


def feature_selection(input_features: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`feature_selection <bioml.feature_selection.Feature_selection>` class and
        execute the :meth:`launch() <bioml.feature_selection.feature_selection.launch>` method."""
    return Feature_selection(input_features=input_features, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl feature_selection module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_features', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    feature_selection(input_features=args.input_features, properties=properties)


if __name__ == '__main__':
    main()