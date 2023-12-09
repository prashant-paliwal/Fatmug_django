Vendor Management System Setup Instructions

1. Install Python:
   - Ensure Python is installed on your machine. Download it from python.org.

2. Create Virtual Environment:
   - Open a terminal or command prompt.
   - Run: virtualenv env

3. Activate Virtual Environment:

   For Windows:
   - Navigate to the 'Scripts' directory: cd env\Scripts
   - Activate the virtual environment: activate

   For Linux:
   - Activate the virtual environment: source env/bin/activate

4. Install Dependencies:
   - Go to the project root directory: cd Fatmung_assessment\vendor_management_system
   - Install project dependencies: pip install -r requirements.txt

5. Run Migrations:
   - Create and apply database migrations:
     - Run: python manage.py makemigrations
     - Run: python manage.py migrate

6. Running the Test Suite:
   - Run test cases: python manage.py test

7. Running the Server:
   - Start the development server: python manage.py runserver

After these steps, you can access the Vendor Management System at http://127.0.0.1:8000/ in your web browser.


8. **Testing with Postman:**
   - Download and install Postman > https://www.postman.com/downloads/.
   - Import the Postman collection:
     - Open Postman.
     - Click on "Import" in the top left corner.
     - Select "Link" and paste the below link of Postman collection.

       ```
       https://speeding-satellite-939721.postman.co/workspace/Fatmang~5632e4f4-4b80-44ea-8bcf-633a3a944cb3/collection/17930638-630e05ee-2219-41c2-a60f-708af920aaef?action=share&creator=17930638
       ```

       "or can impoprt apis collection via postman collection file attached along with readme file in root directory"

   - Use the imported collection to test APIs.

9. ** Documentation **
	- Please visit the link below and find the documentation of apis which include endpoint url and method, request 
	  parameter, headers, body, example request and response, authentication requirements etc.

	  link: https://documenter.getpostman.com/view/17930638/2s9YkgEkTr

**If you have further queries, feel free to reach out at my email - prashantpaliwal203@gmail.com **