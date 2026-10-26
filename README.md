# FarmNova-AI-Chatbot 🌱

**An AI-powered agricultural assistant built with Flask, Google Gemini, and MongoDB Atlas.**

FarmNova AI helps farmers access agricultural information through an AI-powered chatbot. The application uses Google Gemini for AI responses and MongoDB Atlas to store conversations, user information, crop recommendations, disease history, weather history, and reports.

## ✨ Features

- **AI Agricultural Assistant:** Get agriculture-related guidance using Google Gemini.
- **MongoDB Atlas Integration:** Store and manage application data using PyMongo.
- **Conversation History:** Maintain chatbot conversations and messages.
- **User Management:** Store user-related information.
- **Disease History:** Maintain records of plant disease-related information.
- **Crop Recommendations:** Store crop recommendation results.
- **Weather History:** Maintain weather-related records.
- **Report Management:** Store and manage generated reports.

*Features depend on the functionality implemented in the current application version.*

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Google Gemini API | AI-powered responses |
| MongoDB Atlas | Cloud database |
| PyMongo | MongoDB database integration |
| HTML, CSS, JavaScript | Frontend interface |

## 🗄️ Database Structure

This version uses **MongoDB exclusively** for database operations. It uses PyMongo and does not use Flask-SQLAlchemy.

**Database name:** `farmnova`

### Collections

| Collection | Purpose |
|---|---|
| `conversations` | Stores chatbot conversations |
| `messages` | Stores conversation messages |
| `users` | Stores user-related information |
| `disease_history` | Stores disease-related records |
| `crop_recommendations` | Stores crop recommendation records |
| `weather_history` | Stores weather-related records |
| `reports` | Stores report information |

Collections may be created automatically when the application first writes data to them.

## 📋 Prerequisites

Before running the project, install or prepare:

- Python 3.10 or a compatible version supported by the dependencies
- Git
- A MongoDB Atlas account and database cluster
- A Google Gemini API key

## 🚀 Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/FarmNova-AI-Chatbot.git
cd FarmNova-AI-Chatbot
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\activate
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure your credentials:

```env
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@YOUR-ACTUAL-CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=farmnova
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Replace the placeholder values with your actual MongoDB Atlas connection details and Gemini API key.

**Security:** Never upload `.env` or expose your database password or API key on GitHub. Ensure `.env` is listed in `.gitignore`.

### 6. Configure MongoDB Atlas

1. Sign in to [MongoDB Atlas](https://cloud.mongodb.com/).
2. Create or select your database cluster.
3. Create a database user with an appropriate password.
4. Configure Network Access to allow your development machine to connect.
5. Copy the actual connection string from **Connect → Drivers**.
6. Update `MONGO_URI` in your `.env` file.

Do not use the example hostname as your actual cluster address.

### 7. Run the application

```powershell
python app.py
```

Open the application in your browser:

**http://127.0.0.1:5000**

## 📁 Project Structure

```text
FarmNova-AI-Chatbot/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── venv/                 # Local environment, not uploaded
```

*This is an illustrative structure. Adjust the folder names to match the actual files in your repository.*

## 🔧 Troubleshooting

### MongoDB DNS or connection error

If you see `pymongo.errors.ConfigurationError` or a DNS `NXDOMAIN` error:

- Verify that `MONGO_URI` contains your actual Atlas cluster hostname.
- Check that the cluster exists and is available.
- Confirm your network permits DNS SRV lookups.
- Verify your IP address is permitted in MongoDB Atlas Network Access.

### Missing environment variables

Confirm that `.env` exists in the project root and that the variable names match those expected by `app.py` and `database.py`.

### Missing Python dependencies

Activate your virtual environment and run:

```powershell
pip install -r requirements.txt
```

## 🔐 Security

- Keep `.env` out of version control.
- Never publish API keys, database passwords, or private credentials.
- Use environment variables for sensitive configuration.
- Grant database users only the permissions they require.
- If credentials are accidentally exposed, rotate them immediately.

## 🔮 Future Improvements

Potential improvements include:

- Multilingual support for Indian farmers.
- Plant disease detection from uploaded images.
- Location-based weather forecasts.
- Personalized crop and fertilizer recommendations.
- Downloadable agricultural reports.
- Voice-based interaction.

These are future enhancements unless already implemented in the current version.

## 👨‍💻 Author

**Hritik Kedar**

- GitHub: [@hritikkedar19](https://github.com/hritikkedar19)
- LinkedIn: [hritikkedar19](https://www.linkedin.com/in/hritikkedar19/)

## 📄 License

Choose a license before distributing this project publicly. For example, you may use the MIT License by adding a `LICENSE` file containing the appropriate license text.

---

