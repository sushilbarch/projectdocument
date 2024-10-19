import os
import json
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Base directory to store projects (use absolute path)
BASE_DIR = os.path.abspath("./Projects")
UPLOAD_FOLDER = os.path.abspath("./Uploads")
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png', 'xlsx', 'xls', 'dwg', 'dxf', 'kml', 'kmz'}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to create a new project folder
def create_project(project_name):
    # Generate a unique identifier for the project
    project_id = project_name.replace(" ", "_").lower()
    
    # Create the project directory
    project_path = os.path.join(BASE_DIR, project_id)
    
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        
        # Create subfolders for different document types
        subfolders = ["Planning_Documents", "Estimate_Documents", "Notices", "Technical_Evaluation", "Financial_Evaluation", 
                      "Contract_Documents", "Bank_Guarantees", "Insurance_Documents", "Lab_Test_Documents", 
                      "Running_Bills", "Final_Bill", "WCR", "Date_Extension", "Drawing_Files", "Other_Details", "Letters"]
        for folder in subfolders:
            os.makedirs(os.path.join(project_path, folder))
        
        # Save basic project information in a JSON file for reference
        project_info = {
            "project_id": project_id,
            "project_name": project_name,
            "document_folders": subfolders
        }
        with open(os.path.join(project_path, "project_info.json"), "w") as json_file:
            json.dump(project_info, json_file)

# Route to create a new project (GET form + POST submission)
@app.route('/create_project', methods=['GET', 'POST'])
def create_project_route():
    if request.method == 'POST':
        project_name = request.form['project_name']
        create_project(project_name)
        flash(f"Project '{project_name}' created successfully.")
        return redirect(url_for('list_projects'))
    return render_template('create_project.html')

# Route to list all projects
@app.route('/list_projects', methods=['GET'])
def list_projects():
    if os.path.exists(BASE_DIR):
        projects = os.listdir(BASE_DIR)
        return render_template('list_projects.html', projects=projects)
    else:
        flash("Project directory does not exist.")
        return redirect(url_for('index'))

# Route to show project data and upload documents
@app.route('/project/<project_id>', methods=['GET', 'POST'])
def show_project(project_id):
    project_path = os.path.join(BASE_DIR, project_id)
    project_info_path = os.path.join(project_path, "project_info.json")
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            folder_type = request.form['folder_type']
            folder_path = os.path.join(project_path, folder_type)
            if not os.path.exists(folder_path):
                flash("Invalid folder type selected.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            upload_path = os.path.join(folder_path, filename)
            file.save(upload_path)
            flash(f"File '{filename}' uploaded successfully to '{folder_type}'.")
            return redirect(url_for('show_project', project_id=project_id))
    if os.path.exists(project_path) and os.path.exists(project_info_path):
        with open(project_info_path, "r") as json_file:
            project_info = json.load(json_file)
        document_files = {}
        for folder in project_info['document_folders']:
            folder_path = os.path.join(project_path, folder)
            if os.path.exists(folder_path):
                document_files[folder] = os.listdir(folder_path)
        return render_template('project_details.html', project_info=project_info, project_id=project_id, document_files=document_files)
    else:
        flash("Project not found or project information file is missing.")
        return redirect(url_for('list_projects'))

# Route to download a specific document
@app.route('/download_document/<project_id>/<folder_type>/<filename>', methods=['GET'])
def download_document(project_id, folder_type, filename):
    file_path = os.path.join(BASE_DIR, project_id, folder_type, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("Document not found.")
        return redirect(url_for('show_project', project_id=project_id))

# Route to download project data
@app.route('/download_project/<project_id>', methods=['GET'])
def download_project(project_id):
    project_info_path = os.path.join(BASE_DIR, project_id, "project_info.json")
    if os.path.exists(project_info_path):
        return send_file(project_info_path, as_attachment=True)
    else:
        flash("Project data not found.")
        return redirect(url_for('list_projects'))

# HTML templates for rendering (simplified)
index_html = '''
<!doctype html>
<html>
<head><title>Project Management</title></head>
<body>
<h1>Welcome to Project Management</h1>
<ul>
    <li><a href="/create_project">Create a New Project</a></li>
    <li><a href="/list_projects">List All Projects</a></li>
</ul>
</body>
</html>
'''

create_project_html = '''
<!doctype html>
<html>
<head><title>Create Project</title></head>
<body>
<h1>Create a New Project</h1>
<form action="/create_project" method="post">
    <label for="project_name">Project Name:</label>
    <input type="text" id="project_name" name="project_name" required>
    <input type="submit" value="Create Project">
</form>
</body>
</html>
'''

list_projects_html = '''
<!doctype html>
<html>
<head><title>List of Projects</title></head>
<body>
<h1>Projects</h1>
<ul>
{% for project in projects %}
  <li><a href="/project/{{ project }}">{{ project }}</a> - <a href="/download_project/{{ project }}">Download</a></li>
{% endfor %}
</ul>
</body>
</html>
'''

project_details_html = '''
<!doctype html>
<html>
<head><title>Project Details</title></head>
<body>
<h1>Project: {{ project_info['project_name'] }}</h1>
<p>Project ID: {{ project_info['project_id'] }}</p>
<h2>Document Folders:</h2>
<ul>
{% for folder, files in document_files.items() %}
  <li>{{ folder }}
    <ul>
    {% for file in files %}
      <li>{{ file }} - <a href="/download_document/{{ project_id }}/{{ folder }}/{{ file }}">Download</a></li>
    {% endfor %}
    </ul>
  </li>
{% endfor %}
</ul>
<h2>Upload Document</h2>
<form action="/project/{{ project_id }}" method="post" enctype="multipart/form-data">
    <label for="folder_type">Select Document Type:</label>
    <select id="folder_type" name="folder_type">
    {% for folder in project_info['document_folders'] %}
        <option value="{{ folder }}">{{ folder }}</option>
    {% endfor %}
    </select>
    <br><br>
    <input type="file" name="file" required>
    <input type="submit" value="Upload">
</form>
</body>
</html>
'''

# Write HTML templates to files
if not os.path.exists('templates'):
    os.makedirs('templates')

with open('templates/index.html', 'w') as f:
    f.write(index_html)

with open('templates/create_project.html', 'w') as f:
    f.write(create_project_html)

with open('templates/list_projects.html', 'w') as f:
    f.write(list_projects_html)

with open('templates/project_details.html', 'w') as f:
    f.write(project_details_html)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # Ensure the base directory exists
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    app.run(debug=True)
