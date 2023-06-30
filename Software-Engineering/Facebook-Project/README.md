# Facebook-Project
This is a web application that simulates some of the basic functionality of Facebook, including user authentication, creating and editing posts, and liking posts.

Technologies Used
Python 3.8
Django 3.2
MySQL 8.0
HTML 5
CSS 3
JavaScript ES6

# Installation
Clone this repository to your local machine:

git clone https://github.com/yousefayman2003/Facebook-Project.git

```
Install the required Python packages using pip:
pip install -r requirements.txt
```

Create a MySQL database named facebook on your local machine.

Edit the DATABASES setting in settings.py to connect to your local MySQL database:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'facebook',
        'USER': 'your_database_username',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

```

Replace `'your_database_username'` and `'your_database_password'` with your actual database username and password.

Run the Django development server:

 python manage.py runserver
 ```
Open your web browser and navigate to `http://localhost:8000` to view the application.

## Usage

The main functionality of the application is centered around searching for users, creating and editing posts, and liking, commenting on posts created by other users.

### User Authentication

To use the application, you must first create an account by clicking the "Sign Up" link on the login page and providing a valid email address and password. Once you've created an account, you can log in by entering your email address and password on the login page.

### Creating and Editing Posts

Once you're logged in, you can create a new post by entering a title and content of a post then clicking the "Post" button on the home page. This will make a post.

After you've created a post, you can edit it by clicking the "Edit" button on the post's detail page. This will take you to a form where you can update the text of the post.

### Liking Posts

To like a post created by another user, simply click the heart icon next to the post on the home page or on the post's detail page. This will increment the number of likes for the post and indicate that you've liked the post.

### Other Features

The application also includes some other features, such as pagination of posts on the home page, a search bar to search for  a user profilepage where you can view your own posts and edit your profile information.

## Contact

If you have any questions or comments about this project, feel free to contact the author at yousefayman2003@gmail.com.
