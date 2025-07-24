# Backend Image Sharing Application

A Django REST API backend for an image sharing social media application. This application provides a robust backend system for handling user authentication, image posts, following/follower relationships, and social interactions.

## 🌟 Features

- User authentication (signup/login)
- Image post creation and management
- Follow/unfollow functionality
- Feed generation based on followed users
- Like/unlike posts
- User profiles with statistics
- Token-based authentication

## 📦 Module Structure

### 1. Accounts Module (`accounts/`)
- Handles user authentication and authorization
- Features:
  - User signup with email validation
  - User login with token generation
  - Password validation and security
  - Token-based authentication system

### 2. Posts Module (`posts/`)
- Manages image posts and interactions
- Features:
  - Multiple image upload support
  - Post creation with captions
  - Like/unlike functionality
  - Feed generation
  - Post listing with pagination
  - Optimized image storage

### 3. Users Module (`users/`)
- Manages user profiles and relationships
- Features:
  - User profile management
  - Follow/unfollow functionality
  - User statistics (followers, following, posts count)
  - Profile view and updates

## 🛠 Pre-Requirements

- Python 3.13
- Python virtual environment
- Django 5.2.4
- Django REST Framework

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <REPO_URL>
   cd backend_image_sharing_application
   ```

2. **Set up virtual environment**
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   ```
   http://127.0.0.1:8000/ or http://localhost:8000/
   ```

## 🚀 API Endpoints

### Authentication Endpoints
- `POST /api/accounts/signup/` - Register new user
- `POST /api/accounts/login/` - Login user

### Posts Endpoints
- `POST /api/posts/upload-image/` - Create new post
- `GET /api/posts/feed/` - Get feed from followed users
- `GET /api/posts/all-posts/` - Get all posts
- `POST /api/posts/like-unlike/<post_id>/` - Like/unlike post

### Users Endpoints
- `POST /api/users/follow/<pk>/` - Follow user
- `POST /api/users/unfollow/<pk>/` - Unfollow user
- `GET /api/users/all-users/` - List all users

## 📝 Technical Details

- Uses Django REST Framework for API development
- Implements token authentication for secure endpoints
- Optimized database queries with proper indexing
- Implements proper file handling for images
- Uses signals for maintaining denormalized counters
- Includes proper validation and error handling
