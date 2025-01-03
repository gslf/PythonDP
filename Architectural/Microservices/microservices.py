# product_service.py
from dataclasses import dataclass
from typing import Dict, List, Optional
from fastapi import FastAPI
import httpx
import uvicorn

@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int

class ProductService:
    def __init__(self):
        self.products: Dict[int, Product] = {}
        self.app = FastAPI()
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.get("/products/{product_id}")
        async def get_product(product_id: int) -> Optional[Product]:
            return self.products.get(product_id)
        
        @self.app.post("/products/update_stock/{product_id}")
        async def update_stock(product_id: int, quantity: int) -> bool:
            if product_id in self.products:
                self.products[product_id].stock -= quantity
                return True
            return False

# order_service.py
@dataclass
class Order:
    id: int
    user_id: int
    products: List[int]
    total: float
    status: str

class OrderService:
    def __init__(self):
        self.orders: Dict[int, Order] = {}
        self.app = FastAPI()
        self.product_service_url = "http://product-service:8000"
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.post("/orders/create")
        async def create_order(user_id: int, product_ids: List[int]) -> Optional[Order]:
            # Create new order
            async with httpx.AsyncClient() as client:
                total = 0
                # Check products availability with Product Service
                for product_id in product_ids:
                    response = await client.get(
                        f"{self.product_service_url}/products/{product_id}"
                    )
                    if response.status_code != 200:
                        return None
                    product = response.json()
                    total += product["price"]
                    
                    # Update stock
                    await client.post(
                        f"{self.product_service_url}/products/update_stock/{product_id}",
                        params={"quantity": 1}
                    )
                
                # Create and store order
                order = Order(
                    id=len(self.orders) + 1,
                    user_id=user_id,
                    products=product_ids,
                    total=total,
                    status="created"
                )
                self.orders[order.id] = order
                return order

# Run services
if __name__ == "__main__":
    
    
    # Run each service on different ports
    product_service = ProductService()
    order_service = OrderService()
    
    # WARNING: In this example, the services are on the same thread, 
    # so they do not run concurrently. The second one starts only 
    # when the first has finished. In practice, these would run on 
    # different processes/machines.
    uvicorn.run(product_service.app, host="0.0.0.0", port=8000)
    uvicorn.run(order_service.app, host="0.0.0.0", port=8001)