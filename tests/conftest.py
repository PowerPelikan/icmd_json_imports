import pytest

@pytest.fixture
def mock_json_data():
    """Mock JSON with two models, one missing components."""
    return {
        "models": {
            "modelA": {
                "coords": {
                    "component": {"data": ["Fe", "C"]},
                    "phase": {"data": ["LIQ", "FCC_A1"]},
                    "solidification_region": {"data": ["A", "B"]},
                    "gradient_component": {"data": ["Fe", "C"]},
                    "parameter": {"data": ["p1", "p2"]},
                },
                "attrs": {
                    "input_dict": {
                        "composition": {
                            "components": [
                                {"name": "Fe", "samples": [0.8]},
                                {"name": "C", "samples": [0.2]},
                            ]
                        }
                    }
                },
                "data_vars": {
                    "temperature": {"data": [[[1000, 1273, 1832]]]},
                    "phase_fraction": {"data": [[[[0.2, 0.8], [0.3, 0.7]]]]},
                    "temperature_by_phase_region": {
                        "data": [[[[1000, 1832], [900, 1800]]]]
                    },
                    "percent_solidified_molar_values": {"data": [[10, 30, 60, 90]]},
                    "system_density": {"data": [[7.9]]},
                },
            },
            "modelB": {
                "coords": {
                    "phase": {"data": ["FCC_A1"]},
                    # No 'component' — tests empty handling
                },
                "data_vars": {"temperature": {"data": [[[1200, 1400, 1600]]]}}
            },
        }
    }