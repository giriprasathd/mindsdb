import os
import time
import pytest
from unittest.mock import patch

import pandas as pd
from mindsdb_sql import parse_sql

from ..executor_test_base import BaseExecutorTest


class TestTimeGPT(BaseExecutorTest):
    @staticmethod
    def get_api_key():
        """Retrieve TimeGPT API key from environment variables"""
        return os.environ.get("TIMEGPT_API_KEY")

    def wait_predictor(self, project, name):
        # wait
        done = False
        for attempt in range(200):
            ret = self.run_sql(f"select * from {project}.models where name='{name}'")
            if not ret.empty:
                if ret["STATUS"][0] == "complete":
                    done = True
                    break
                elif ret["STATUS"][0] == "error":
                    raise RuntimeError("predictor failed", ret["ERROR"][0])
            time.sleep(0.5)
        if not done:
            raise RuntimeError("predictor wasn't created")

    def run_sql(self, sql):
        ret = self.command_executor.execute_command(parse_sql(sql, dialect="mindsdb"))
        assert ret.error_code is None
        if ret.data is not None:
            columns = [col.alias if col.alias is not None else col.name for col in ret.columns]
            return pd.DataFrame(ret.data, columns=columns)

    def test_no_timeseries_query(self):
        self.run_sql("create database proj")
        self.run_sql(f"""create ml_engine timegpt from timegpt using api_key='{self.get_api_key()}';""")
        self.run_sql(
            """
            create model proj.test_timegpt_unknown_arguments
            predict expenditure -- as we don't pass any time series arguments, model should fail to create
            using
                engine='timegpt',
                wrong_argument_name='any value';
        """
        )
        with pytest.raises(Exception) as e:
            self.wait_predictor("proj", "test_timegpt_unknown_arguments")

        assert "KeyError: 'is_timeseries'" in str(e.value.args[1])

    @patch("mindsdb.integrations.handlers.postgres_handler.Handler")
    def test_forecast_group(self, mock_handler):
        # create project
        self.run_sql("create database proj")
        df = pd.read_csv('tests/unit/ml_handlers/data/house_sales.csv')
        self.set_handler(mock_handler, name="pg", tables={"df": df})

        window = 128
        horizon = 8

        self.run_sql(f"""create ml_engine timegpt from timegpt using api_key='{self.get_api_key()}';""")
        self.run_sql(
            f"""
           create model proj.test_timegpt_forecast
           predict ma
           order by saledate
           group by type, bedrooms
           window {window}
           horizon {horizon}
           using
             engine='timegpt';
        """
        )
        self.wait_predictor("proj", "test_timegpt_forecast")

        ret = self.run_sql(
            """
            SELECT p.*
            FROM proj.test_timegpt_forecast as p
            JOIN pg.df as t
            WHERE p.saledate > LATEST
            AND t.type = 'house' AND t.bedrooms = 2;
        """
        )
        assert ret.shape[0] == horizon
