# Student Semaphore

This application is a status semaphore for students to share how they are doing in a classroom or computer lab environment. It allows students to indicate their current status (e.g., working, need help, away) using a visual interface that represents the room layout and individual computers.

## Features
- Visual representation of the room and computers
- Each computer can display its current status
- Statuses are updated in real-time
- Login system for students to identify their computer
- Secure module signing and verification for integrity

## Technologies Used
- Python (Flask web framework)
- HTML, CSS, JavaScript for frontend
- SQLite for backend data storage
- PyCryptodome for cryptographic signing of modules

## Setup Instructions
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Generate RSA keys for signing modules:**
   ```bash
   openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
   openssl rsa -pubout -in private_key.pem -out public_key.pem
   ```
3. **Sign modules:**
   ```bash
   python sign-modules.py
   ```
4. **Run the application:**
   ```bash
   python app.py
   ```

## Usage
- Access the web interface in your browser.
- Log in using your assigned computer hostname.
- Change your status as needed.
- View the status of other students in the room.

## Security
- All Python modules in the `modules/` directory are signed using the developer's private key.
- Signatures are verified using the public key to ensure integrity and authenticity.

## Folder Structure
- `app.py` - Main application entry point
- `web.py` - Web routes and logic
- `sign-modules.py` - Script for signing and verifying modules
- `modules/` - Python modules for application features
- `static/` - Static files (CSS, JS)
- `templates/` - HTML templates
- `data/` - SQLite database

## License
MIT License

## Author
Developed by Adam

