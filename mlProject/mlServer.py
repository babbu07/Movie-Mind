from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the picked database and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


# Title finding
myDf = movies["title"]
model = pickle.load(open("titleFindingModel.pkl", "rb"))
embedding = pickle.load(open("embeddingTitle.pkl", "rb"))

def recommed(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]
    return_list=[]
    for i in movies_list:
        return_list.append(int(movies.iloc[i[0]].movie_id))
    return return_list

def getThreeTitle(name):
    nameEncode = model.encode(name)
    similarityTitle = sorted(list(enumerate(model.similarity(embedding, nameEncode))),reverse=True, key=lambda x: x[1])[0:3]
    return myDf.iloc[similarityTitle[0][0]]
    # rList = []
    # for i in similarityTitle:
    #     rList.append(myDf.iloc[i[0]])
    # print(rList)
    
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # get the json data from request
        data = request.get_json()
        
        # Extract the string input
        input_movie = data.get("input", "")
        
        # Title matched to the best one
        input_movie = getThreeTitle(input_movie)
        
        # Ensure input is a string
        if not isinstance(input_movie, str):
            return jsonify({"error": "Input must be a string"})
        
        # Call the function
        result = recommed(input_movie)
        
        return jsonify({"result": result})
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__== "__main__":
    app.run(debug=True)