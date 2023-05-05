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
    TODO: Add a description of the module.
    Args:
        input_features (str): The path to the training features that contains both ifeature and possum in csv format. `Sample file <>`_. Accepted formats: fasta (edam:format_1929).

        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **label** (*str*) - ("pssm") The pssm files directory's path.
            * **fasta_dir** (*str*) - ("fasta_files") The directory for the fasta files.
            * **ifeature_dir** (*str*) - ("iFeature") Path to the iFeature programme folder.
            * **possum_dir** (*str*) - ("POSSUM_Toolkit") A path to the possum programme.
            * **ifeature_out** (*str*) - ("ifeature_features") The directory where the ifeature features are.
            * **possum_out** (*str*) - ("possum_features") The directory for the possum extractions.
            * **filtered_out** (*str*) - ("training_features") The directory for the filtered features from the new data or the features for training.
            * **excel** (*str*) - ("training_features/selected_features.xlsx") The path to where the selected features from training are saved in excel format, it will
                                    be used to select specific columns from all the generated features for the new data.
            * **purpose** (*str*) - ("extract") Choose the operation between extracting reading for training or filtering for prediction, ("extract", "read", "filter").
            * **long** (*str*) - (False) True when restarting from the long commands.
            * **run** (*str*) - ("both") Run possum or ifeature extraction, ("possum", "ifeature", "both").
            * **num_thread** (*int*) - (100) The number of threads to use for the generation of pssm profiles.
            * **type** (*str*) - ("all") A list of the features to extract, ("all", "APAAC", "PAAC",
                        "CKSAAGP","Moran", "Geary", "NMBroto", "CTDC", "CTDT", "CTDD", "CTriad", "GDPC", "GTPC",
                        "QSOrder", "SOCNumber", "GAAC", "KSCtriad",
                        "aac_pssm", "ab_pssm", "d_fpssm", "dp_pssm", "dpc_pssm", "edp", "eedp", "rpm_pssm",
                        "k_separated_bigrams_pssm", "pssm_ac", "pssm_cc", "pssm_composition", "rpssm", "s_fpssm",
                        "smoothed_pssm:5", "smoothed_pssm:7", "smoothed_pssm:9", "tpc", "tri_gram_pssm", "pse_pssm:1",
                        "pse_pssm:2", "pse_pssm:3").
            * **type_file** (*str*) - (None) The path to the a file with the feature names.
            * **selected** (*str*) - (None) The selected_algorithms with the selected feature sets in algorithm:feature_set format.
            
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.ensemble import ensemble
            prop = { pssm_dir: 'pssm', 
                    fasta_dir: 'fasta_files', 
                    ifeature_dir: 'iFeature', 
                    possum_dir: 'POSSUM_Toolkit',
                    ifeature_out: 'ifeature_features',
                    possum_out: 'possum_features',
                    filtered_out: 'training_features',
                    excel: 'training_features/selected_features.xlsx',
                    purpose: 'extract',
                    long: False,
                    run: 'both',
                    num_thread: 100,
                    type: 'all',
                    type_file: None,
                    selected: None }
                    
            feature_extraction(input_fasta_file='input.fasta',
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
    def __init__(self, input_fasta_file: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_fasta_file": input_fasta_file},
            "out": {}
        }

        # Properties specific for BB
        self.pssm_dir = properties.get('pssm_dir', 'pssm')
        self.fasta_dir = properties.get('fasta_dir', 'fasta_files')
        self.ifeature_dir = properties.get('ifeature_dir', 'iFeature')
        self.possum_dir = properties.get('possum_dir', 'POSSUM_Toolkit')
        self.ifeature_out = properties.get('ifeature_out', 'ifeature_features')
        self.possum_out = properties.get('possum_out', 'possum_features')
        self.filtered_out = properties.get('filtered_out', 'training_features')
        self.excel = properties.get('excel', 'training_features/selected_features.xlsx')
        self.purpose = properties.get('purpose', 'extract')
        self.long = properties.get('long', False)
        self.run = properties.get('run', 'both')
        self.num_thread = properties.get('num_thread', 100)
        self.type = properties.get('type', 'all')
        self.type_file = properties.get('type_file', None)
        self.selected = properties.get('selected', None)

        # Properties common in all GROMACS BB

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Feature_extraction <bioml.feature_extraction.Feature_extraction>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()


        if self.container_path:
            shutil.copytree("", Path(self.stage_io_dict.get("unique_dir")).joinpath(Path("").name))
            file1 = str(Path(self.container_volume_path).joinpath(Path(file1).name, Path(file1).name))

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m Feature_extraction',
                    '-i', self.stage_io_dict["in"]["input_fasta_file"]]



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


def feature_selection(input_fasta_file: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`Feature_extraction <bioml.feature_extraction.Feature_extraction>` class and
        execute the :meth:`launch() <bioml.feature_extraction.Feature_extraction.launch>` method."""
    return Feature_selection(input_fasta_file=input_fasta_file, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl ensemble module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    feature_extraction(input_fasta_file=args.i, properties=properties)


if __name__ == '__main__':
    main()