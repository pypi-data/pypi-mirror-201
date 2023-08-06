#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class MessageActionGiftPremium(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``157``
        - ID: ``C83D6AEC``

    Parameters:
        currency (``str``):
            N/A

        amount (``int`` ``64-bit``):
            N/A

        months (``int`` ``32-bit``):
            N/A

        cryptoCurrency (``str``, *optional*):
            N/A

        cryptoAmount (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["currency", "amount", "months", "cryptoCurrency", "cryptoAmount"]

    ID = 0xc83d6aec
    QUALNAME = "types.MessageActionGiftPremium"

    def __init__(self, *, currency: str, amount: int, months: int, cryptoCurrency: Optional[str] = None, cryptoAmount: Optional[int] = None) -> None:
        self.currency = currency  # string
        self.amount = amount  # long
        self.months = months  # int
        self.cryptoCurrency = cryptoCurrency  # flags.0?string
        self.cryptoAmount = cryptoAmount  # flags.0?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionGiftPremium":
        
        flags = Int.read(b)
        
        currency = String.read(b)
        
        amount = Long.read(b)
        
        months = Int.read(b)
        
        cryptoCurrency = String.read(b) if flags & (1 << 0) else None
        cryptoAmount = Long.read(b) if flags & (1 << 0) else None
        return MessageActionGiftPremium(currency=currency, amount=amount, months=months, cryptoCurrency=cryptoCurrency, cryptoAmount=cryptoAmount)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.cryptoCurrency is not None else 0
        flags |= (1 << 0) if self.cryptoAmount is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        b.write(Int(self.months))
        
        if self.cryptoCurrency is not None:
            b.write(String(self.cryptoCurrency))
        
        if self.cryptoAmount is not None:
            b.write(Long(self.cryptoAmount))
        
        return b.getvalue()
