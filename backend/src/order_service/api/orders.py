from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.order_service import OrderService
from src.dependencies import get_order_service
from src.domain.entities.order import Order
from src.domain.value_objects.order_status import OrderStatus
from src.presentation.dto import OrderCreateRequest, OrderResponse, OrderUpdateRequest

order_router = APIRouter(
    prefix="/api/orders",
    tags=["orders"],
)


@order_router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreateRequest,
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Create a new order"""
    try:
        # Convert status string to OrderStatus enum
        status_enum = (
            OrderStatus(order_data.status)
            if order_data.status
            else OrderStatus.MODERATION
        )

        order = Order(
            title=order_data.title,
            description=order_data.description,
            author_id=order_data.author_id,
            status=status_enum,
            primary_responses=order_data.primary_responses,
            skills=[],  # TODO: Convert skill strings to Skill objects
        )

        created_order = await order_service.create_order(order)
        return OrderResponse(order=created_order)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create order: {e}",
        )


@order_router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Get order by UUID"""
    order = await order_service.get_order_by_uuid(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return OrderResponse(order=order)


@order_router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: str,
    order_data: OrderUpdateRequest,
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Update order by ID"""
    # Get existing order first (outside try-catch to avoid catching 404)
    existing_order = await order_service.get_order_by_uuid(order_id)
    if existing_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    try:
        # Update fields if provided
        updated_order = Order(
            title=order_data.title
            if order_data.title is not None
            else existing_order.title,
            description=order_data.description
            if order_data.description is not None
            else existing_order.description,
            author_id=existing_order.author_id,
            status=OrderStatus(order_data.status)
            if order_data.status is not None
            else existing_order.status,
            primary_responses=order_data.primary_responses
            if order_data.primary_responses is not None
            else existing_order.primary_responses,
            skills=existing_order.skills,  # TODO: Handle skills update
        )

        updated_order = await order_service.update_order_by_uuid(
            order_id, updated_order
        )
        return OrderResponse(order=updated_order)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update order: {e}",
        )


@order_router.delete("/{order_id}", response_model=OrderResponse)
async def delete_order(
    order_id: str,
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Delete order by ID"""
    try:
        deleted_order = await order_service.delete_order_by_uuid(order_id)
        return OrderResponse(order=deleted_order)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete order: {e}",
        )
