from flask import Flask, render_template
from card_details_extracter import find_details
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

application = Flask(__name__)
 
application.config['SECRET_KEY'] = 'supersecretkey'
application.config['UPLOAD_FOLDER'] = 'img'
application.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG"]

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@application.route('/', methods=['GET',"POST"])
@application.route('/home', methods=['GET',"POST"])
def home():
    """home page"""
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),application.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        # Get the list of all files and directories
        path = "img"
        dir_list = os.listdir(path)
        details_file = path+'/'+dir_list[0]
        result = find_details(details_file)
        os.remove(details_file)
        print(result)

        return render_template('result.html', result=result)
    return render_template('index.html', form=form)


if __name__ == "__main__":
    application.run(debug=True, port=5123)