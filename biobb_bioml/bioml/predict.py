#!/usr/bin/env python3

"""Module containing the Predict class and the command line interface."""

import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_bioml.bioml import common as com
import os


class Predict(BiobbObject):
    """
    | biobb_bioml Predict
    | Wrapper class for the bioml Predict module.
    | Predict using the models and average the votations.

    Args:
        input_excel (str): The file to where the selected features are saved in excel format.  File type: input. Accepted formats: XLSX (edam:format_3620)
        input_fasta (str): The fasta file path. File type: input. Accepted formats: FASTA (edam:format_1929).
        extracted (str): The file where the extracted features from the new data are stored. File type: input. Accepted formats: XLSX (edam:format_3620).
        properties (dict):
            * **scaler** (*str*) - ("robust") Choose one of the scaler available in scikit-learn, defaults to RobustScaler.
            * **model_output** (*str*) - ("models") The directory for the generated models.
            * **prediction_threshold** (*float*) - (1.0) Between 0.5 and 1 and determines what considers to be a positive prediction, if 1 only those predictions where all models agrees are considered to be positive.
            * **number_similar_samples** (*int*) - (1) The number of similar training samples to filter the predictions.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.predict import predict
            prop = { scaler: 'robust',
                    model_output: 'models',
                    prediction_threshold: 1.0,,
                    number_similar_samples: 1}

            predict(input_excel='training_features/selected_features.xlsx',
                            input_fasta='input.fasta',
                            extracted: 'extracted_features/new_features.xlsx'
                            properties=prop)

    Info:
        * wrapped_software:
            * name: BioMl predict
            * version: >0.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_excel: str, input_fasta: str, extracted: str,
                 properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        prediction_results =  properties.get('prediction_results', "prediction_results.zip")

        # Input/Output files
        self.io_dict = {
            "in": {"input_excel": input_excel, "input_fasta": input_fasta, "extracted": extracted},
            "out": {"prediction_results": prediction_results}
        }

        # Properties specific for BB
        self.scaler = properties.get('scaler', None)

        self.model_output =  properties.get('mode_output', None)
        #self.model_output = f"/data/galaxy_extra/tmp/{self.model_output}
        self.model_output = f"/home/bubbles/Ruite/esterase_dataset/tmp/{self.model_output}"
        self.prediction_threshold = properties.get('prediction_threshold', None)
        self.number_similar_samples = properties.get('number_similar_samples', None)
        # Properties common in all BB

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`predict <bioml.predict.predict>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m BioML.predict',
                    '--excel', self.stage_io_dict["in"]["input_excel"],
                    '--extracted', self.stage_io_dict["in"]["extracted"],
                    '--fasta_file', self.stage_io_dict["in"]["input_fasta"],
                    '--res_dir', self.stage_io_dict["out"]["prediction_results"].rstrip('.zip')]

        if self.scaler:
            self.cmd.append('--scaler')
            self.cmd.append(self.scaler)
        if self.model_output:
            self.cmd.append('--model_output')
            self.cmd.append(self.model_output)
        if self.prediction_threshold:
            self.cmd.append('--prediction_threshold')
            self.cmd.append(str(self.prediction_threshold))
        if self.number_similar_samples:
            self.cmd.append('--number_similar_samples')
            self.cmd.append(str(self.number_similar_samples))

        # Run Biobb block
        self.run_biobb()

        # Zip output
        results_path = os.path.join(os.path.dirname(os.path.dirname(self.stage_io_dict['out']['prediction_results'])), os.path.basename(self.stage_io_dict["out"]["prediction_results"]))
        to_zip = []
        to_zip.append(os.path.basename(self.stage_io_dict["unique_dir"]))
        print(f"Zipping {to_zip} to {results_path}")
        com.zip_list(results_path, to_zip)

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), ""])
        self.remove_tmp_files()

        return self.return_code


def predict(input_excel: str, extracted: str, input_fasta: str, output_model: str, properties: dict = None,
                   **kwargs) -> int:
    """Create :class:`predict <bioml.predict.Predict>` class and
        execute the :meth:`launch() <bioml.predict.predict.launch>` method."""
    return Predict(input_excel=input_excel,  extracted=extracted, input_fasta=input_fasta,
                          output_model=output_model, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl genera_model module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_excel', required=True)
    required_args.add_argument('--extracted', required=True)
    required_args.add_argument('--input_fasta', required=True)
    required_args.add_argument('--output_model', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    predict(input_excel=args.input_excel, extracted=args.extracted, input_fasta=args.input_fasta,
                   output_model=args.output_model, properties=properties)


if __name__ == '__main__':
    main()