import json
from icmdoutput.models.plotting.scheil_plot import Scheil

def test_scheil_plot_builds(tmp_path, mock_json_data):
    f = tmp_path / "mock.json"
    f.write_text(json.dumps(mock_json_data))
    s = Scheil(str(f), "modelA")
    df = s.get_scheil_df()
    assert "Percent solidified molar" in df.columns