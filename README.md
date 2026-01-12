# 🎉 Lamitie 2025 - University Event Management System

A complete **FastAPI-based backend** for managing university event registrations, QR code generation, email automation, and attendance tracking.

## 🚀 Features

- **Student Registration** - Register students with automatic QR code generation
- **Email Automation** - Send beautiful HTML invitation emails with QR codes
- **Attendance Tracking** - Scan QR codes to mark attendance on event day
- **Remote MySQL Database** - Connected to Hostinger MySQL server
- **Async Operations** - High-performance async SQLAlchemy + aiomysql
- **API Documentation** - Auto-generated Swagger UI and ReDoc
- **CORS Enabled** - Ready for React/Vite frontend integration

## 📋 Tech Stack

- **Framework:** FastAPI (Python 3.12+)
- **Database:** MySQL (Remote - Hostinger) with async SQLAlchemy
- **Email:** fastapi-mail with Gmail SMTP
- **QR Code:** qrcode + Pillow
- **Validation:** Pydantic V2
- **Server:** Uvicorn (ASGI)

## 🛠️ Installation

### Prerequisites
- Python 3.12+
- MySQL database (Hostinger or local)
- Gmail account with App Password

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/shaveenudayanga/lamitie-25.git
cd lamitie-25/backend
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
DB_URL=mysql+aiomysql://username:password@host:3306/database
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

> **Note:** For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.

5. **Run the server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server will start at: http://localhost:8000

## 📚 API Documentation

Once the server is running, access:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔌 API Endpoints

### Registration
```http
POST /register
```
Register a student and send QR code invitation email.

**Request Body:**
```json
{
  "name": "John Doe",
  "index_number": "2025CS001",
  "email": "john@university.edu",
  "combination": "Physical Science"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Registration successful! Check your email...",
  "student": {
    "id": 1,
    "name": "John Doe",
    "index_number": "2025CS001",
    "email": "john@university.edu",
    "combination": "Physical Science",
    "attendance_status": false,
    "created_at": "2026-01-13T10:30:00"
  }
}
```

### Attendance Scanning
```http
POST /scan
```
Mark student attendance by scanning QR code.

**Request Body:**
```json
{
  "index_number": "2025CS001"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Welcome, John Doe! Your attendance has been recorded.",
  "student_name": "John Doe",
  "already_scanned": false
}
```

### Health Check
```http
GET /health
```
Check API and database connection status.

### List Students
```http
GET /students
```
Get all registered students (admin endpoint).

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── database.py          # Async SQLAlchemy setup
├── models.py            # Database models (Student)
├── schemas.py           # Pydantic validation schemas
├── email_utils.py       # QR code generation & email sending
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── .env                 # Your actual credentials (not in Git)
```

## 🔐 Security

- Environment variables for all sensitive data
- `.env` file excluded from Git via `.gitignore`
- Gmail App Passwords for email authentication
- URL-encoded special characters in connection strings
- Production-ready error handling

## 🎨 Email Template

Students receive a beautifully designed HTML email with:
- Personalized greeting
- Embedded QR code for event entry
- Event details and instructions
- Responsive design for all devices

## 🚦 Running in Production

For production deployment:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use the included `Dockerfile` for containerized deployment.

## 🧪 Testing

Test the API using the built-in Swagger UI at `/docs` or with curl:

```bash
# Health check
curl http://localhost:8000/health

# Register a student
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Student",
    "index_number": "TEST001",
    "email": "test@example.com",
    "combination": "Physical Science"
  }'

# Mark attendance
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"index_number": "TEST001"}'
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

Developed for **Lamitie 2025** - University Cultural Festival

## 🆘 Troubleshooting

### Database Connection Issues
- Ensure Remote MySQL is enabled in Hostinger
- Whitelist your IP address in Hostinger Remote MySQL settings
- Verify credentials in `.env` file
- Check if special characters in password are URL-encoded

### Email Not Sending
- Use Gmail App Password, not regular password
- Remove spaces from App Password
- Enable "Less secure app access" if using older Gmail account
- Check SMTP settings (smtp.gmail.com:587)

### Server Won't Start
- Check if port 8000 is already in use
- Activate virtual environment before running
- Verify all dependencies are installed
- Check `.env` file exists and has correct format

---

**Server Status:** 🟢 Running at http://localhost:8000
**Documentation:** 📖 http://localhost:8000/docs
