from fastapi import FastAPI

app = FastAPI(title="Product Service")


products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 55000
    },
    {
        "id": 2,
        "name": "Mouse",
        "price": 800
    }
]


@app.get("/")
def home():
    return {"message": "Product Service is running"}


@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {"message": "Product not found"}
