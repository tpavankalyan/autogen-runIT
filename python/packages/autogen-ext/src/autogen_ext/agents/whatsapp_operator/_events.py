from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class WhatsappOperatorEvent:
    source: str
    message: str
    url: str
    action: str | None = None
    arguments: Dict[str, Any] | None = None
