"""
Tests for Pydantic models.
"""
import pytest
from app.models import TelemetryParams


def test_telemetry_params_basic():
    """Test basic parameter validation."""
    params = TelemetryParams(v="4.16.1", guid="test-guid")
    assert params.v == "4.16.1"
    assert params.guid == "test-guid"


def test_telemetry_params_all_fields():
    """Test with all documented parameters from analysis."""
    params = TelemetryParams(
        # Version & Environment
        v="4.16.1-20904e45",
        env="prod",
        os="ubuntu-24.04",
        kv="linux-6.12.54-linuxkit",
        # License Information
        lic="bGljZW5zZS1mcmVlLTQuMTYuMS0yMDkwNGU0NQ==",
        licls="free",
        # Instance Identity
        guid="b117a3cd-37e2-43a8-bb5b-a5d5eb5a5fec",
        # Deployment Mode
        p="s",
        dm="s",
        it="c",
        # Feature Usage Statistics
        fc_giv="9",
        fc_h7h="4",
        fc_EYq="15",
        fc_qiD="7",
        fc_uOA="2",
        fc_rTA="1",
        fc_GZs="1",
        fc_ffg="1",
        fc_nUz="2",
        # Lookup Statistics
        lk_max="23156",
        lk_csv="3",
        # Pipeline/Processing Metrics
        pp="0",
        pp_ie="0",
        pp_ib="0",
        pp_ce="0",
        pp_cb="0",
        pp_oe="0",
        pp_ob="0",
        # Event Metrics
        mc="87",
        ib="0",
        ob="0",
        ie="0",
        oe="0",
        im="0",
        # Component Counts
        pc="9",
        dc="0",
        ic="19",
        qc="0",
        oc="2",
        sc="0",
        prc="0",
        rc="0",
        wpc="8",
        tpp="0",
        # Timestamps
        et="1770278291000",
        lt="1770278520000",
        # Feature Flags
        fs_r="f",
    )

    assert params.v == "4.16.1-20904e45"
    assert params.guid == "b117a3cd-37e2-43a8-bb5b-a5d5eb5a5fec"
    assert params.fc_giv == "9"
    assert params.lk_max == "23156"


def test_telemetry_params_all_optional():
    """Test that all parameters are optional."""
    params = TelemetryParams()
    assert params.v is None
    assert params.guid is None


def test_telemetry_params_extra_allowed():
    """Test that extra parameters are allowed (forward compatibility)."""
    params = TelemetryParams(
        v="4.16.1",
        unknown_param="some_value",
        future_feature="enabled"
    )
    assert params.v == "4.16.1"
    # Extra params should be accessible via dict
    assert "unknown_param" in params.model_dump()
