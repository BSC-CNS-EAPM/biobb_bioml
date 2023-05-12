#!/usr/bin/env python3

"""Module containing the Ensemble class and the command line interface."""
import os
import shutil
import argparse
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger



class Ensemble(BiobbObject):
    """
    | biobb_bioml Ensemble
    | Wrapper class for the `bioml Ensemble <>`_ module.
    | .

    Args:
        input_excel (str): The file to where the selected features are saved in excel format. `Sample file <>`_. Accepted formats: xlsx (edam:format_3620).
        output_ensemble (str): The path to the output for the ensemble results. File type: output. `Sample file <>`_. Accepted formats: ... (edam:format_XXXX).
        input_hyperparameter_path (str): Path to the hyperparameter file. File type: input. `Sample file <>`_. Accepted formats: ... (edam:format_xxxx).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **sheets** (*list*) - (None) Names or index of the selected sheets for both features and hyperparameters.
            * **rediction_threshold** (*float*) - (0.5) Between 0.5 and 1.
            * **precision_weight** (*float*) - (1) Weights to specify how relevant is the precision for the ranking of the different features.
            * **recall_weight** (*float*) - (0.8) Weights to specify how relevant is the recall for the ranking of the different features.
            * **class0_weight** (*float*) - (0.5) Weights to specify how relevant is the f1, precision and recall scores of the class 0 
                                            or the negative class for the ranking of the different features with respect to class 1 or 
                                            the positive class.
            * **report_weight** (*float*) - ("0.25") Weights to specify how relevant is the f1, precision and recall for the ranking of the
                                            different features with respect to MCC and the R2 which are more general measures of
                                            the performance of a model
            * **difference_weight** (*float*) - (0.8) How important is to have similar training and test metrics.
            * **kfold_parameters** (*str*) - ("5:0.2") The parameters for the kfold in num_split:test_size format.
            * **label** (*str*) - (None) The path to the labels of the training set in a csv format.
            * **scaler** (*str*) - ("robust") Choose one of the scaler available in scikit-learn, defaults to RobustScaler, ("robust", "standard", "minmax").
           
    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.ensemble import ensemble
            prop = { 'rediction_threshold': 0.5,
                     'precision_weight': '1',
                     'recall_weight': '0.8',
                     'class0_weight': '0.5',
                     'report_weight': '0.25',
                     'difference_weight': '0.8',
                     'kfold_parameters': '5:0.2',
                     'scaler': 'robust'
                     }
            genion(input_excel='training_features/selected_features.xlsx',
                   output_ensemble='ensemble_results',
                   input_hyperparameter_path='hyperparameter',
                   properties=prop)

    Info:
        * wrapped_software:
            * name: BioMl ensemble
            * version: >0.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """
    def __init__(self, input_excel: str, output_ensemble: str, input_hyperparameter_path: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_excel": input_excel, "input_hyperparameter_path": input_hyperparameter_path},
            "out": {"output_ensemble": output_ensemble}
        }

        # Properties specific for BB        
        self.sheets = properties.get('sheets', None)
        self.rediction_threshold = properties.get('rediction_threshold', 0.5)
        self.precision_weight = properties.get('precision_weight', 1)
        self.recall_weight = properties.get('recall_weight', 0.8)
        self.class0_weight = properties.get('class0_weight', 0.5)
        self.report_weight = properties.get('report_weight', 0.25)
        self.difference_weight = properties.get('difference_weight', 0.8)
        self.kfold_parameters = properties.get('kfold_parameters', '5:0.2')
        self.label = properties.get('label', None)
        self.scaler = properties.get('scaler', 'robust')

        # Properties common in all BB


        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Ensemble <bioml.ensemble.Ensemble>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()


        if self.container_path:
            shutil.copytree("", Path(self.stage_io_dict.get("unique_dir")).joinpath(Path("").name))
            file1 = str(Path(self.container_volume_path).joinpath(Path(file1).name, Path(file1).name))

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m Ensemble',
                    '-e', self.stage_io_dict["in"]["input_excel"],
                    '-hp', self.stage_io_dict["in"]["input_hyperparameter_path"],
                    '-o', self.stage_io_dict["out"]["output_ensemble"]]

        if self.sheets:
            self.cmd.append(f'-sc {self.sheets}')

        if self.rediction_threshold:
            self.cmd.append(f'-va {self.rediction_threshold}')

        if self.precision_weight:
            self.cmd.append(f'-pw {self.precision_weight}')

        if self.recall_weight:
            self.cmd.append(f'-rw {self.recall_weight}')

        if self.class0_weight:
            self.cmd.append(f'-c0 {self.class0_weight}')

        if self.report_weight:
            self.cmd.append(f'-rpw {self.report_weight}')

        if self.difference_weight:
            self.cmd.append(f'-dw {self.difference_weight}')

        if self.kfold_parameters:
            self.cmd.append(f'-k {self.kfold_parameters}')
        
        if self.label:
            self.cmd.append(f'-l {self.label}')

        if self.scaler:
            self.cmd.append(f'-s {self.scaler}')

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


def ensemble(input_excel: str, input_hyperparameter_path: str, output_ensemble: str,
              properties: dict = None, **kwargs) -> int:
    """Create :class:`Ensemble <bioml.ensemble.Ensemble>` class and
        execute the :meth:`launch() <bioml.ensemble.Ensemble.launch>` method."""
    return Ensemble(input_excel=input_excel, input_hyperparameter_path=input_hyperparameter_path,
                    output_ensemble=output_ensemble, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl ensemble module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-e', required=True)
    required_args.add_argument('-hp', required=True)
    required_args.add_argument('-o', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    ensemble(input_excel=args.e, input_hyperparameter_path=args.hp, output_ensemble=args.o,
            properties=properties)


if __name__ == '__main__':
    main()