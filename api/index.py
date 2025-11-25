from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# MongoDB 연결
MONGODB_URI = "mongodb+srv://attendance_user:Ilovekwu123!@attendance-cluster.n2vufnx.mongodb.net/?appName=attendance-cluster"

def get_db():
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        return client.attendance_db
    except Exception as e:
        print(f"MongoDB 연결 실패: {e}")
        return None

def initialize_database():
    """데이터베이스 초기화"""
    try:
        db = get_db()
        if db is None:
            return False
            
        sample_students = [
            {
                "student_id": "20240001",
                "name": "김철수", 
                "major": "컴퓨터공학과",
                "email": "kim@school.ac.kr",
                "phone": "010-1111-2222",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240002",
                "name": "이영희",
                "major": "경영학과", 
                "email": "lee@school.ac.kr",
                "phone": "010-2222-3333",
                "created_at": datetime.now()
            }
        ]
        
        sample_weeks = [
            {"week_id": 1, "week_name": "1주차"},
            {"week_id": 2, "week_name": "2주차"},
            {"week_id": 3, "week_name": "3주차"}
        ]
        
        sample_attendance = [
            {"student_id": "20240001", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()}
        ]
        
        # 기존 데이터 삭제
        db.students.delete_many({})
        db.weeks.delete_many({})
        db.attendance.delete_many({})
        
        # 새 데이터 삽입
        db.students.insert_many(sample_students)
        db.weeks.insert_many(sample_weeks) 
        db.attendance.insert_many(sample_attendance)
        
        return True
    except Exception as e:
        print(f"데이터베이스 초기화 실패: {e}")
        return False

# ===== API 라우트 =====

@app.route('/')
def home():
    return jsonify({
        "message": "🎓 출석 관리 시스템 API - Vercel",
        "status": "작동중",
        "endpoints": [
            "/api/students",
            "/api/attendance-board", 
            "/api/init-db"
        ]
    })

@app.route('/api/init-db', methods=['POST', 'GET'])
def init_db():
    """데이터베이스 초기화 API"""
    success = initialize_database()
    if success:
        return jsonify({
            "success": True,
            "message": "✅ 데이터베이스 초기화 완료!"
        })
    else:
        return jsonify({
            "success": False, 
            "error": "데이터베이스 초기화 실패"
        })

@app.route('/api/attendance-board', methods=['GET'])
def get_attendance_board():
    """출석부 전체 데이터"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        week = request.args.get('week', 1, type=int)
        
        students = list(db.students.find().sort("student_id", 1))
        attendance_data = list(db.attendance.find({"week_id": week}))
        
        result = []
        for index, student in enumerate(students, 1):
            attendance_record = next(
                (a for a in attendance_data if a["student_id"] == student["student_id"]),
                None
            )
            
            is_attendance = attendance_record["status"] == "출석" if attendance_record else False
            
            student_data = {
                "number": index,
                "name": student["name"],
                "student_id": int(student["student_id"]),
                "department": student["major"],
                "is_attendance": is_attendance
            }
            result.append(student_data)
        
        return jsonify({
            "success": True,
            "data": result,
            "week": week
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    """모든 학생 조회"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
            
        students = list(db.students.find().sort("student_id", 1))
        
        result = []
        for index, student in enumerate(students, 1):
            student_data = {
                "number": index,
                "name": student["name"],
                "student_id": int(student["student_id"]),
                "department": student["major"],
                "is_attendance": False
            }
            result.append(student_data)
        
        return jsonify({
            "success": True, 
            "data": result
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/attendance/check', methods=['POST'])
def check_attendance():
    """출석 체크"""
    try:
        data = request.get_json()
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        if not data or not data.get('student_id') or not data.get('week_id'):
            return jsonify({
                "success": False,
                "error": "학번과 주차는 필수 입력 항목입니다"
            }), 400
        
        student_id_str = str(data.get('student_id'))
        
        attendance_record = {
            "student_id": student_id_str,
            "week_id": data.get('week_id'),
            "status": "출석" if data.get('is_attendance', True) else "결석",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now()
        }
        
        db.attendance.update_one(
            {
                "student_id": attendance_record["student_id"],
                "week_id": attendance_record["week_id"]
            },
            {"$set": attendance_record},
            upsert=True
        )
        
        return jsonify({
            "success": True, 
            "message": "출석이 체크되었습니다"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Vercel에서 필요
if __name__ == '__main__':
    app.run(debug=True)
