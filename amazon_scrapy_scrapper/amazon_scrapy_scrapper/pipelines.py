import pymongo


class AmazonScrapyScrapperPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient("mongodb+srv://akash:8jNYW8eVQCHORH6M@cluster0.k8zrx.mongodb.net/product?retryWrites=true&w=majority")

        # creating database
        db = self.conn['amazonDB']
        # creating collection
        self.collection = db['products']

    def process_item(self, item, spider):

        """
            method stores the data in db
            params:
                self (class instance)
                item (list): data scraped
            return:
                item (list)
        """
        
        for i in range(0,40):
            try:
                name = item['detail'][i] if item['detail'] != None else ''
                price = item['price'][i] if item['price'] != None else ''
                image = item['image'][i] if item['image'] != None else ''
                rating = item['rating'][i] if item['rating'] != None else ''
                
                self.collection.insert({
                'name': name,
                # 'product_image': item['product_image'][i],
                'image': image,
                'price': price,
                'rating': rating,
                # 'product_rating': item['product_rating'][i],
                'type': item['type']
                })
            except IndexError:
                pass
        return item