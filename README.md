# projectdocument
Provide database management of construction project in nepal in order .

This code is a Flask web application for managing projects and their associated documents. It allows users to create project folders, upload documents to specific categories, list all projects, and download individual documents or project data. Below is a detailed explanation of its components and functionalities:

1. Overview
Flask: The web framework used to create and handle HTTP requests.
Project Management Features:
Create a New Project: Create a folder structure for a new project.
Upload Documents: Upload documents into specific subfolders of a project.
List Projects: Display all created projects.
Download Documents: Download individual project documents.
Download Project Info: Download project metadata.
Project Folder Structure: Organizes documents into different categories such as planning documents, technical evaluation, contract documents, etc.
2. Configuration
BASE_DIR: The root directory to store all projects.
UPLOAD_FOLDER: Directory for temporarily storing uploaded files.
ALLOWED_EXTENSIONS: Defines the allowed file types (pdf, docx, jpg, jpeg, png, xlsx, xls, dwg, dxf, kml, kmz) for upload.
3. Utility Functions
allowed_file(filename): Checks if the file has an allowed extension. This is used to validate user uploads.
create_project(project_name):
Creates a new project directory.
Creates subfolders for each document type.
Saves project metadata in a JSON file (project_info.json).
4. Flask Routes
4.1 Home Page (/)
Displays a welcome page with options to Create a New Project and List All Projects.
Template: index.html.
4.2 Create a New Project (/create_project)
GET: Renders a form for creating a new project.
POST: Handles project creation:
Takes a project name from the form.
Calls create_project() to create folders and save metadata.
Redirects to the list of projects with a success message.
Template: create_project.html.
4.3 List All Projects (/list_projects)
Lists all the created projects.
Displays links for each project to:
View Details: See documents and upload new ones.
Download Project Info: Download project_info.json containing metadata.
Template: list_projects.html.
4.4 Show Project Data and Upload Documents (/project/<project_id>)
Displays the details of a specific project, including:
The project ID and name.
Document folders and the documents they contain.
Option to Upload Documents to specific folders.
GET: Displays the project details.
POST: Handles document upload:
Validates the selected file.
Saves the file in the specified subfolder of the project.
Displays a success message if the upload is successful.
Template: project_details.html.
4.5 Download a Specific Document (/download_document/<project_id>/<folder_type>/<filename>)
Allows downloading a specific document from a project.
Uses send_file() to serve the file as an attachment.
4.6 Download Project Data (/download_project/<project_id>)
Allows downloading the project metadata (project_info.json) file.
Uses send_file() to serve the JSON file.
5. HTML Templates
HTML templates are used for rendering different pages. Each HTML file is saved in the templates folder:

index.html:
Displays a home page with links to Create a New Project or List All Projects.
create_project.html:
Displays a form to create a new project.
list_projects.html:
Lists all the projects with links to view project details or download project metadata.
project_details.html:
Displays details of a specific project:
Lists all document types and their contents.
Provides a form to upload new documents to the project.
6. Code Flow
Create Project:

The user navigates to the Create a New Project page, provides a name, and submits the form.
A new project folder is created with subfolders for document types.
The project metadata is saved in a JSON file.
List Projects:

The user views all created projects on the List All Projects page.
For each project, the user can view the details or download the project metadata.
View Project Details:

The user clicks on a specific project to see its details.
The user can view documents in each category or upload new documents.
Upload Document:

The user selects a document category and uploads a file to that specific folder.
The file is saved in the appropriate subfolder, and a success message is displayed.
Download Document:

The user can download any document associated with a project.
7. Potential Improvements
User Authentication: Add authentication to secure project data from unauthorized users.
Validation and Error Handling:
Add more input validation to prevent invalid project names or duplicate projects.
Improve error handling for missing files or directories.
Dynamic Project Metadata: Add more fields to project_info.json for detailed project tracking.
Enhanced UI: Improve the templates using frameworks like Bootstrap to enhance the UI.
8. Example Usage
Scenario: A construction project manager wants to manage multiple projects, including storing documents related to planning, contracts, evaluations, etc.
Steps:
The manager creates a new project using the Create Project feature.
They then upload various documents to the different categories within the project.
The manager can revisit any project to view, manage, and download documents as needed.
This application serves as a simple project management tool where documents related to a project are categorized, uploaded, and easily accessible. It provides a solid foundation for adding more advanced features like metadata editing, user permissions, and version tracking.
