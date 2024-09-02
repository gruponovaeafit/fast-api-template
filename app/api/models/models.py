from typing import Optional
from pydantic import BaseModel

# Define your data models and schemas here
# For now, using generic examples

class ItemPatch(BaseModel):
    """
    Data model for partially updating an existing item.
    
    This model is used when an existing item is being updated with partial data. By providing only the fields 
    that need updating, the model ensures that unnecessary changes are not made to the item in the database.
    """
    name: Optional[str] = None
    description: Optional[str] = None

class ItemCreate(BaseModel):
    """
    Data model for creating a new item.
    
    This model is used when a new item is being created and doesn't have an ID yet. By separating the creation model
    from the general item model, it ensures that the ID is not provided or altered during the creation process.
    """
    name: str
    description: str

class Item(ItemCreate):
    """
    Data model for an existing item.
    
    This model extends the ItemCreate model by including an ID attribute. It's used when an item is being 
    fetched, updated, or deleted. The separation ensures that the ID is always present for existing items,
    making it clear when an item is new (without an ID) versus when it's an existing item (with an ID).
    """
    id: str

class ResponseError(BaseModel):
    """
    Data model for API error responses.
    
    Whenever the API encounters an error, be it a user-made error, a server error, or any other type of error,
    it will respond with this model. Having a standardized error response format ensures that clients can
    easily understand and handle errors consistently. The `detail` attribute provides a descriptive message 
    about the specific error, aiding in debugging and issue resolution.
    """
    detail: str