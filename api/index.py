from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB 연결
MONGODB_URI = "mongodb+srv://attendance_user:Ilovekwu123!@attendance-cluster.n2vufnx.mongodb.net/"

def get_db():
    client = MongoClient(MONGODB_URI)
    return client.attendance_db

@app.route('/')
def home():
    return jsonify({
        "message": "🎓 출석 관리 시스템 API", 
        "status": "작동중",
        "database": "MongoDB"
    })

@app.route('/api/test-db')
def test_db():
    try:
        db = get_db()
        # 간단한 쿼리 실행
        count = db.students.count_documents({})
        return jsonify({
            "success": True, 
            "message": "MongoDB 연결 성공!",
            "students_count": count
        })
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"MongoDB 연결 실패: {str(e)}"
        })

@app.route('/api/init-db', methods=['POST'])
def init_db():
    try:
        db = get_db()
        
        # 샘플 데이터
        sample_students = [
            {"student_id": "20240001", "name": "김철수", "major": "컴퓨터공학과"},
            {"student_id": "20240002", "name": "이영희", "major": "경영학과"},
            {"student_id": "20240003", "name": "박민수", "major": "전자공학과"}
        ]
        
        # 기존 데이터 삭제
        db.students.delete_many({})
        
        # 새 데이터 추가
        for student in sample_students:
            student["created_at"] = datetime.now()
            db.students.insert_one(student)
        
        return jsonify({
            "success": True,
            "message": "데이터베이스 초기화 완료!",
            "students_added": len(sample_students)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        db = get_db()
        students = list(db.students.find().sort("student_id", 1))
        for student in students:
            student['_id'] = str(student['_id'])
        return jsonify({
            "success": True, 
            "data": students,
            "count": len(students)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
