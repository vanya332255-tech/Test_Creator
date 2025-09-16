# TestingApp - Test Creation and Management System

A modern web application for creating, publishing, and taking tests with Google OAuth and Telegram authentication support.

## 🚀 Features

- **Authentication**: Login via Google or Telegram
- **Test Creation**: Intuitive editor with different question types
- **Question Types**:
  - Single correct answer
  - Multiple correct answers  
  - Open-ended questions
- **Publishing**: Unique 6-character codes for tests
- **Taking Tests**: User-friendly interface for test completion
- **Analytics**: Detailed results statistics

## 🛠 Technologies

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (can be changed to PostgreSQL)
- **Authentication**: Google OAuth, Telegram Bot API

## 📦 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd TestingApp
```

2. **Create a virtual environment**:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp config.env .env
# Edit .env file with your settings
```

5. **Initialize database**:
```bash
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade
```

6. **Create superuser**:
```bash
python -m flask createsuperuser
```

7. **Run the application**:
```bash
cd src
$env:FLASK_APP="run.py"
python -m flask run
```

## 🔧 Configuration

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:5000/auth/google/callback`
6. Add your credentials to `.env` file

### Telegram Bot Setup
1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get bot token
3. Add token and bot name to `.env` file
4. Start the bot with `/start` command

## 👤 User Creation

### **Method 1: Registration via Google/Telegram (RECOMMENDED)**
1. Go to `http://localhost:5000/auth/login`
2. Click "Google" or "Telegram"
3. Follow authorization instructions
4. Your account will be created automatically

### **Method 2: Registration via form with verification**
1. Go to `http://localhost:5000/auth/register`
2. Fill out the registration form:
   - **Username** - unique username
   - **Email** - your email address
   - **First Name** and **Last Name**
   - **Password** (minimum 6 characters)
3. Click "Register"
4. Fill out Google Form to get verification code
5. Enter verification code
6. Login via `http://localhost:5000/auth/login`

### **Method 3: Create superuser (via command line)**
```bash
python -m flask createsuperuser
```
Enter data:
- Username: `admin`
- Email: `admin@example.com`
- First Name: `Admin`
- Last Name: `Administrator`
- Password: `your_password`

### **Method 4: Via Google/Telegram (for regular users)**
- Click "Login via Google" or "Login via Telegram"
- Follow on-screen instructions

## 📝 Creating Tests

### **1. Create new test:**
1. Login to the system
2. Click "Create Test"
3. Enter test title (e.g., "Math Test")
4. Click "Create Test"

### **2. Adding questions:**
1. After creating test, you'll be on the edit page
2. In "Add Question" section:
   - Enter question text
   - Choose question type:
     - **Single correct answer** - user can select only one answer
     - **Multiple correct answers** - user can select multiple answers
     - **Open-ended question** - user enters text answer
3. Click "Add Question"

### **3. Adding answer options:**
1. For questions with answer options:
   - Enter option text in "New answer option" field
   - Click "+" to add
   - Click "○" to make option correct
   - Click "🗑️" to delete option

### **4. Publishing test:**
1. When all questions are added, click "Publish"
2. Get unique 6-character code (e.g., `ABC123`)
3. Share this code with participants

## 🎯 Taking Tests

### **1. Find test:**
1. Click "Find Test"
2. Enter 6-character test code
3. Click "Find Test"

### **2. Answer questions:**
1. Read the question
2. For questions with options - select answers
3. For open-ended questions - enter text answer
4. Click "Complete Test"

### **3. View results:**
- See your result in "X/Y" format (correct/total)
- Percentage of correctness

## 📊 Results Analytics

### **1. View test results:**
1. Go to "My Tests"
2. Find the test you need
3. Click "Results"
4. See table with all attempts:
   - User
   - Completion date
   - Result (X/Y)
   - Correctness percentage

### **2. Edit test:**
1. In "My Tests" click "Edit"
2. You can:
   - Add new questions
   - Delete questions
   - Edit answer options
   - Change correct answers
   - Publish/unpublish

## 🔧 Additional Commands

### **Show all users:**
```bash
python -m flask listusers
```

### **Apply database migrations:**
```bash
python -m flask db upgrade
```

### **Create new migration:**
```bash
python -m flask db migrate -m "Description of changes"
```

## 📚 Test Examples

### **Example 1: Math Test**
**Title:** "Math for 5th Grade"

**Question 1:** "What is 2 + 2?"
- Type: Single correct answer
- Options:
  - 3 ❌
  - 4 ✅
  - 5 ❌
  - 6 ❌

**Question 2:** "Which of the following numbers are even?"
- Type: Multiple correct answers
- Options:
  - 2 ✅
  - 3 ❌
  - 4 ✅
  - 5 ❌
  - 6 ✅

**Question 3:** "Solve the equation: x + 3 = 7"
- Type: Open-ended question
- Correct answer: "x = 4"

### **Example 2: Ukrainian History Test**
**Title:** "Ukrainian History - Middle Ages"

**Question 1:** "When was Kyivan Rus founded?"
- Type: Single correct answer
- Options:
  - 862 year ✅
  - 988 year ❌
  - 1054 year ❌

**Question 2:** "Which of the listed princes ruled in Kyiv?"
- Type: Multiple correct answers
- Options:
  - Volodymyr the Great ✅
  - Yaroslav the Wise ✅
  - Bohdan Khmelnytsky ❌
  - Oleg the Prophet ✅

### **Example 3: Programming Test**
**Title:** "Python Basics"

**Question 1:** "How to create a list in Python?"
- Type: Open-ended question
- Correct answer: "my_list = []" or "list()"

**Question 2:** "Which of the following data types exist in Python?"
- Type: Multiple correct answers
- Options:
  - int ✅
  - string ✅
  - boolean ✅
  - char ❌
  - float ✅

## 🚀 Quick Start

### **1. First run:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure settings
cp config.env .env
# Edit .env file

# 3. Initialize database
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade

# 4. Create superuser
python -m flask createsuperuser

# 5. Run application
python src/run.py
```

### **2. Create first test:**
1. Open `http://localhost:5000`
2. Login to system
3. Click "Create Test"
4. Add 3-5 questions
5. Publish test
6. Share code with friends!

### **3. Test functionality:**
1. Open another browser (or private window)
2. Register as new user
3. Find test by code
4. Take the test
5. View results in admin panel

## 🔒 Security

### **Verification System:**
- **Registration via Google/Telegram** - automatic verification
- **Registration via form** - mandatory verification via Google Forms
- **Google Forms** provide additional user verification
- This prevents fake account creation and ensures security

### **Recommendations:**
1. **Set up Google OAuth** for convenient user login
2. **Set up Telegram Bot** for additional security
3. **Create Google Form** for registration verification (see `GOOGLE_FORM_SETUP.md`)
4. **Create superuser** for administrative access
5. **Regularly check** user list via `python -m flask listusers`

## 🎨 Design

The application uses modern, responsive design with:
- Gradient backgrounds
- Smooth animations
- Mobile-friendly interface
- Intuitive navigation
- Clean typography

## 📁 Project Structure

```
TestingApp/
├── src/                    # Main code
│   ├── app/               # Flask application
│   │   ├── auth/          # Authentication
│   │   ├── quizzes/       # Tests
│   │   ├── models.py      # Database models
│   │   └── ...
│   └── run.py            # Entry point
├── templates/            # HTML templates
├── static/              # CSS/JS files
├── migrations/          # Database migrations
├── instance/            # Database
├── requirements.txt     # Dependencies
├── config.env          # Configuration
└── README.md           # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you have any questions or need help, please open an issue in the repository.

---

Made with ❤️ for education and testing