#!/usr/bin/env python3

"""Module containing the Outlier class and the command line interface."""
import argparse
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class Outlier(BiobbObject):
    """
    | biobb_bioml Outlier
    | Wrapper class for the bioml Outlier module.
    | Detect outliers from the selected features.

    Args:
        input_excel (str): The file to where the selected features are saved in excel format.  File type: input. Accepted formats: XLSX (edam:format_3620).
        output_outlier (str): The path to the output for the outliers. File type: output. Accepted formats: CSV (edam:format_3752).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **num_thread** (*int*) - (10) The number of threads to use for the parallelization of outlier detection.
            * **scaler** (*str*) - ("robust") "Choose one of the scaler available in scikit-learn, defaults to RobustScaler. Option: ("robust", "standard", "minmax").
            * **contamination** (*float*) - (0.06) The expected % of outliers.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.outlier import outlier
            prop = {num_thread: 10,
                    scaler: 'robust',
                    contamination: 0.06}

            outlier(input_excel='training_features/selected_features.xlsx',
                            output_outlier = 'training_results/outliers.csv',
                            properties=prop)

    Info:
        * wrapped_software:
            * name: BioMl outlier model
            * version: >0.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_excel: str, output_outlier: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_excel": input_excel},
            "out": {"output_model": output_outlier}
        }

        # Properties specific for BB
        self.num_thread = properties.get('num_thread', None)
        self.scaler = properties.get('scaler', None)
        self.contamination = properties.get('contamination', None)
        # Properties common in all BB

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`outlier <bioml.outlier.outlier>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m BioML.outlier',
                    '-e', self.stage_io_dict["in"]["input_excel"],
                    '-o', self.stage_io_dict["out"]["output_outlier"]]

        if self.num_thread:
            self.cmd.append('--num_thread')
            self.cmd.append(self.num_thread)
        if self.scaler:
            self.cmd.append('--scaler')
            self.cmd.append(self.scaler)
        if self.contamination:
            self.cmd.append('--contamination')
            self.cmd.append(self.contamination)

        # Run Biobb block
        self.run_biobb()

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), ""])
        self.remove_tmp_files()

        return self.return_code


def outlier(input_excel: str, output_outlier: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`outlier <bioml.outlier.Outlier>` class and
        execute the :meth:`launch() <bioml.outlier.outlier.launch>` method."""
    return Outlier(input_excel=input_excel, output_outlier=output_outlier, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl genera_model module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_excel', required=True)
    required_args.add_argument('--output_outlier', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    outlier(input_excel=args.input_excel, output_outlier=args.output_outlier, properties=properties)


if __name__ == '__main__':
    main()