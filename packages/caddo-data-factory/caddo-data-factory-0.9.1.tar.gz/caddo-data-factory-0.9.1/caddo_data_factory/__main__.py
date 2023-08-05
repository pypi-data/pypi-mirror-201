import os
import sys

import pandas as pd
from caddo_file_parser.settings.generation_settings import GenerationSettings

from caddo_data_factory.functions.functions_loader import FunctionsLoader
from caddo_data_factory.functions.folds_preparation import FoldsPreparation
from caddo_file_parser.caddo_file_parser import CaddoFileParser
from caddo_file_parser.models.caddo_file import CaddoFile
from caddo_data_factory.settings.settings_reader import SettingsReader


def open_dataset_file(path, sep):
    chunksize = 10 ** 6
    chunks =  pd.read_csv(path, sep=sep, chunksize=chunksize)
    dataset = pd.DataFrame()
    dataset = pd.concat(chunk for chunk in chunks)
    # dataset = pd.read_csv(path, sep=sep)
    return dataset


class DataFactory:
    def __init__(self):
        print("INIT")
        settings_file_path = f'{os.getcwd()}/settings.yaml'
        if sys.argv[1] == "--configuration":
            settings_file_path = sys.argv[2]
        self.dataSettings: GenerationSettings = SettingsReader(settings_file_path).load()
        print(self.dataSettings)
        self.folds_preparation = FoldsPreparation()
        self.extraction_module = None
        self.load_modules()
        self.run()

    def load_modules(self):
        print("LOADING DATA EXTRACTION FUNCTION:")
        functions_loader = FunctionsLoader()
        self.extraction_module = functions_loader.extract_features_keywords(self.dataSettings)
        print()

    def run(self):
        print("READ DATA FROM FILE")
        dataset_df = open_dataset_file(self.dataSettings.data_input_path, self.dataSettings.data_input_separator)
        seeds = CaddoFileParser().read_seeds(self.dataSettings)

        print("EXTRACT DATA")
        pre_processed_data = self.extraction_module.extract(dataset_df)

        print("PREPARE FOLDS")
        folds = self.folds_preparation.get_folds_dataset(dataset_df, self.dataSettings, seeds)

        print("SAVE TO .CADDO FILE")
        caddoFile = CaddoFile(folds, pre_processed_data, self.dataSettings, seeds)
        CaddoFileParser().create_file(caddoFile)

if __name__ == '__main__':
    DataFactory()
