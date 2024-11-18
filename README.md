# FastAPI Messenger

FastAPI Messenger is a real-time messaging platform designed for seamless communication, even across language barriers. Using AI-powered translation, users can chat in real-time with automatic message translations. The platform includes essential features such as user authentication, message sending/receiving, and AI-based translation.

## Features

**Real-time Messaging**: Instant communication between users.  
**AI-Powered Translation**: Chat with people speaking different languages effortlessly.  
**Secure Authentication**: Token-based authentication using JWT.  
**Chat Management**: Create chats, send messages, and maintain contact lists.

## Technology Stack

**Backend**: FastAPI  
**Frontend**: React
**Database**: PostgreSQL with SQLAlchemy ORM  
**AI Translation**: Integrated AI for real-time message translation

## Installation

### Prerequisites

**Python**: 3.12 or later  
**Dependencies**: Listed in requirements.txt

### Setup

1. Clone the repository:

git clone https://github.com/your-repo/fastapi-messenger.git
cd fastapi-messenger
2. Install dependencies:

pip install -r requirements.txt
3. Set up the environment variables: Create a .env file in the root directory and include:

APP_VERSION=0.0.1  
SECRET_KEY=your_secret_key   
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
DATABASE_URL=your_postgresql_database_url
4. Run the application:

uvicorn app.main:app --reload
5. Access the API documentation: Open http://127.0.0.1:8000/docs in your browser.

## API Endpoints

### Authentication

**Register**: POST /auth/register - Register a new user.  
**Login**: POST /auth/login - Authenticate and receive a JWT token.  
**Current User**: GET /auth/users/me - Retrieve details of the logged-in user.

### Messaging

**Send/Receive Messages**: POST /chat/{chat_id}/message  
**Get Messages**: GET /chat/{chat_id}/message

### Contacts and Chats

**Get Contacts**: GET /contacts
**Create Chat**: POST /chat

## Database

The application uses PostgreSQL as the database, managed through SQLAlchemy ORM.

## Authentication

The application implements JWT-based authentication. Upon successful login, users receive a token that must be included in the Authorization header for accessing protected routes.

Example:

Authorization: Bearer <access_token>  

## Testing

The application uses pytest for automated testing. To run the tests, use:

pytest  

The tests cover:

User registration and login
JWT token generation and validation
Messaging functionalities

## Environment Variables

The application uses environment variables for configuration. Below is an example of the .env file:

APP_VERSION=0.0.1  
SECRET_KEY=your_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
DATABASE_URL=your_postgresql_database_url  

## Project Structure

/.github         # CI/CD configuration files  
/app             # FastAPI application code  
/core            # Core utilities and settings  
/database        # Database models and migrations  
/tests           # Test suite for the application  

## Contact

If you have any questions or suggestions, feel free to reach out at eoma575@gmail.com.