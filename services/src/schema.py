"""Request bodies."""

from pydantic import BaseModel, Field, model_validator

from src.catalogue import COLOURS, PRODUCTS, Size, Status, Style


class OrderItemIn(BaseModel):
    style: Style
    colour: str
    size: Size
    quantity: int = Field(ge=1)
    note: str | None = Field(default=None, max_length=500)  # e.g. an alteration for this piece

    @model_validator(mode="after")
    def check_against_catalogue(self):
        product = PRODUCTS[self.style]
        if self.size not in product["sizes"]:
            raise ValueError(f"{self.style.value} is not available in size {self.size.value}")
        valid_colours = {c.value for c in COLOURS[product["fabric"]]}
        if self.colour not in valid_colours:
            raise ValueError(f"{self.colour} is not a {product['fabric'].value} colour")
        return self


class CreateOrderIn(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    items: list[OrderItemIn] = Field(min_length=1)
    notes: str | None = None


class UpdateStatusIn(BaseModel):
    status: Status
