#!/usr/bin/env python3

"""Module containing the Generate pssm class and the command line interface."""
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_bioml.bioml import common as com


class Generate_pssm(BiobbObject):
    """
    | biobb_bioml Generate pssm
    | Wrapper class for the `bioml Generate pssm module.
    | Creates a database and performs psiblast.

    Args:
        input_fasta (str): The fasta file.  File type: input. Accepted formats: FASTA (edam:format_1929).
        output_pssm (str): A zip file containing the pssm files. File type: output. Accepted formats: ZIP (edam:format_3989).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **dbinp** (*str*) - (None) The path to the fasta files to create the database.
            * **dbout** (*str*) - ("database/uniref50") The name for the created database.
            * **num_thread** (*int*) - (100) The number of threads to use for the generation of pssm profiles.
            * **number** (*str*) - ("*") A number for the files.
            * **iterations** (*int*) - (3) The number of iterations in PSIBlast.
            * **possum_dir** (*str*) - ("POSSUM_Toolkit") A path to the possum programme.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_bioml.generate_pssm import generate_pssm
            prop = { dbout: 'database/uniref50',
                    num_thread: 100,
                    number: '*',
                    iterations: 3,
                    possum_dir: 'POSSUM_Toolkit'}

            generate_pssm(input_fasta='file.fasta',
                            output_pssm = 'pssm.zip',
                            properties=prop)

    Info:
        * wrapped_software:
            * name: BioMl generate pssm
            * version: >0.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_fasta: str, output_pssm: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_fasta": input_fasta},
            "out": {"output_pssm": output_pssm}
        }

        # Properties specific for BB
        self.dbinp = properties.get('dbinp', None)
        self.dbout = properties.get('dbout', None)
        self.num_thread = properties.get('num_thread', None)
        self.number = properties.get('number', None)
        self.iterations = properties.get('iterations', None)
        self.possum_dir = properties.get('possum_dir', None)

        # Properties common in all BB

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`generate_pssm <bioml.generate_pssm.generate_pssm>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # This is a placeholder
        fu.log('Creating command line with parameters', self.out_log, self.global_log)
        self.cmd = ['python -m BioML.generate_pssm',
                    '--i', self.stage_io_dict["in"]["input_fasta"]]

        if self.dbinp:
            self.cmd.append('--dbinp')
            self.cmd.append(self.dbinp)

        if self.dbout:
            self.cmd.append('--dbout')
            self.cmd.append(self.dbout)

        if self.num_thread:
            self.cmd.append('--num_thread')
            self.cmd.append(self.num_thread)

        if self.number:
            self.cmd.append('--number')
            self.cmd.append(self.number)

        if self.iterations:
            self.cmd.append('--iterations')
            self.cmd.append(self.iterations)

        if self.possum_dir:
            self.cmd.append('--possum_dir')
            self.cmd.append(self.possum_dir)

        # Run Biobb block
        self.run_biobb()

        # TODO - Test may not work
        com.create_zip(self.stage_io_dict["out"]["output_pssm"], self.stage_io_dict["unique_dir"])

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), ""])
        self.remove_tmp_files()

        return self.return_code


def generate_pssm(input_fasta: str, output_pssm: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`generate_pssm <bioml.generate_pssm.Generate_pssm>` class and
        execute the :meth:`launch() <bioml.generate_pssm.generate_pssm.launch>` method."""
    return Generate_pssm(input_fasta=input_fasta, output_pssm=output_pssm, properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the BioMl generate_pssm module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_fasta', required=True)
    required_args.add_argument('--output_pssm', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    generate_pssm(input_fasta=args.input_fasta, output_pssm=args.output_pssm, properties=properties)


if __name__ == '__main__':
    main()