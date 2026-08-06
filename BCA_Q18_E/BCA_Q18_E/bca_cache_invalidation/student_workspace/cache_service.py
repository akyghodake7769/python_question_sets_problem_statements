# Cache Service
def update_product_price(redis_client, product_id, new_price):
    db_update(product_id, new_price)
    redis_client.delete(f'product:{product_id}')
