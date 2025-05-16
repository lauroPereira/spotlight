from datetime import datetime
from typing import List, Any, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

class Complaint(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "date": "2025-05-16T12:00:00",
                "category": "COBRANÇA INDEVIDA",
                "description": "Cobrança indevida no plano pré-pago.",
                "razao_social": "CLARO S/A"
            }
        }
    )
    date: datetime
    category: str
    description: str
    raw_brand: str = Field(..., alias="razao_social")

    # strip, uppercase e não vazio em um só
    @field_validator("category", "description", "raw_brand", mode="before")
    @classmethod
    def strip_and_upper(cls, v: str) -> str:
        s = v.strip().upper()
        if not s:
            raise ValueError("value cannot be empty")
        return s

    # parse ISO strings e validar futuro
    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime:
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except Exception:
                raise ValueError("invalid date format, must be ISO")
        return v

    @field_validator("date")
    @classmethod
    def date_not_future(cls, v: datetime) -> datetime:
        if v > datetime.utcnow():
            raise ValueError("date cannot be in the future")
        return v


class PluginResult(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "plugin": "ANATEL",
                "company": "CLARO",
                "fetched_at": "2025-05-16T12:30:00",
                "total_raw": 1523456,
                "complaints": [{
                    "date": "2025-05-16T12:00:00",
                    "category": "COBRANÇA INDEVIDA",
                    "description": "Cobrança indevida no plano pré-pago.",
                    "razao_social": "CLARO S/A"
                },
                {
                    "date": "2025-05-16T12:00:00",
                    "category": "FALTA DE SINAL",
                    "description": "Sinal fraco na região central.",
                    "razao_social": "CLARO S/A"
                }]
            }
        }
    )
    plugin: str
    company: str
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    total_raw: int
    complaints: List[Complaint]

    # strip+upper e não vazio
    @field_validator("plugin", "company", mode="before")
    @classmethod
    def strip_and_upper_meta(cls, v: str) -> str:
        s = v.strip().upper()
        if not s:
            raise ValueError("plugin/company cannot be empty")
        return s

    @field_validator("total_raw")
    @classmethod
    def must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("total_raw must be non-negative")
        return v

    @field_validator("fetched_at", mode="before")
    @classmethod
    def parse_fetched_at(cls, v: Any) -> datetime:
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except Exception:
                raise ValueError("invalid fetched_at format, must be ISO")
        return v

    @field_validator("fetched_at")
    @classmethod
    def fetched_not_future(cls, v: datetime) -> datetime:
        if v > datetime.utcnow():
            raise ValueError("fetched_at cannot be in the future")
        return v

    @model_validator(mode="before")
    @classmethod
    def ensure_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # permite passar um único dict em "complaints"
        comp = data.get("complaints")
        if isinstance(comp, dict):
            data["complaints"] = [comp]
        elif not isinstance(comp, list):
            raise ValueError("complaints must be a list or a dict")
        return data

# Note: Removed non_empty_complaints validator to allow empty complaints list
