import pandas as pd

def get_recommendations(id):    
    orders = pd.read_excel("data/Ordershop.xlsx")
    
    orders_for_shop = orders[orders.shop_id == id].order_id.unique();
    
    relevant_orders = orders[orders.order_id.isin(orders_for_shop)]
    
    accompanying_shops_by_order = relevant_orders[relevant_orders.shop_id != id]
    num_instance_by_accompanying_shop = accompanying_shops_by_order.groupby("shop_id")["shop_id"].count().reset_index(name="instances")
    
    num_orders_for_shop = orders_for_shop.size
    shop_instances = pd.DataFrame(num_instance_by_accompanying_shop)
    shop_instances["frequency"] = shop_instances["instances"]/num_orders_for_shop
    
    recommended_shops = pd.DataFrame(shop_instances.sort_values("frequency", ascending=False).head(3))
    
    shops = pd.read_excel("data/Shop.xlsx")
    recommended_shops = pd.merge(recommended_shops, shops, on="shop_id")
    print(recommended_shops)
    
    return recommended_shops.to_json(orient="table")
    