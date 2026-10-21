import pandas as pd
from streamlit.testing.v1 import AppTest

def test_dataset_loads():
    df = pd.read_csv("data/student-mat.csv", sep=";")
    assert df.shape == (395, 33)

def test_app_starts_without_error():
    at = AppTest.from_file("app.py", default_timeout=120).run()
    assert not at.exception