<h1> Vendor Management System</h1>
The Vendor Management System (VMS) is a comprehensive software solution designed to streamline and optimize the process of managing vendors for businesses of all sizes.
The system provides a centralized platform for businesses to efficiently onboard, communicate with, evaluate, and manage their vendors, ultimately improving operational efficiency and vendor relationships.
![image](https://github.com/daringsingh22/Vendor_Management_Python_Project/assets/121395485/d6decbd2-dfad-4d9a-87bd-e1a868fa0df9)


<h2>Project Setup</h2>

<h3><-- Clone Project from github --></h3>

1. Ensure python and postman are already installed on system.<br>
2. Open VSCode to any project folder as desired.<br>
3. Clone the project from github --> git clone "https://github.com/daringsingh22/Vendor_Management_Python_Project.git"<br>
4. Open VScode again under folder 'VendorManagementSystem' and will be the main project folder.

<h3><-- Installing requirements --></h3>

5. Create virtual environment and activate it. <br>
6. Install all the requirements --> "pip install -r requirements.txt"

<h3><-- setting up DB --></h3>

7. Run following commands to create DB tables:
    - python manage.py makemigrations
    - python manage.py migrate

8. Create superuser for admin login:
    - python manage.py createsuperuser
    * enter username and password

9. To verify whether tables are being created successfully:
    - python manage.py runserver
    - open chorme and run url "http://127.0.0.1:8000/admin" and login with username and password as given, 3 tables will be created under "VENDORPROFILEMANAGEMENTAPP".

<h2>End Project Setup</h2>


<h2>Testing API Urls using postman<h2>

<h3><-- Create Token --></h3>

1. Login to admin panel with given credential as mention perviously (Point 9).<br>
2. Click on table name Tokens and create one token by clicking "ADD TOKEN".<br>
3. Copy created token.

<h3><-- Configure Postman --></h3>

4. Under headers, create one field for token: {"Key": Authorization, "Value":token generated_token}

<h3><-- Creating vendors Details API--></h3>

5. Open postman and configure the url and body:
    - Method : POST
    - Url : http://localhost:8000/api/vendors/
    - Body(raw - JSON): {
                            "name": "BlueDart",
                            "contact_details":"1234567890",
                            "address":"Marathahalli, Bangalore"
                        }
    - Under headers create one field for token: {"Key": Authorization, "Value":token generated_token}

6. Repeat no 4 (changes only in Body section) to create another vendor details

<h3><-- Creating purchase order API--></h3>

7. Configure url and body. Copy the vendor_code generated previously for which order is to be made:
    - Method : POST
    - Url : http://localhost:8000/api/purchase_orders/
    - Body(raw - JSON): {
                            "vendor":"vednor_code",
                            "items":{
                                        "product":"charger"
                                    },
                            "quantity":2,
                            "delivery_date":"2023-12-7"
                        }
8. Repeat no 7 to create more purchase for same or different vendors.

<h3><-- Acknowledge API --></h3>

9. Acknowledge the PO by the vendor. Copy the po_number for order to be acknowledged.
    - Method : POST
    - Url : http://localhost:8000/api/purchase_orders/po_number/acknowledge/
    - It will return the response time in second.

<h3><-- Metric performance API --></h3>

Note: When order is created, status is in "pending" and then acknowedgment is done by the vendor, indicating that order is being processed. When the order is completed, status is changed to "completed" and all the required metric is calculated. Will also pass quality rating at the same time.

10. Change the status to "completed":
    - Method : PATCH
    - Url : http://localhost:8000/api/purchase_orders/po_number/
    - Body(raw - JSON): {
                            "status": "completed",
                            "quality_rating": 8.8
                        }
    - Metrix will be automatically generated in vendor table.

<h3><-- Vendor Performance API --></h3>

11. Check performance of each vendor. Get the vendor_code for which performance is need to be checked.
    - Method : GET
    - Url : http://localhost:8000/api/vendors/vendor_code/performance/
    - Output will be the performance metrix.

<h2>End Testing API Urls using postman<h2>


<h2>Test Suite Setup<h2>

<h3><----- Steps -----></h3>

1. First ensure all the steps mentioned in project setup section are done. * This step is mandatory
2. Make sure Vscode is opened under main project folder 'VendorManagementSystem' and virtual envrionment is activated.
3. run the command in terminal --> "python manage.py test VendorProfileManagementApp"
4. This will run the test suite:
    - First, it creates a vendor detail record in Vendor table.
    - Then it creates a purchase order for given vendor.
    - Now, Vendor acknowledges the order and average response time is created.
        - Note: as this is a test suite, acknowledgement is done instantly.
    - We now changes the status to 'complete' and remaining metrix are calculated.
    - Finally, it displays the performance of the vendor.
    - Output will be displayed in the terminal.
    - This test suite includes the testing of all the major api endpoints.

<h2>End Test Suite Setup<h2>
