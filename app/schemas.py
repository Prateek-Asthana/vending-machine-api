from pydantic import BaseModel, Field, field_validator


# --- Slot ---
# class SlotCreate(BaseModel):
#     code: str
#     capacity: int = Field(..., gt=0)

class SlotCreate(BaseModel):
    # code: str
    # capacity: int = Field(..., gt=0)

    # @field_validator("code")
    # @classmethod
    # def trim_slot_code(cls, v: str) -> str:
    #     # bug 2 FIX: remove leading/trailing spaces
    #     v = v.strip()

    #     if not v:
    #         raise ValueError("Slot code cannot be empty or spaces only")

    #     return v

    # code: str
    # capacity: int = Field(..., gt=0, le=100)

    # @field_validator("code")
    # @classmethod
    # def normalize_slot_code(cls, v: str) -> str:
    #     # 🔥 Bug 2 fix: trim spaces
    #     v = v.strip()

    #     # 🔥 Bug 1 fix: make case-insensitive
    #     v = v.upper()

    #     if not v:
    #         raise ValueError("Slot code cannot be empty")

    #     return v


    code: str
    capacity: int = Field(
        ...,
        gt=0,
        le=100,   # 🔥 BUG 3 FIX: upper limit
        description="Slot capacity must be between 1 and 100"
    )

    @field_validator("code")
    @classmethod
    def normalize_slot_code(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Slot code cannot be empty")
        return v


class SlotResponse(BaseModel):
    id: str
    code: str
    capacity: int
    current_item_count: int

    model_config = {"from_attributes": True}


# --- Item ---
class ItemCreate(BaseModel):
    name: str
    price: int = Field(..., ge=0)  # Allow any non-negative price
    quantity: int = Field(..., gt=0)


class ItemBulkEntry(BaseModel):
    name: str
    price: int = Field(..., ge=0)  # Allow any non-negative price
    quantity: int = Field(..., gt=0)


class ItemBulkRequest(BaseModel):
    items: list[ItemBulkEntry]


class ItemResponse(BaseModel):
    id: str
    name: str
    price: int
    quantity: int

    model_config = {"from_attributes": True}


class ItemDetailResponse(ItemResponse):
    slot_id: str


class ItemPriceUpdate(BaseModel):
    price: int = Field(..., gt=0)


# --- Slot full view ---
class SlotFullViewItem(BaseModel):
    id: str
    name: str
    price: int
    quantity: int

    model_config = {"from_attributes": True}


class SlotFullView(BaseModel):
    id: str
    code: str
    capacity: int
    items: list[SlotFullViewItem]

    model_config = {"from_attributes": True}


# --- Purchase ---
class PurchaseRequest(BaseModel):
    item_id: str
    cash_inserted: int = Field(..., ge=0)


class PurchaseResponse(BaseModel):
    item: str
    price: int
    cash_inserted: int
    change_returned: int
    remaining_quantity: int
    message: str


class InsufficientCashError(BaseModel):
    error: str = "Insufficient cash"
    required: int
    inserted: int


class OutOfStockError(BaseModel):
    error: str = "Item out of stock"


# --- Generic message responses ---
class MessageResponse(BaseModel):
    message: str


class BulkAddResponse(BaseModel):
    message: str = "Items added successfully"
    added_count: int


class BulkRemoveBody(BaseModel):
    item_ids: list[str] | None = None


# --- Change breakdown (bonus) ---
class ChangeBreakdownResponse(BaseModel):
    change: int
    denominations: dict[str, int]
