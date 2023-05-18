#!/usr/bin/env python3

"""Module containing the Model training class and the command line interface."""
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_bioml.bioml import common as com



class Model_training(BiobbObject):
    """
    | biobb_bioml Model training
    | Wrapper class for the bioml Model training module.
    | Train the models.

    Args:
        input_excel (str): The file to where the selected features are saved in excel format. File type: input. Accepted formats: xlsx (edam:format_3620).
        label (str): The path to the labels of the training set in a csv format. File type: input. Accepted formats: csv (edam:format_3752).
        hyperparameters (str): The path to the hyperparameters of the training set in a csv format. File type: output. Accepted formats: xlsx (edam:format_3620).
        training_output (str): ("training_results") The zip where to save the models training results. File type: output. Accepted formats: ZIP (edam:format_3989).
        properties (dict):
            * **num_thread** (*int*) - (50) The number of threads to search for the hyperparameter space.
            * **scaler** (*str*) - ("robust") "Choose one of the scaler available in scikit-learn, defaults to RobustScaler. Option: ("robust", "standard", "minmax").
            * **kfold_parameters** (*str*) - ("5:0.2") The parameters for the kfold in num_split:test_size format.
            * **outliers** (*str*) - (None) A list of outliers if any, the name should be the same as in the excel file with the filtered features, you can also specify the path to a file in plain text format, each record should be in a new line.
            * **precision_weight** (*float*) - (1) Weights to specify how relevant is the precision for the ranking of the different features.
            * **recall_weight** (*float*) - (0.8) Weights to specify how relevant is the recall for the ranking of the different features.
            * **class0_weight** (*float*) - (0.5) Weights to specify how relevant is the f1, precision and recall scores of the class 0 or the negative class for the ranking of the different features with respect to class 1 or the positive class.
            * **report_weight** (*float*) - (0.25) Weights to specify how relevant is the f1, precision and recall for the ranking of the different features with respect to MCC which is a more general measures of the performance of a model.
            * **difference_weight** (*float*) - (1.1) How important is to have similar training and test metrics.
            * **small** (*str*) - (None) Default to true, if the number of samples is < 300 or if you machine is slow. The hyperparameters tuning will fail if you set trial time short and your machine is slow.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.model_training import model_training
            prop = { num_thread: 50,
                    scaler: 'robust',
                    kfold_parameters: '5:0.2',
                    precision_weight: 1,
                    recall_weight: 0.8,
                    class0_weight: 0.5,
                    report_weight: 0.25,
                    difference_weight: 1.1}
                    
            model_training(input_excel='training_features/selected_features.xlsx',
                            label='training_features/labels.csv',
                            training_output: 'training_results.zip',
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
    def __init__(self, input_excel: str, label: str, hyperparameters: str, training_output: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        hyperparameters = hyperparameters or "training_results/hyperparameters.xlsx"

        # Input/Output files
        self.io_dict = {
            "in": {"input_excel": input_excel, "label": label},
            "out": {"training_output": training_output, "hyperparameters": hyperparameters}
        }

        # Properties specific for BB
        self.num_thread = properties.get('num_thread', None)
        self.scaler = properties.get('scaler', None)
        self.kfold_parameters = properties.get('kfold_parameters', None)
        self.outliers = properties.get('outliers', None)
        self.precision_weight = properties.get('precision_weight', None)
        self.recall_weight = properties.get('recall_weight', None)
        self.class0_weight = properties.get('class0_weight', None)
        self.report_weight = properties.get('report_weight', None)
        self.difference_weight = properties.get('difference_weight', None)
        self.small = properties.get('small', None)

        # Properties common in all BB

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`model_training <bioml.model_training.model_training>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m BioML.model_training',
                    '--excel', self.stage_io_dict["in"]["input_excel"],
                    '--label', self.stage_io_dict["in"]["label"],
                    '--training_output', self.stage_io_dict["out"]["training_output"].rstrip('.zip')]
        
        if self.num_thread:
            self.cmd.append('--num_thread')
            self.cmd.append(str(self.num_thread))
        if self.scaler:
            self.cmd.append('--scaler')
            self.cmd.append(self.scaler)
        if self.kfold_parameters:
            self.cmd.append('--kfold_parameters')
            self.cmd.append(self.kfold_parameters)
        if self.outliers:
            self.cmd.append('--outliers')
            self.cmd.append(str(self.outliers))
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
        if self.small:
            self.cmd.append('--small')
            self.cmd.append(self.small)

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Zip output
        to_zip = []
        to_zip.append(self.stage_io_dict["out"]["training_output"])
        to_zip.append(self.stage_io_dict["unique_dir"])
        com.zip_list(self.stage_io_dict["out"]["training_output"], to_zip)

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), ""])
        self.remove_tmp_files()

        return self.return_code


def model_training(input_excel: str, label: str, hyperparameters: str, training_output: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`model_training <bioml.model_training.Model_training>` class and
        execute the :meth:`launch() <bioml.model_training.model_training.launch>` method."""
    return Model_training(input_excel=input_excel, label=label, hyperparameters=hyperparameters, training_output=training_output, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl model_training module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_excel', required=True)
    required_args.add_argument('--label', required=True)
    required_args.add_argument('--hyperparameters', required=False)
    required_args.add_argument('--training_output', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    model_training(input_excel=args.input_excel, label=args.label, hyperparameters=args.hyperparameters, training_output=args.training_output, properties=properties)


if __name__ == '__main__':
    main()