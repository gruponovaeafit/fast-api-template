from fastapi import APIRouter, HTTPException, Request, status
from slowapi.errors import RateLimitExceeded
from typing import List
import logging

# Configuration, models, methods and authentication modules imports
from app.api.config.db import get_items, add_item, find_item, update_item, delete_item
from app.api.config.limiter import limiter
from app.api.config.env import API_NAME
from app.api.models.models import ResponseError, ItemPatch, ItemCreate, Item
from app.api.auth.auth import auth_handler
from app.api.methods.methods import is_valid_objectid, convert_objectid_to_str

router = APIRouter()

# Log file name
log_filename = f"api_{API_NAME}.log"

# Configurate the logging level to catch all messages from DEBUG onwards
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    handlers=[logging.FileHandler(log_filename),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)

@router.post('/items/', 
             response_model=Item, 
             status_code=status.HTTP_201_CREATED, 
             tags=["CRUD"],
             responses={
                 500: {"model": ResponseError, "description": "Internal server error."},
                 429: {"model": ResponseError, "description": "Too many requests."}
             })
@limiter.limit("5/minute")
def create_item(item: ItemCreate, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Create a new item in the database.
    
    Args:
    - item (ItemCreate): Item to be created.
    
    Returns:
    - Item: Created item with its ID.
    """
    try:
        logger.info("Creating a new item.")
        item_dict = item.dict()
        item_dict["id"] = str(len(get_items()) + 1)  # Simple ID assignment
        add_item(item_dict)
        logger.info(f"Item with ID {item_dict['id']} successfully created.")
        return item_dict
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Error creating item: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating item.")

@router.get('/items/', 
            response_model=List[Item],
            tags=["CRUD"],
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."},
                404: {"model": ResponseError, "description": "No items found."},
            })
@limiter.limit("5/minute")
def list_items(request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Fetch all items from the database.
    
    Returns:
    - List[Item]: List of items.
    """
    try:
        logger.info("Fetching all items.")
        items = get_items()
        if not items:
            logger.warning("No items found.")
            raise HTTPException(status_code=404, detail="No items found.")
        logger.info("Items successfully fetched.")
        return items
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Error fetching items: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching items.")

@router.get('/items/{item_id}/',
            response_model=Item,
            tags=["CRUD"],
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."},
                404: {"model": ResponseError, "description": "Item not found."},
                400: {"model": ResponseError, "description": "Invalid item_id format."},
            })
@limiter.limit("5/minute")
def get_item(item_id: str, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Fetch a single item from the database using its ID.
    
    Args:
    - item_id (str): ID of the item to be fetched.
    
    Returns:
    - Item: Fetched item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        logger.info(f"Fetching item with ID {item_id}.")
        if not is_valid_objectid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item_id format.")
        item = find_item(item_id)
        if not item:
            logger.warning(f"No item found with ID {item_id}.")
            raise HTTPException(status_code=404, detail="Item not found.")
        logger.info(f"Item with ID {item_id} successfully fetched.")
        return item
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Error fetching item: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching item.")

@router.put('/items/{item_id}/', 
            response_model=Item,
            tags=["CRUD"],
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."},
                404: {"model": ResponseError, "description": "Item not found or not updated."},
                400: {"model": ResponseError, "description": "Invalid item_id format."},
            })
@limiter.limit("5/minute")
def update_item(item_id: str, item_update: ItemCreate, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Update an item in the database.
    
    Args:
    - item_id (str): ID of the item to be updated.
    - item_update (ItemCreate): New data for the item.
    
    Returns:
    - Item: Updated item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        logger.info(f"Updating item with ID {item_id}.")
        if not is_valid_objectid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item_id format.")
        updated_item = update_item(item_id, item_update.dict())
        if not updated_item:
            logger.warning(f"Failed to update item with ID {item_id}.")
            raise HTTPException(status_code=404, detail="Item not found or not updated.")
        logger.info(f"Item with ID {item_id} successfully updated.")
        return updated_item
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Error updating item: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating item.")

@router.patch('/items/{item_id}/',
              response_model=Item,
              tags=["CRUD"],
              responses={
                  500: {"model": ResponseError, "description": "Internal server error."},
                  429: {"model": ResponseError, "description": "Too many requests."},
                  404: {"model": ResponseError, "description": "Item not found or not patched."},
                  400: {"model": ResponseError, "description": "Invalid item_id format."},
              })
@limiter.limit("5/minute")
def patch_item(item_id: str, item_patch: ItemPatch, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Partially update an item in the database.
    
    Args:
    - item_id (str): ID of the item to be updated.
    - item_update (ItemCreate): New data for the item.
    
    Returns:
    - Item: Updated item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        logger.info(f"Partially updating item with ID {item_id}.")
        if not is_valid_objectid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item_id format.")
        updated_item = update_item(item_id, item_patch.dict())
        if not updated_item:
            logger.warning(f"Failed to patch item with ID {item_id}.")
            raise HTTPException(status_code=404, detail="Item not found or not patched.")
        logger.info(f"Item with ID {item_id} successfully patched.")
        return updated_item
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Error patching item: {str(e)}")
        raise HTTPException(status_code=500, detail="Error patching item.")

@router.delete('/items/{item_id}/',
               response_model=Item,
               tags=["CRUD"],
               responses={
                   500: {"model": ResponseError, "description": "Internal server error."},
                   429: {"model": ResponseError, "description": "Too many requests."},
                   404: {"model": ResponseError, "description": "Item not found or not deleted."},
                   400: {"model": ResponseError, "description": "Invalid item_id format."},
               })
@limiter.limit("5/minute")
def delete_item(item_id: str, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Delete an item from the database.
    
    Args:
    - item_id (str): ID of the item to be deleted.
    
    Returns:
    - Item: Deleted item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        logger.info(f"Deleting item with ID {item_id}.")
        if not is_valid_objectid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item_id format.")
        deleted_item = delete_item(item_id)
        if not deleted_item:
            logger.warning(f"Failed to delete item with ID {item_id}.")
            raise HTTPException(status_code=404, detail="Item not found or not deleted.")
        logger.info(f"Item with ID {item_id} successfully deleted.")
        return deleted_item
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Error deleting item: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting item.")
