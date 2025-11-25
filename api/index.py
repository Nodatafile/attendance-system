from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB 연결
MONGODB_URI = "mongodb+srv://attendance_user:Ilovekwu123!@attendance-cluster.n2vufnx.mongodb.net/?appName=attendance-cluster"

def get_db():
    client = MongoClient(MONGODB_URI)
    return client.attendance_db

def initialize_database():
    """데이터베이스 초기화 - 테이블(컬렉션)과 풍부한 샘플 데이터 생성"""
    try:
        db = get_db()
        
        # 풍부한 샘플 학생 데이터
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
            },
            {
                "student_id": "20240003",
                "name": "박민수",
                "major": "전자공학과",
                "email": "park@school.ac.kr",
                "phone": "010-3333-4444",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240004",
                "name": "정수진",
                "major": "디자인학과",
                "email": "jung@school.ac.kr",
                "phone": "010-4444-5555",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240005",
                "name": "최윤호",
                "major": "영어영문학과",
                "email": "choi@school.ac.kr",
                "phone": "010-5555-6666",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240006",
                "name": "한지민", 
                "major": "법학과",
                "email": "han@school.ac.kr",
                "phone": "010-6666-7777",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240007",
                "name": "송민준",
                "major": "의학과",
                "email": "song@school.ac.kr", 
                "phone": "010-7777-8888",
                "created_at": datetime.now()
            }
        ]
        
        # 샘플 주차 데이터
        sample_weeks = [
            {"week_id": 1, "week_name": "1주차"},
            {"week_id": 2, "week_name": "2주차"},
            {"week_id": 3, "week_name": "3주차"},
            {"week_id": 4, "week_name": "4주차"},
            {"week_id": 5, "week_name": "5주차"},
            {"week_id": 6, "week_name": "6주차"},
            {"week_id": 7, "week_name": "7주차"}
        ]
        
        # 풍부한 샘플 출석 데이터 (모든 학생 x 여러 주차)
        sample_attendance = [
            # 1주차 출석 데이터
            {"student_id": "20240001", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 1, "status": "지각", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 1, "status": "결석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240007", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            
            # 2주차 출석 데이터
            {"student_id": "20240001", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 2, "status": "조퇴", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 2, "status": "지각", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240007", "week_id": 2, "status": "결석", "date": "2024-03-08", "timestamp": datetime.now()},
            
            # 3주차 출석 데이터
            {"student_id": "20240001", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 3, "status": "결석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240007", "week_id": 3, "status": "지각", "date": "2024-03-15", "timestamp": datetime.now()},
            
            # 4주차 출석 데이터
            {"student_id": "20240001", "week_id": 4, "status": "출석", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 4, "status": "출석", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 4, "status": "출석", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 4, "status": "지각", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 4, "status": "결석", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 4, "status": "출석", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240007", "week_id": 4, "status": "출석", "date": "2024-03-22", "timestamp": datetime.now()},
            
            # 5주차 출석 데이터
            {"student_id": "20240001", "week_id": 5, "status": "조퇴", "date": "2024-03-29", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 5, "status": "출석", "date": "2024-03-29", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 5, "status": "출석", "date": "2024-03-29", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 5, "status": "출석", "date": "2024-03-29", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 5, "status": "출석", "date": "2024-03-29", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 5, "status": "지각", "date": "2024-03-29", "timestamp": datetime.now()},
            {"student_id": "20240007", "week_id": 5, "status": "출석", "date": "2024-03-29", "timestamp": datetime.now()},
            
            # 6주차 출석 데이터 (일부만)
            {"student_id": "20240001", "week_id": 6, "status": "출석", "date": "2024-04-05", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 6, "status": "출석", "date": "2024-04-05", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 6, "status": "결석", "date": "2024-04-05", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 6, "status": "출석", "date": "2024-04-05", "timestamp": datetime.now()},
            {"student_id": "20240007", "week_id": 6, "status": "출석", "date": "2024-04-05", "timestamp": datetime.now()},
            
            # 7주차 출석 데이터 (일부만)
            {"student_id": "20240001", "week_id": 7, "status": "출석", "date": "2024-04-12", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 7, "status": "출석", "date": "2024-04-12", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 7, "status": "지각", "date": "2024-04-12", "timestamp": datetime.now()},
            {"student_id": "20240007", "week_id": 7, "status": "출석", "date": "2024-04-12", "timestamp": datetime.now()}
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

# ===== 시스템 관리 API =====

@app.route('/')
def home():
    # 첫 요청시 데이터베이스 초기화 체크
    try:
        db = get_db()
        if db.students.count_documents({}) == 0:
            initialize_database()
            print("✅ 테스트 데이터 자동 생성 완료!")
    except Exception as e:
        print(f"자동 데이터 생성 실패: {e}")
    
    return jsonify({
        "message": "🎓 출석 관리 시스템 API",
        "status": "작동중",
        "database": "MongoDB",
        "version": "1.0.0",
        "test_data": "자동 생성됨"
    })

@app.route('/api/init-db', methods=['POST'])
def init_db():
    """데이터베이스 초기화 API"""
    success = initialize_database()
    if success:
        return jsonify({
            "success": True,
            "message": "✅ 데이터베이스 초기화 완료!",
            "students_added": 7,
            "weeks_added": 7,
            "attendance_added": 40,
            "collections": ["students", "weeks", "attendance"]
        })
    else:
        return jsonify({
            "success": False, 
            "error": "데이터베이스 초기화 실패"
        })

# ===== 학생 관리 API =====

@app.route('/api/students', methods=['GET'])
def get_students():
    """모든 학생 조회"""
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

# ... (나머지 API 함수들은 이전과 동일하게 유지)
# get_student, update_student, delete_student, get_attendance, 
# get_student_attendance, check_attendance, delete_attendance,
# get_attendance_board, get_stats_overview 함수들

if __name__ == '__main__':
    app.run(debug=True)
