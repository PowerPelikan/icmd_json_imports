import json
from icmdoutput.redundant_data import PhasesAndTemps

def test_phase_fraction_and_temps(tmp_path, mock_json_data):
    f = tmp_path / "mock.json"
    f.write_text(json.dumps(mock_json_data))
    pt = PhasesAndTemps(str(f), "modelA")

    df_t = pt.get_temperatures()
    assert "Temperature in C" in df_t.columns
    fracs = pt.get_phase_fraction()
    assert fracs.shape[0] > 0