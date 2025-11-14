import json
from icmdoutput.json_import import SingleModel

def test_singlemodel_access(tmp_path, mock_json_data):
    f = tmp_path / "mock.json"
    f.write_text(json.dumps(mock_json_data))
    sm = SingleModel(str(f), "modelA")
    grad = sm.get_gradient_component()
    assert not grad.empty