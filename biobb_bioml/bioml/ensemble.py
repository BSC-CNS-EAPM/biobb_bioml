#!/usr/bin/env python3

"""Module containing the Ensemble class and the command line interface."""
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_bioml.bioml import common as com
import os


class Ensemble(BiobbObject):
    """
    | biobb_bioml Ensemble
    | Wrapper class for the bioml Ensemble module.
    | Generate ensemble of models from the user specified sheets in order to select the best combination of sheets and kfolds.

    Args:
        input_excel (str): The file to where the selected features are saved in excel format. File type: input. Accepted formats: XLSX (edam:format_3620).
        input_hyperparameter (str): Hyperparameter file. File type: input. Accepted formats: XLSX (edam:format_3620).
        sheets (str): Names or index of the selected sheets for both features and hyperparameters. File type: input. Accepted formats: text (edam:format_1964).
        ensemble_output (str): The zip file to the output for the ensemble results. File type: output. Accepted formats: ZIP (edam:format_3987).
        label (str): The path to the labels of the training set in a csv format. File type: input. Accepted formats: CSV (edam:format_3752).
        properties (dict):
            * **prediction_threshold** (*float*) - (1.0) Between 0.5 and 1 and determines what considers to be a positive prediction, if 1 only those predictions where all models agrees are considered to be positive.
            * **num_thread** (*int*) - (10) The number of threads to use for the parallelization of outlier detection.
            * **precision_weight** (*float*) - (1) Weights to specify how relevant is the precision for the ranking of the different features.
            * **recall_weight** (*float*) - (0.8) Weights to specify how relevant is the recall for the ranking of the different features.
            * **class0_weight** (*float*) - (0.5) Weights to specify how relevant is the f1, precision and recall scores of the class 0 or the negative class for the ranking of the different features with respect to class 1 or the positive class
            * **report_weight** (*float*) - (0.25) Weights to specify how relevant is the f1, precision and recall for the ranking of the different features with respect to MCC which is a more general measures of the performance of a model
            * **difference_weight** (*float*) - (1.1) How important is to have similar training and test metrics.
            * **kfold_parameters** (*str*) - ("5:0.2") The parameters for the kfold in num_split:test_size format.
            * **label** (*str*) - (None) The path to the labels of the training set in a csv format.
            * **scaler** (*str*) - ("robust") Choose one of the scaler available in scikit-learn, defaults to RobustScaler.
            * **outliers** (*str*) - (None) A list of outliers if any, the name should be the same as in the excel file with the filtered features, you can also specify the path to a file in plain text format, each record should be in a new line.
           
    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.ensemble import ensemble
            prop = { 'prediction_threshold': 1.0,
                    'num_thread': '10',
                    'precision_weight': '1',
                    'recall_weight': '0.8',
                    'class0_weight': '0.5',
                    'report_weight': '0.25',
                    'difference_weight': '1.1',
                    'kfold_parameters': '5:0.2',
                    'scaler': 'robust'
                     }
            ensemble(input_excel='training_features/selected_features.xlsx',
                   input_hyperparameter='training_features/hyperparameters.xlsx',
                   sheets='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15',
                   ensemble_output='ensemble.zip',
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
    def __init__(self, input_excel: str, input_hyperparameter: str, sheets: str, label: str, output_ensemble: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_excel": input_excel, "input_hyperparameter": input_hyperparameter, "sheets": sheets, "label": label},
            "out": {"output_ensemble": output_ensemble}
        }

        # Properties specific for BB
        self.prediction_threshold = properties.get('rediction_threshold', None)
        self.num_thread = properties.get('num_thread', None)
        self.precision_weight = properties.get('precision_weight', None)
        self.recall_weight = properties.get('recall_weight', None)
        self.class0_weight = properties.get('class0_weight', None)
        self.report_weight = properties.get('report_weight', None)
        self.difference_weight = properties.get('difference_weight', None)
        self.kfold_parameters = properties.get('kfold_parameters', None)
        self.label = properties.get('label', None)
        self.scaler = properties.get('scaler', None)
        self.outliers = properties.get('outliers', None)

        # Properties common in all BB


        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Ensemble <bioml.ensemble.Ensemble>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m BioML.ensemble',
                    '--excel', self.stage_io_dict["in"]["input_excel"],
                    '--hyperparameter_path', self.stage_io_dict["in"]["input_hyperparameter"],
                    '--sheets', self.stage_io_dict["in"]["sheets"],
                    '--label', self.stage_io_dict["in"]["label"],
                    '--ensemble_output', self.stage_io_dict["out"]["output_ensemble"].rstrip('.zip')]

        if self.prediction_threshold:
            self.cmd.append('--prediction_threshold')
            self.cmd.append(self.prediction_threshold)
        if self.num_thread:
            self.cmd.append('--num_thread')
            self.cmd.append(str(self.num_thread))
        if self.precision_weight:
            self.cmd.append('--precision_weight')
            self.cmd.append(self.precision_weight)
        if self.recall_weight:
            self.cmd.append('--recall_weight')
            self.cmd.append(self.recall_weight)
        if self.class0_weight:
            self.cmd.append('--class0_weight')
            self.cmd.append(self.class0_weight)
        if self.report_weight:
            self.cmd.append('--report_weight')
            self.cmd.append(self.report_weight)
        if self.difference_weight:
            self.cmd.append('--difference_weight')
            self.cmd.append(self.difference_weight)
        if self.kfold_parameters:
            self.cmd.append('--kfold_parameters')
            self.cmd.append(self.kfold_parameters)
        if self.scaler:
            self.cmd.append('--scaler')
            self.cmd.append(self.scaler)
        if self.outliers:
            self.cmd.append('--outliers')
            for outlier in self.outliers.split(','):
                self.cmd.append(f'"{outlier}"')
            
        # Run Biobb block
        self.run_biobb()

        # Zip the output
        results_path = os.path.join(os.path.dirname(os.path.dirname(self.stage_io_dict['out']['output_ensemble'])), os.path.basename(self.stage_io_dict["out"]["output_ensemble"]))
        to_zip = []
        to_zip.append(os.path.basename(self.stage_io_dict["unique_dir"]))
        print(f"Zipping {to_zip} to {results_path}")
        com.zip_list(results_path, to_zip)

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), ""])
        self.remove_tmp_files()

        return self.return_code


def ensemble(input_excel: str, input_hyperparameter: str, sheets:str, label: str, output_ensemble: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`Ensemble <bioml.ensemble.Ensemble>` class and
        execute the :meth:`launch() <bioml.ensemble.Ensemble.launch>` method."""
    return Ensemble(input_excel=input_excel, input_hyperparameter=input_hyperparameter,
                    sheets=sheets, label=label, output_ensemble=output_ensemble, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl ensemble module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_excel', required=True)
    required_args.add_argument('--input_hyperparameter', required=True)
    required_args.add_argument('--sheets', required=False)
    required_args.add_argument('--label', required=True)
    required_args.add_argument('--ensemble_output', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    ensemble(input_excel=args.input_excel, input_hyperparameter=args.input_hyperparameter, sheets=args.sheets, label=args.label, output_ensemble=args.ensemble_output,
            properties=properties)


if __name__ == '__main__':
    main()