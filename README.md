# Flask Inventory

An Inventory Management Web App that replicates the concept of an e-commerce application based around 2 entities namely the Admin of the Inventory and Wareshouse Location Supervisor, as per the requisites the application focuses on 3 main activities
1) Add Products, Update Products, View Products
2) Add Locations, Update Locations, View Locations
3) Add Movements of Products to the Base Location(X) or Move Products from Location(X) to Location(Y)
4) Update Movements, View Movements

but, here's a little twist to add the uniqueness of this web app, the Admin and Inventory Manager have different rights given to them.

Admin Rights
1) Adding/Updating Products
2) Adding Movements from the Admin Headquarters to the Warehouse Location
3) Adding Movements from one Location to Another
4) View Status of each Warehouse Location

Warehouse Location Supervisor Rights
1) Registeration of New Location
2) Request for new Products
3) View the status of activities

Additional Functionalities
1) Carts: for the Warehouse Location Supervisors to add Products to stock up the local inventory
2) Status: View Status of activities completed each day with interactive graphs powered by [Pygal](http://www.pygal.org/en/stable/)
3) Download Status Report: Reports are downloaded in pdf format


## 1.0 Getting Started
How to use/play with this web app?

### 1.1 Getting the files on your machine
You can download the repository or simply do a ```git clone  <repo-name>``` from your command prompt or Linux Terminal and there you have the files on your local machine

