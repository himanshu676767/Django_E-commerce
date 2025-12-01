from ecommerce_project.db.mongo import get_db

def get_user_count():
	db = get_db()
	return db.users.count_documents({})

def get_orders_count():
	db = get_db()
	return db.orders.count_documents({})

def get_high_selling_product():
	db = get_db()
	pipeline = [
		{"$unwind": "$products"},
		{"$group": {"_id": "$products.product_id", "total_sold": {"$sum": "$products.quantity"}}},
		{"$sort": {"total_sold": -1}},
		{"$limit": 1}
	]
	result = list(db.orders.aggregate(pipeline))
	if not result:
		return None

	product = db.products.find_one({"_id": result[0]["_id"]})
	return {
		"product_name": product["name"],
		"units_sold": result[0]["total_sold"]
	}
