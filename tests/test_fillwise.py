import pytest
import numpy as np
import pandas as pd
from fillwise.core import Fillwise


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Group": ["A", "B", "C"],
        "Count": [10, 20, 30]
    })


@pytest.fixture
def mask_path():
    return "tests/icon.png"


def test_fillwise_initialization(sample_df, mask_path):
    viz = Fillwise(sample_df, image_path=mask_path, fill_style="radial")
    assert viz.labels == ["A", "B", "C"]
    assert len(viz.percentages) == 3
    assert np.isclose(sum(viz.percentages), 1.0)


def test_invalid_fill_style(sample_df, mask_path):
    with pytest.raises(ValueError, match="Unsupported fill style"):
        Fillwise(sample_df, image_path=mask_path, fill_style="diagonal")


def test_missing_mask_path(sample_df):
    with pytest.raises(ValueError, match="mask_path must be provided"):
        Fillwise(sample_df, image_path=None)


def test_color_validation(sample_df, mask_path):
    with pytest.raises(ValueError, match="Not enough colors provided"):
        Fillwise(sample_df, image_path=mask_path, colors=["#FF0000"])


def test_render_output_shape(sample_df, mask_path):
    viz = Fillwise(sample_df, image_path=mask_path, fill_style="horizontal")
    image = viz.render()
    assert isinstance(image, np.ndarray)
    assert image.shape[2] == 4  # RGBA


def test_save_output(tmp_path, sample_df, mask_path):
    output_path = tmp_path / "output.png"
    viz = Fillwise(sample_df, image_path=mask_path, fill_style="vertical")
    viz.save(path=str(output_path))
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_show_method(monkeypatch, sample_df, mask_path):
    viz = Fillwise(sample_df, image_path=mask_path, fill_style="radial")

    # Mock PIL.Image.show
    class DummyImage:
        def show(self): return True

    monkeypatch.setattr("fillwise._utils.array_to_image",
                        lambda x: DummyImage())
    assert viz.show() is None  # Should not raise


def test_zero_counts(mask_path):
    df = pd.DataFrame({
        "Label": ["A", "B", "C"],
        "Count": [0, 0, 0]
    })
    with pytest.raises(ZeroDivisionError):
        Fillwise(df, image_path=mask_path)
