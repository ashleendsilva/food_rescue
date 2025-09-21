# Food Save & Share Platform
This project is a web-based platform that connects restaurants with excess food to NGOs and volunteers who can distribute it to people in need. The system helps reduce food waste while addressing hunger in communities through a simple, user-friendly interface.
---

## Features

 -**Restaurant Dashboard**:- Add and manage excess food listings with contact details  
-**NGO Portal** - Browse available food items with pickup locations and contact information  
-**Interactive Map** - Locate nearby restaurants and food pickup points  
-**Dual Authentication** - Separate login/signup flows for restaurants and NGOs  
-**Responsive Design** - Works seamlessly on desktop and mobile devices  
-**Real-time Updates** - Dynamic food listing updates and availability status  

## Tech Stack

-**Frontend**: HTML5, CSS3, Vanilla JavaScript  
-**Styling**: Custom CSS with modern UI/UX design  
-**Maps**: Google Maps Embed API  
-**Backend Integration**: RESTful API endpoints  
-**Storage**: SQLite   
 
 ## Setup Instructions

### 1.Download the project files

```bash
git clone https://github.com/yourusername/food-save-share.git
cd food-save-share
```
### 2.Set up your backend server

-**Configure your backend to handle the following endpoints**:

`POST /auth/signup/restaurant` - **Restaurant registration**  
`POST /auth/signup/ngo` - **NGO registration**  
`POST /auth/login` - **User authentication**  
`POST /auth/food/add` - **Add food listings**  
`GET /auth/food/available` - **Get available food for NGOs**  
`GET /auth/food/my-foods` - **Get restaurant's food listings**  


### 3.Configure Google Maps (Optional)

-Replace the Google Maps embed URL with your location   
-Add your Google Maps API key if needed  


### 4.Deploy the application

-Upload `index.html` to your web server  
-Ensure your backend APIs are accessible  
-Test the authentication and food management flows  