### 1.2 Installation of pre-requisite libraries
The package consists of a [requirements.txt](https://github.com/glenveigas437/Flask-Inventory-/blob/main/requirements.txt) file, go to your cmd and hit command ```pip install -r requirements.txt``` and you have all the libraries installed

### 1.3 Running the application
Hit the command ```python run.py``` for Windows and ```python3 run.py``` for Mac/Linux
![Running the application](https://user-images.githubusercontent.com/31877827/138885493-fa4fe32b-6ca6-4ad1-8843-77e17d44b130.png)


See the magic happen ✳️


## 2.0 Main App
### 2.1 Home Page
here are some screenshots of the home page
![Home Page 1](https://user-images.githubusercontent.com/31877827/138886099-abcf5cab-ac98-46f0-bc01-e0298d8aac5e.png)

![Home Page 2](https://user-images.githubusercontent.com/31877827/138886236-5b36b215-9910-469f-80eb-9b06ee075e9b.png)

![Home Page 3](https://user-images.githubusercontent.com/31877827/138886312-20c71a2d-3f71-433d-8e9f-684baddc78a3.png)

![Home Page 4](https://user-images.githubusercontent.com/31877827/138886392-a6a1ae5e-7e63-45c7-afd6-eb4b2695ab88.png)

You can hover over some the contents to view the animations

### 2.2 Login/Register Page
Since the application has 2 main entities based on their roles and responsibilities, there are 2 different Login Sections

![Admin Login Page](https://user-images.githubusercontent.com/31877827/138887106-5e9d51fb-76c0-4af8-a8b8-30d9113168d5.png)

![Admin Registration Page](https://user-images.githubusercontent.com/31877827/138887259-d62ecd8b-d1fe-40a2-b03e-acb694e04ce3.png)

The registration pages have the roles and rights mentioned on the LHS of the page

## 3.0 Admin - Products
### 3.1 Admin Home
![image](https://user-images.githubusercontent.com/31877827/138887848-8715b94c-8fbd-4555-99c2-f552937462de.png)

### 3.2 Add Brand, Categories, Products
![Adding Brand](https://user-images.githubusercontent.com/31877827/138888131-cf93f635-09dd-40d3-8dde-a6db27b55436.png)
![Adding Category](https://user-images.githubusercontent.com/31877827/138888283-e07fa7f0-59e9-4d67-a166-7ad4bbaab269.png)
![Adding Product](https://user-images.githubusercontent.com/31877827/138888456-8edddefe-1b49-4313-8d99-fb81e4741b3f.png)

Once the Products are added you can view them
![Products Added](https://user-images.githubusercontent.com/31877827/138888680-8a2a91a3-9501-429c-a12d-7dea6198a407.png)

## 4.0 Location Warehouse Supervisor - Registration, Requesting for Products
### 4.1 Supervisor Registration
You need to register with the Location Name, and add the specific address to the location warehouse
![Registration](https://user-images.githubusercontent.com/31877827/138889643-27d1a029-3f49-487a-a7bc-1312c5a5828f.png)

### 4.2 Supervisor Home
![Supervisor Home](https://user-images.githubusercontent.com/31877827/138889965-0166075f-71a7-44c9-9599-6ccf7f6aeaa3.png)

### 4.3 View Details of the Product and Add to Cart
![Details Page](https://user-images.githubusercontent.com/31877827/138890275-c4d55ac2-4193-410b-b225-d0b6d27acb18.png)

### 4.4 Cart
The requested products are added to the cart, multiple products can also be added.

![Cart](https://user-images.githubusercontent.com/31877827/138890624-e3024ec8-a380-4631-982a-c651e2480fe2.png)

### 4.5 View Orders
Orders made can be seen under: Home Page --> Location Name dropdown ---> Orders

![Orders](https://user-images.githubusercontent.com/31877827/138890879-5035d52b-1f19-4feb-94b9-c070002636bd.png)
These Orders are Pending

## 5.0 Admin - Orders, Movements, Status
### 5.1 List of Orders made by Location Supervisors
![image](https://user-images.githubusercontent.com/31877827/138891623-64362aee-34bd-420f-93c9-07cdd895fda3.png)


### 5.2 Viewing a specific order
![image](https://user-images.githubusercontent.com/31877827/138891479-0affb9fd-064f-49ae-958c-81cf14c38a28.png)
There is a Make Movement Button which redirects you to the movements Page

### 5.3 Movement of Products
![image](https://user-images.githubusercontent.com/31877827/138891897-144bf100-889a-4470-a169-3abb21d38d88.png)

### Updated List of Orders completed
![image](https://user-images.githubusercontent.com/31877827/138892186-d22fb741-662f-4470-82d6-91421cce06e1.png)

### 5.4 List of Locations
![image](https://user-images.githubusercontent.com/31877827/138892700-7b77b332-0b84-4ece-ab71-53b96eba854b.png)

### 5.4.1 Location Profile
![image](https://user-images.githubusercontent.com/31877827/138892595-57e83fa4-dd1d-478b-ba8e-6ea722fdc5d7.png)

The Location Profile also displays the distance between the Admin HQ and the Warehouse Location. Feature courtesy of [Geopy](https://github.com/geopy/geopy) 

### 5.4.2 Status
![image](https://user-images.githubusercontent.com/31877827/138898165-7d3c8650-51bc-4310-8f64-1553ebbf93c6.png)

![image](https://user-images.githubusercontent.com/31877827/138898285-caf81a31-e31a-494b-bd19-8503ad178862.png)

![image](https://user-images.githubusercontent.com/31877827/138898420-d76cc819-2c11-46e6-8668-5f317a6cf3c3.png)

![image](https://user-images.githubusercontent.com/31877827/138898526-7647dbfe-b750-4b60-bffe-4152836fdf75.png)

![image](https://user-images.githubusercontent.com/31877827/138898607-71920649-8276-4d6c-8a15-7c54981bacb7.png)

## 6.0 Supervisor - Status
![image](https://user-images.githubusercontent.com/31877827/138898979-73132082-ae42-4a3c-86dc-8bdcb7eb72b7.png)

## 7.0 Download PDF

The status report can be downloaded in a pdf format courtesy of [wkhtmltopdf](https://wkhtmltopdf.org/)
Though the installation is not straightforward, you may face certain issues, You can read this [Stack Overflow](https://stackoverflow.com/questions/27673870/cant-create-pdf-using-python-pdfkit-error-no-wkhtmltopdf-executable-found) thread to resolve it.

Downloaded pdf file can be viewed in the Project folder on your local machine
![image](https://user-images.githubusercontent.com/31877827/138899883-6dc1177b-ea93-476f-9e9d-0e6008e1cb63.png)


This project is also hosted on [PythonAnywhere](http://inventoryapp.pythonanywhere.com)





















