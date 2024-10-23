from flask import Flask, request, jsonify
import pickle

# Initialize the Flask application
application = Flask(__name__)

# Load the model and vectorizer
loaded_model = None
with open('basic_classifier.pkl', 'rb') as fid:
    loaded_model = pickle.load(fid)

vectorizer = None
with open('count_vectorizer.pkl', 'rb') as vd:
    vectorizer = pickle.load(vd)

# Route to handle predictions
@application.route('/', methods=['GET', 'POST'])
def predict():
    prediction = ""
    if request.method == 'POST':
        # Get the user input from the form
        user_input = request.form['text']
        
        # Predict using the loaded model
        prediction = loaded_model.predict(vectorizer.transform([user_input]))[0]

    # Return the form and display the prediction if available
    return '''
        <form method="post">
            <label for="text">Enter text to classify:</label><br>
            <textarea name="text" rows="4" cols="50" required></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
        <br>
        <div>Prediction: {}</div>
    '''.format(prediction)

if __name__ == "__main__":
    application.run(port=8000, debug=True)
