import json
from icmdoutput.models.equilibrium import Equilibrium

def test_equilibrium_loading(tmp_path, mock_json_data):
    f = tmp_path / "mock.json"
    f.write_text(json.dumps(mock_json_data))
    eq = Equilibrium(str(f), "modelA")
    # Only basic keys checked because mock doesn't include all vars
    assert eq.get_phase_names_df().shape[0] >= 1