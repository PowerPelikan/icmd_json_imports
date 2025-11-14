import json
from icmdoutput.models.solidification import Solidification

def test_solidification_basic(tmp_path, mock_json_data):
    f = tmp_path / "mock.json"
    f.write_text(json.dumps(mock_json_data))
    solid = Solidification(str(f), "modelA")

    df_regions = solid.get_solid_regions()
    assert not df_regions.empty
    scheil_df = solid.get_data_for_scheil_plot()
    assert "Phase Region" in scheil_df.columns