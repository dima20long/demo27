"""Репозиторий для заказов на производство."""
from app.repositories.base_repository import BaseRepository
from app.models import ProductionOrder


class ProductionOrderRepository(BaseRepository):
    """Репозиторий заказов на производство."""

    def __init__(self):
        super().__init__(ProductionOrder)
