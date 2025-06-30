from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from forms.forms import UploadForm

# Flask app setup
app = Flask(__name__,template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Load trained model
model = load_model('GrainPalette_Model.h5')

# Define class names (ensure it matches your training class order)
class_names = ['Arborio', 'Basmati', 'Ipsala', 'Jasmine', 'Karacadag']

def model_predict(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor = img_tensor / 255.0

    prediction = model.predict(img_tensor)
    class_index = np.argmax(prediction)
    class_name = class_names[class_index]
    confidence = float(np.max(prediction))

    return class_name, confidence

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/predict',methods=['GET','POST'])
def predict():
    form = UploadForm()
    if form.validate_on_submit():
        img_file = form.image.data
        filename = secure_filename(img_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img_file.save(file_path)

        predicted_class, confidence = model_predict(file_path)

        return render_template('result.html',
                               image_url=file_path,
                               predicted_class=predicted_class,
                               confidence=round(confidence * 100, 2))

    return render_template('predict.html', form=form)

@app.route('/details')
def details():
    return render_template('details.html')

if __name__ == '__main__':
    app.run(debug=True)
