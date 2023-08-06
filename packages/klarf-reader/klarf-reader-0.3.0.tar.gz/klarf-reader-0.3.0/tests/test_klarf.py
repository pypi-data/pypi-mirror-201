# MODULES
from dataclasses import asdict
import inspect
from pathlib import Path
import dictdiffer

# UNITTEST
import unittest

# KLARF_READER
from klarf_reader.klarf import Klarf
from klarf_reader.models.klarf_content import (
    DieOrigin,
    DiePitch,
    KlarfContent,
    SampleCenterLocation,
    SamplePlanTest,
    SetupId,
    Summary,
    Wafer,
    SingleKlarfContent,
)

# UTILS
from klarf_reader.utils import klarf_convert

# TESTS
from tests.utils import *


ASSETS_PATH: Path = Path(__file__).parent / "assets"
ASSETS_SAVED_PATH: Path = ASSETS_PATH / "saved"


class TestKlarf(unittest.TestCase):
    def setUp(self) -> None:
        self.path_klarf_single_wafer = ASSETS_PATH / "J052SBN_8196_J052SBN-01.000"
        self.path_klarf_multi_wafers = ASSETS_PATH / "J237DTA_3236.000"

    def test_klarf_single_wafer(self) -> None:
        # Given
        expected = load_json(
            filename=ASSETS_SAVED_PATH
            / f"{self.__class__.__name__}__{inspect.currentframe().f_code.co_name}.json"
        )

        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_single_wafer)

        save_as_json(
            ASSETS_SAVED_PATH
            / f"{self.__class__.__name__}__{inspect.currentframe().f_code.co_name}.json",
            dict=asdict(content),
        )

        # Then
        self.assertEqual(asdict(content), expected)

    def test_klarf_single_wafer_with_custom_attributes(self) -> None:
        # Given
        expected = load_json(
            filename=ASSETS_SAVED_PATH
            / f"{self.__class__.__name__}__{inspect.currentframe().f_code.co_name}.json"
        )

        custom_columns_lot = ["TOTO"]
        custom_columns_defects = ["DEFECTAREA"]

        # When
        content = Klarf.load_from_file(
            filepath=self.path_klarf_single_wafer,
            custom_columns_lot=custom_columns_lot,
            custom_columns_defects=custom_columns_defects,
        )

        save_as_json(
            ASSETS_SAVED_PATH
            / f"{self.__class__.__name__}__{inspect.currentframe().f_code.co_name}.json",
            dict=asdict(content),
        )

        # Then
        self.assertEqual(asdict(content), expected)

    def test_klarf_single_wafer_with_raw_content(self) -> None:
        # Given
        expected_raw_content_length = 13356

        # When
        content, raw_content = Klarf.load_from_file_with_raw_content(
            filepath=self.path_klarf_single_wafer
        )

        # Then
        self.assertEqual(len(raw_content), expected_raw_content_length)

    def test_klarf_multi_wafers(self) -> None:
        # Given
        expected = load_json(
            filename=ASSETS_SAVED_PATH
            / f"{self.__class__.__name__}__{inspect.currentframe().f_code.co_name}.json"
        )

        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_multi_wafers)
        content_dict = asdict(content)

        save_as_json(
            ASSETS_SAVED_PATH
            / f"{self.__class__.__name__}__{inspect.currentframe().f_code.co_name}.json",
            dict=content_dict,
        )

        # Then
        diff = get_diff(item_1=[content_dict], item_2=[expected])

        self.assertEqual(content_dict, expected)

    def test_convert_single_klarf_content(self) -> None:
        # Given
        expected = load_json(
            filename=ASSETS_SAVED_PATH
            / f"{self.__class__.__name__}__{inspect.currentframe().f_code.co_name}.json"
        )

        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_multi_wafers)
        single_klarf_content = klarf_convert.convert_to_single_klarf_content(
            klarf_content=content, wafer_index=0
        )

        single_klarf_content_dict = asdict(single_klarf_content)

        save_as_json(
            ASSETS_SAVED_PATH
            / f"{self.__class__.__name__}__{inspect.currentframe().f_code.co_name}.json",
            dict=single_klarf_content_dict,
        )

        # Then
        diff = get_diff(item_1=[single_klarf_content_dict], item_2=[expected])

        self.assertEqual(single_klarf_content_dict, expected)
