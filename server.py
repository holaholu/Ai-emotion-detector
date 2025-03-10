"""This server uses fask to the deploy the Emotion Dection function"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector
app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emo_detector():
    """This route processes the text to be analyzer and returns the output from the AI"""
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')
    # Pass the text to the emotion_detector function and store the response
    response = emotion_detector(text_to_analyze)
    dominant= response["dominant_emotion"]
    # Check if the label is None, indicating an error or invalid input
    if dominant is None:
        return "Invalid input! Try again."

    # Return a formatted string with the customer specifications
    #store and remove the dominant_emotion
    del response['dominant_emotion']
    #create a string text for all emotions and values
    keys = list(response.keys())
    new_data = ", ".join(f"'{key}': {value}" for key, value in response.items())
    if len(keys) > 1:
        new_data = new_data.replace(f", '{keys[-1]}': {response[keys[-1]]}",
        f" and '{keys[-1]}': {response[keys[-1]]}")
    #Add the customer front text and dominat emotion
    text1="For the given statement, the system response is "
    return_data = text1 +  new_data + ". The dominant emotion is  " + str(dominant)+"."
    return return_data

@app.route("/")
def render_index_page():
    """This function renders the index page of the application"""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
