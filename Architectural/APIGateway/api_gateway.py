from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import httpx

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderRequest(BaseModel):
    user_id: int
    items: List[OrderItem]
    payment_token: str

class ApiGateway:
    def __init__(self):
        # Simplified service URLs
        self.services = {
            'product': 'http://product-service:8001',
            'order': 'http://order-service:8002',
            'payment': 'http://payment-service:8003'
        }

    async def process_order(self, order: OrderRequest) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                # 1. Check product availability
                for item in order.items:
                    response = await client.get(
                        f"{self.services['product']}/products/{item.product_id}"
                    )
                    product = response.json()
                    if product['stock'] < item.quantity:
                        raise HTTPException(
                            status_code=400, 
                            detail=f"Product {item.product_id} out of stock"
                        )

                # 2. Process payment
                payment_response = await client.post(
                    f"{self.services['payment']}/process",
                    json={'payment_token': order.payment_token}
                )
                if payment_response.status_code != 200:
                    raise HTTPException(
                        status_code=400, 
                        detail="Payment failed"
                    )

                # 3. Update product quantities
                for item in order.items:
                    await client.put(
                        f"{self.services['product']}/products/{item.product_id}",
                        json={'reduce_stock': item.quantity}
                    )

                # 4. Create order
                order_response = await client.post(
                    f"{self.services['order']}/orders",
                    json=order.dict()
                )
                
                return order_response.json()

            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500, 
                    detail="Order processing failed"
                )

app = FastAPI()
gateway = ApiGateway()

@app.post("/orders")
async def create_order(order: OrderRequest):
    return await gateway.process_order(order)