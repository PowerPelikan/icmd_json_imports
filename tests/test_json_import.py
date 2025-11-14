import json
import pandas as pd
from icmdoutput.json_import import JsonData

def test_jsondata_extract_elements_handles_missing(tmp_path, mock_json_data):
    """Ensure missing model component data doesn't cause failure."""
    f = tmp_path / "mock.json"
    f.write_text(json.dumps(mock_json_data))
    jd = JsonData(str(f))

    df = jd.get_elements()
    assert isinstance(df, pd.DataFrame)
    # one model has elements, one is empty
    assert "modelA" in df.index or "modelA" in df.columns
    assert any("Fe" in str(x) for x in df.to_numpy().flatten())

def test_jsondata_model_listing(tmp_path, mock_json_data):
    f = tmp_path / "mock.json"
    f.write_text(json.dumps(mock_json_data))
    jd = JsonData(str(f))
    models = jd.get_models()
    assert set(models) == {"modelA", "modelB"}
    data = jd.get_data()
    assert "models" in data