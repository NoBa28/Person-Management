from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from datetime import date

from dto.AddressUpdate import AddressUpdate


@dataclass
class PersonUpdate:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    mail: Optional[str] = None
    address: Optional[AddressUpdate] = None
    person_id: Optional[int] = None
