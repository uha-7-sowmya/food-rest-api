from flask import Flask,request
from fooddb.MongoUtilis import  MongoDBConnection


mycoll =  MongoDBConnection('rocketRecipeDB','food-items','mongodb+srv://test:test123@cluster0.djvqvtj.mongodb.net/?retryWrites=true&w=majority').create_connection()

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
        if data :
           return data
        else:
           return  {}
    return f'service is not available,please try again'

@app.get('/api/foods/')
def get_food_items():
    if mycoll is not None:
        data = mycoll.find()
        if data:
            return [item for item in data]
        else:
            return []
    return f'service is not available,please try again'

@app.post('/api/food/')
def save_food_item():
    if mycoll is not None:
        data = request.json
        response = mycoll.insert_one(data)
        if response.acknowledged:
           return f' Data inserted successfully :  {response.inserted_id}'
        else:
           return f'Unable to insert data '
    return f'service is not available,please try again'

@app.post('/api/foods/')
def save_food_items():
    if mycoll is not None:
        data = request.json
        response = mycoll.insert_many(data)
        if response.acknowledged:
           return f' Data inserted successfully :  {response.inserted_ids}'
        else:
            return 'Unable to insert data '
    return f'service is not available,please try again'

@app.put('/api/food/<int:id>')
def update_food_item(id):
    if mycoll is not None:
        data = request.json
        response= mycoll.update_one({'_id':id},{'$set':data})
        if response.acknowledged:
           return f'Data updated sucessfully {id}'
        else:
            return f'Unable to update data of {id}'
    else:
        return f'service is not available,please try again'



@app.delete('/api/food/<int:id>')
def delete_food_item(id):
    if mycoll is not None:
        response=mycoll.delete_one({"_id":id})
        if response.acknowledged:
           return f'data deleted of {id} and it is {response.acknowledged}'        
        else:
           return f'Unable to delete data of {id}'
    else:
        return f'service is not available,please try again'

if __name__ == '__main__':
    # create db connection..
    app.run(debug=True)