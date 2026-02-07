"""
Pydantic models for telemetry data structures.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TelemetryParams(BaseModel):
    """
    Query parameters for Cribl telemetry endpoint.

    All parameters are Optional[str] since they come from query strings.
    Based on analysis from docs/analysis/telemetry-capture-20260205.md

    Note: Using aliases to map from query param format (fc.giv) to Python-safe names (fc_giv)
    """

    # Version & Environment
    v: Optional[str] = Field(None, description="Cribl version", alias="v")
    env: Optional[str] = Field(None, description="Environment (prod/dev)")
    os: Optional[str] = Field(None, description="Operating system")
    kv: Optional[str] = Field(None, description="Kernel version")

    # License Information
    lic: Optional[str] = Field(None, description="Base64-encoded license info")
    licls: Optional[str] = Field(None, description="License class")

    # Instance Identity
    guid: Optional[str] = Field(None, description="Unique instance identifier")

    # Deployment Mode
    p: Optional[str] = Field(None, description="Product/platform type")
    dm: Optional[str] = Field(None, description="Deployment mode")
    it: Optional[str] = Field(None, description="Instance type")

    # Feature Usage Statistics (fc.* prefix)
    fc_giv: Optional[str] = Field(None, description="Feature usage counter", alias="fc.giv")
    fc_h7h: Optional[str] = Field(None, description="Feature usage counter", alias="fc.h7h")
    fc_EYq: Optional[str] = Field(None, description="Feature usage counter", alias="fc.EYq")
    fc_qiD: Optional[str] = Field(None, description="Feature usage counter", alias="fc.qiD")
    fc_uOA: Optional[str] = Field(None, description="Feature usage counter", alias="fc.uOA")
    fc_rTA: Optional[str] = Field(None, description="Feature usage counter", alias="fc.rTA")
    fc_GZs: Optional[str] = Field(None, description="Feature usage counter", alias="fc.GZs")
    fc_ffg: Optional[str] = Field(None, description="Feature usage counter", alias="fc.ffg")
    fc_nUz: Optional[str] = Field(None, description="Feature usage counter", alias="fc.nUz")

    # Lookup Statistics (lk.* prefix)
    lk_max: Optional[str] = Field(None, description="Max lookup entries", alias="lk.max")
    lk_csv: Optional[str] = Field(None, description="CSV lookups count", alias="lk.csv")

    # Pipeline/Processing Metrics (pp.* prefix)
    pp: Optional[str] = Field(None, description="Total pipeline processors")
    pp_ie: Optional[str] = Field(None, description="Input events", alias="pp.ie")
    pp_ib: Optional[str] = Field(None, description="Input bytes", alias="pp.ib")
    pp_ce: Optional[str] = Field(None, description="Computed events", alias="pp.ce")
    pp_cb: Optional[str] = Field(None, description="Computed bytes", alias="pp.cb")
    pp_oe: Optional[str] = Field(None, description="Output events", alias="pp.oe")
    pp_ob: Optional[str] = Field(None, description="Output bytes", alias="pp.ob")

    # Event Metrics
    mc: Optional[str] = Field(None, description="Metric count")
    ib: Optional[str] = Field(None, description="Input bytes")
    ob: Optional[str] = Field(None, description="Output bytes")
    ie: Optional[str] = Field(None, description="Input events")
    oe: Optional[str] = Field(None, description="Output events")
    im: Optional[str] = Field(None, description="Input messages")

    # Component Counts
    pc: Optional[str] = Field(None, description="Pipeline count")
    dc: Optional[str] = Field(None, description="Destination count")
    ic: Optional[str] = Field(None, description="Input count")
    qc: Optional[str] = Field(None, description="Queue count")
    oc: Optional[str] = Field(None, description="Output count")
    sc: Optional[str] = Field(None, description="Source count")
    prc: Optional[str] = Field(None, description="Processor count")
    rc: Optional[str] = Field(None, description="Route count")
    wpc: Optional[str] = Field(None, description="Worker process count")
    tpp: Optional[str] = Field(None, description="Total pipeline processors")

    # Timestamps
    et: Optional[str] = Field(None, description="Epoch time (start time)")
    lt: Optional[str] = Field(None, description="Last time (last event time)")

    # Feature Flags
    fs_r: Optional[str] = Field(None, description="Feature state", alias="fs.r")

    model_config = ConfigDict(
        extra="allow",  # Allow extra params for forward compatibility
        populate_by_name=True,  # Allow using both alias and field name
    )
