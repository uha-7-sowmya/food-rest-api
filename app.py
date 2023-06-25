from flask import Flask,request
from fooddb.MongoUtilis import  MongoDBConnection


mycoll =  MongoDBConnection('rocketRecipeDB','food-items','mongodb+srv://sowmya:<sowmya@10>@cluster0.djvqvtj.mongodb.net/?retryWrites=true&w=majority').create_connection()

app = Flask(__name__)


env = {
    'name' : 'rocket recipe microservice',
    'version': 'V1.0'
}

@app.route('/')
def greet():
    return f"{env['name']} is UP & RUNNING with version : {env['version']}"


@app.get('/api/food/<int:id>')
def get_food_item(id):
    if mycoll is not None:
        data = mycoll.find_one(id)
        return data
    return f'no items found'


@app.get('/api/food/')
def get_food_items():
    if mycoll is not None:
        data = mycoll.find()
        return data
    return f'no items found'

@app.post('/api/food/')
def save_food_item():
    if mycoll is not None:
        data = request.json
        response = mycoll.insert_one(data)
        return f' data inserted successfully :{response.acknowledged} {response.inserted_id}'
    return f'Service is not avaiable....'

@app.post('/api/foods/')
def save_food_items():
    if mycoll is not None:
        data = request.json
        response = mycoll.insert_many(data)
        return f' data inserted successfully : {response.acknowledged} {response.inserted_ids}'
    return f'Service is not avaiable....'

@app.put('/api/food/<int:id>')
def update_food_item(id):
    if mycoll is not None:
        data = request.json
        response= mycoll.update_one({'_id':id},{'$set':data})
        return f'data updated sucessfully'
    else:
        return f'no data updated'


@app.delete('/api/food/<int:id>')
def delete_food_item(id):
    if mycoll is not None:
        response=mycoll.delete_one(id)
        return f'data deleted and {response.status}'
    else:
        return f'no data deleted'

if __name__ == '__main__':
    # create db connection..
    app.run(debug=True)