
import importlib, pytest

@pytest.mark.skipif(not importlib.util.find_spec("app.main"), reason="app.main not found")
def test_fastapi_app_importable():
    mod = importlib.import_module("app.main")
    assert hasattr(mod, "app"), "FastAPI app not exported as `app`"
