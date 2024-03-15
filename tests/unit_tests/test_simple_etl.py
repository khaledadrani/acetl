import os
from functools import partial

import pandas as pd
import pytest

from source.etl_csv.simple_etl import SimpleETLPipeline
from source.common.configuration.config import ROOT_DIRECTORY, DatabaseConfig
from source.common.utils.generate_dummy_data import save_to_csv, generate_fake_data


class TestSimpleETLPipeline:
    test_data_path = ROOT_DIRECTORY / "data/test_data_path.csv"

    def setup_method(self):
        save_to_csv(generate_fake_data(100), self.test_data_path)

        self.simple_etl = partial(SimpleETLPipeline,
                                  data_path=self.test_data_path,
                                  database_url=DatabaseConfig().database_url
                                  )

    def teardown_method(self):
        os.unlink(self.test_data_path)

    def test_setup_file(self):
        df = pd.read_csv(self.test_data_path)

        assert len(df) == 100

    def test_extract(self):
        etl = self.simple_etl()

        etl.extract()

        assert len(etl.current_data) == 100

    def test_transform(self):
        etl = self.simple_etl()

        etl.extract()

        etl.transform()

        assert len(etl.current_data) < 100 # there must be some rows dropped

    @pytest.mark.skip("TODO")
    def test_load(self):
        """
        "TODO Require implementing fake classes for db session"
        :return:
        """
        pass

