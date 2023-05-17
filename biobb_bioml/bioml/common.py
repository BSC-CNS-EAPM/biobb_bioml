""" Common functions for package biobb_bioml """
import logging
import os
import typing
import zipfile
from pathlib import Path


def zip_list(zip_file: str, file_list: typing.Iterable[str], out_log: logging.Logger = None):
    file_list.sort()
    with zipfile.ZipFile(zip_file, 'w') as zip_f:
        inserted = []
        for index, f in enumerate(file_list):
            if os.path.exists(Path(f)):
                base_name = Path(f).name
                if os.path.isdir(Path(f)):
                    for root, dirs, files in os.walk(f):
                        for file in files:
                            zip_f.write(root+"/"+file)
                            inserted.append(file)
                if base_name in inserted:
                    base_name = 'file_' + str(index) + '_' + base_name
                inserted.append(base_name)
                zip_f.write(f)
    if out_log:
        out_log.info("Adding:")
        out_log.info(str(file_list))
        out_log.info("to: " + str(Path(zip_file).resolve()))