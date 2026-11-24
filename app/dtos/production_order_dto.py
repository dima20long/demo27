"""DTO для заказов на производство."""
from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class ProductionOrderItemDTO:
    """DTO для позиции заказа на производство."""
    order_item_id: str
    production_order_id: str
    product_id: str
    quantity: float
    completed_quantity: float
    unit_price: float
    total_price: float

    @classmethod
    def from_model(cls, item) -> "ProductionOrderItemDTO":
        """Создать DTO из модели."""
        return cls(
            order_item_id=str(item.order_item_id),
            production_order_id=str(item.production_order_id),
            product_id=str(item.product_id),
            quantity=float(item.quantity),
            completed_quantity=float(item.completed_quantity),
            unit_price=float(item.unit_price),
            total_price=float(item.total_price),
        )

    def to_dict(self) -> dict:
        """Конвертировать в словарь."""
        return asdict(self)


@dataclass
class ProductionOrderDTO:
    """DTO для заказа на производство."""
    order_id: str
    order_number: str
    order_date: Optional[str] = None
    subdivision: Optional[str] = None
    client_id: Optional[str] = None
    sales_order_id: Optional[str] = None
    total_amount: float = 0.0
    status: str = "Новый"
    created_at: Optional[str] = None
    items: Optional[List[ProductionOrderItemDTO]] = None

    @classmethod
    def from_model(cls, order) -> "ProductionOrderDTO":
        """Создать DTO из модели."""
        items = [ProductionOrderItemDTO.from_model(item) for item in order.items] if order.items else None
        return cls(
            order_id=str(order.order_id),
            order_number=order.order_number,
            order_date=order.order_date.isoformat() if order.order_date else None,
            subdivision=order.subdivision,
            client_id=str(order.client_id) if order.client_id else None,
            sales_order_id=str(order.sales_order_id) if order.sales_order_id else None,
            total_amount=float(order.total_amount) if order.total_amount else 0,
            status=order.status,
            created_at=order.created_at.isoformat() if order.created_at else None,
            items=items,
        )

    def to_dict(self) -> dict:
        """Конвертировать в словарь."""
        return asdict(self)
