from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import zipfile
import os
import cv2
import subprocess
import pyrebase

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
# Create the 'uploads' directory if it doesn't exist
uploads_dir = os.path.join(os.getcwd(), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Add your own details
config = {
  "apiKey":"Your api key",
  "authDomain": "Your authDomain",
  "databaseURL": "Your databaseURL",
  "storageBucket": "Your storageBucket"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}



def zip_files(folder_path, file_paths, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_paths:
            file_path = os.path.join(folder_path, file)
            zipf.write(file_path, os.path.basename(file_path))
    
    # Move the zip file to the uploads folder
    new_zip_path = os.path.join(folder_path, zip_name)
    if os.path.exists(new_zip_path):
        os.remove(new_zip_path)  # Remove the existing zip file if exists
    os.rename(zip_name, new_zip_path)

@app.route('/')

@app.route('/home')
def home_page():
    if person["is_logged_in"] == True:
        return render_template("home_page2.html", email = person["email"], name = person["name"])
    else:
        return render_template('home_page.html')

@app.route('/add_watermark')
def add_page():
    if person["is_logged_in"] == True:
        return render_template("add_page.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

@app.route('/check_watermark')
def check_page():
    if person["is_logged_in"] == True:
        return render_template("check_page.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

@app.route('/how_to_use')
def howtouse_page():
    if person["is_logged_in"] == True:
        return render_template("howtouse_page2.html", email = person["email"], name = person["name"])
    else:
        return render_template('howtouse_page.html')

@app.route('/uploads', methods=['POST'])
def uploads():
    # ดึงข้อมูลจากแบบฟอร์ม
    uploaded_files = request.files.getlist('fileInput')
    text_input = request.form['textInput']
    img_watermark_list = []
    result_image_list2 = []
    img_has_watermark_list = []
    message_warning = None
    message_warning2 = None
    if uploaded_files and text_input:
        for file in uploaded_files:
            #print(f'ไฟล์ {file.filename} ถูกบันทึกเรียบร้อย')
            filename_without_spaces = file.filename.replace(" ", "")
            # บันทึกไฟล์ที่ถูกอัปโหลด
            file.save(os.path.join(uploads_dir,filename_without_spaces))
            file_split = filename_without_spaces.split('.')[0]
            cmd_command = ("python ./invisible-watermark -v -a encode -t bytes -m dwtDct -w {} -o ./uploads/{}_wm.png ./uploads/{}".format(text_input, file_split, filename_without_spaces))
            result = subprocess.run(cmd_command, shell=True, capture_output=True, text=True)
            filename1 = "{}_wm.png".format(file_split)
            img_watermark_list.append(filename1)

            length_watermark = len(text_input) * 8
            cmd_command2 = ("python ./invisible-watermark -v -a decode -t bytes -m dwtDct -l {} ./uploads/{}".format(length_watermark, filename1))
            result2 = subprocess.run(cmd_command2, shell=True, capture_output=True, text=True)
            # แยก output ตามเครื่องหมาย newline
            output_lines2 = result2.stdout.split('\n')
            #print(output_lines2)
            #print(result_image_list2)
            for i in range(0, 1):
                try:
                    if output_lines2[1] == text_input:
                        result_image = "Successfully Inserted"
                        img_has_watermark_list.append(filename1)
                        result_image_list2.append(result_image)
                        print("ไฟล์ : {} |ข้อความที่ป้อน : {} |ผลลัพธ์ : {}".format(file.filename, result_image, text_input))
                    else :
                        result_image = "Failed to insert"
                        result_image_list2.append(result_image)
                        message_warning = "##  If ''Failed to insert'' you can try reducing the number of words.  ##"
                        message_warning2 = "Watermarks do not work well with a homogeneous background color."
                        print("ไฟล์ : {} |ข้อความที่ป้อน : {} |ผลลัพธ์ : {}".format(file.filename, text_input, result_image))
                except:
                    pass
        len_image = len(img_watermark_list)
            
        if len(img_watermark_list) == 1:
            print(img_watermark_list, "image have 1")
            # ส่งกลับไปยังหน้าแรก
            return render_template('download_page.html', email = person["email"], name = person["name"], img_watermark_list = img_watermark_list, file_load = filename1, len_image = len_image, result_image_list2 = result_image_list2, message_warning=message_warning, message_warning2=message_warning2)
        elif len(img_watermark_list) > 1:
            print(img_watermark_list)
            file_paths = img_has_watermark_list
            zip_name = 'images.zip'
            zip_files('uploads', file_paths, zip_name)
            # ส่งกลับไปยังหน้าแรก
            return render_template('download_page.html', email = person["email"], name = person["name"], img_watermark_list = img_watermark_list, file_load = zip_name, len_image = len_image, result_image_list2 = result_image_list2, message_warning=message_warning, message_warning2=message_warning2)
    else:
        if person["is_logged_in"] == True:
            return render_template("add_page.html", email = person["email"], name = person["name"])
        else:
            return redirect(url_for('login'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/check', methods=['POST'])
def check():
    # ดึงข้อมูลจากแบบฟอร์ม
    uploaded_files2 = request.files.getlist('fileInput2')
    text_input2 = request.form['textInput2']
    img_watermark_list2 = []
    result_image_list = []
    if uploaded_files2 and text_input2:
        for file in uploaded_files2:
            print(file.filename)
            img_watermark_list2.append(file.filename)
            file.save(os.path.join(uploads_dir,file.filename))
            print(f'ไฟล์ {file.filename} ถูกบันทึกเรียบร้อย')
            length_watermark = len(text_input2) * 8
            cmd_command = ("python ./invisible-watermark -v -a decode -t bytes -m dwtDct -l {} ./uploads/{}".format(length_watermark, file.filename))
            result = subprocess.run(cmd_command, shell=True, capture_output=True, text=True)
            # แยก output ตามเครื่องหมาย newline
            output_lines = result.stdout.split('\n')
            print(output_lines)
            for i in range(0, 1):
                try:
                    if output_lines[1] == text_input2:
                        result_image = "Watermark detected (Owner)"
                        result_image_list.append(result_image)
                        print(file.filename, result_image)
                    else :
                        result_image = "Not found"
                        result_image_list.append(result_image)
                        print(file.filename, result_image)
                except:
                    pass
        len_image = len(img_watermark_list2)

        # ส่งกลับไปยังหน้าแรก
        return render_template('check_page2.html', filename2 = file.filename, text = text_input2, img_watermark_list2 = img_watermark_list2, result_image_list = result_image_list, len_image = len_image, email = person["email"], name = person["name"])
    else:
        if person["is_logged_in"] == True:
            return render_template("check_page.html", email = person["email"], name = person["name"])
        else:
            return redirect(url_for('login'))

#Login
@app.route("/login")
def login():
    return render_template("login.html")

#Login
@app.route("/logout")
def logout():
    global person
    person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
    return render_template("home_page.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to welcome page
            return redirect(url_for('home_page'))
        except:
            #If there is any error, redirect back to login
            return render_template("login.html")
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('home_page'))
        else:
            return render_template("login.html")

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        confirm_password = result["confirm_password"]
        name = result["name"]
        if password != confirm_password:
            return render_template("signup.html")
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('home_page'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('home_page'))
        else:
            return redirect(url_for('register'))
        
if __name__ == '__main__':
    app.run(debug=True, port=5888)

