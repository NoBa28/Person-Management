from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressUpdate:
    street: Optional[str] = None
    house_num: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    address_id: Optional[int] = None
