import os
import certifi
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

app = Flask(__name__)

# --- 1. ربط قاعدة البيانات SQL (Neon) ---
# التأكد من استخدام SSL لضمان الاتصال السحابي الآمن
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_FS9lf5OWXApx@ep-empty-scene-anpilbym-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# --- 2. ربط قاعدة البيانات NoSQL (MongoDB Atlas) ---
# التعديل هنا: استخدام certifi بشكل صريح لحل مشكلة SSL Handshake
mongo_uri = "mongodb+srv://zineb_admin:2004%2F10%2F04@cluster0.2ex5tcr.mongodb.net/?retryWrites=true&w=majority"
ca = certifi.where() #

# تحسين الذاكرة: تقليل عدد الاتصالات (maxPoolSize) لتجنب SIGKILL
mongo_client = MongoClient(mongo_uri, tlsCAFile=ca, connect=False, maxPoolSize=1) #
nosql_db = mongo_client["TP_Cloud_Zineb"]

@app.route('/')
def home():
    try:
        # العمل على SQL
        db.create_all()
        student = Student.query.filter_by(name="Zineb").first()
        if not student:
            new_student = Student(name="Zineb")
            db.session.add(new_student)
            db.session.commit()
            sql_status = "Data saved to SQL (Neon)!"
        else:
            sql_status = "Student already exists in SQL."

        # العمل على NoSQL
        nosql_db.activity_logs.insert_one({
            "event": "Project_Access",
            "student": "Zineb",
            "status": "Success"
        })
        nosql_status = "Activity logged to NoSQL (MongoDB Atlas)!"

        return f"""
        <div style="text-align:center; padding:50px; font-family:Arial;">
            <h1 style="color:#2c3e50;">TP V: Cloud Computing Success</h1>
            <p style="font-size:18px; color:#27ae60;"><b>{sql_status}</b></p>
            <p style="font-size:18px; color:#2980b9;"><b>{nosql_status}</b></p>
            <hr style="width:50%;">
            <p>تم الربط بنجاح بين تطبيق الويب وقواعد البيانات السحابية.</p>
        </div>
        """
    except Exception as e:
        print(f"Detailed Error: {e}")
        return f"<h1 style='color:red;'>Error connecting to Cloud:</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    # Render يتطلب الاستماع على 0.0.0.0 والمنفذ المحدد في البيئة
    port = int(os.environ.get("PORT", 10000)) #
    app.run(host="0.0.0.0", port=port)
