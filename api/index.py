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
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # 연결 테스트
        client.admin.command('ismaster')
        return client.attendance_db
    except Exception as e:
        print(f"MongoDB 연결 실패: {e}")
        return None

def initialize_database():
    """데이터베이스 초기화 - 테이블(컬렉션)과 풍부한 샘플 데이터 생성"""
    try:
        db = get_db()
        if db is None:
            return False
            
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
            }
        ]
        
        # 샘플 주차 데이터
        sample_weeks = [
            {"week_id": 1, "week_name": "1주차"},
            {"week_id": 2, "week_name": "2주차"},
            {"week_id": 3, "week_name": "3주차"}
        ]
        
        # 샘플 출석 데이터
        sample_attendance = [
            {"student_id": "20240001", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 1, "status": "지각", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240001", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 2, "status": "조퇴", "date": "2024-03-08", "timestamp": datetime.now()}
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
    return jsonify({
        "message": "🎓 출석 관리 시스템 API",
        "status": "작동중",
        "database": "MongoDB",
        "version": "1.0.0",
        "endpoints": [
            "/api/students",
            "/api/attendance", 
            "/api/init-db",
            "/api/stats/overview"
        ]
    })

# favicon.ico 요청 처리
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/api/init-db', methods=['POST'])
def init_db():
    """데이터베이스 초기화 API"""
    success = initialize_database()
    if success:
        return jsonify({
            "success": True,
            "message": "✅ 데이터베이스 초기화 완료!",
            "students_added": 3,
            "weeks_added": 3,
            "attendance_added": 5
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
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
            
        students = list(db.students.find().sort("student_id", 1))
        for student in students:
            student['_id'] = str(student['_id'])
        return jsonify({
            "success": True, 
            "data": students,
            "count": len(students)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/students', methods=['POST'])
def add_student():
    """새 학생 추가"""
    try:
        data = request.json
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        # 필수 필드 검증
        if not data.get('student_id') or not data.get('name') or not data.get('major'):
            return jsonify({
                "success": False,
                "error": "학번, 이름, 학과는 필수 입력 항목입니다"
            }), 400
        
        # 학번 중복 검사
        existing_student = db.students.find_one({"student_id": data.get('student_id')})
        if existing_student:
            return jsonify({
                "success": False,
                "error": "이미 존재하는 학번입니다"
            }), 400
        
        student_data = {
            "student_id": data.get('student_id'),
            "name": data.get('name'),
            "major": data.get('major'),
            "email": data.get('email'),
            "phone": data.get('phone'),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        result = db.students.insert_one(student_data)
        
        return jsonify({
            "success": True,
            "message": "학생이 성공적으로 추가되었습니다",
            "data": {
                "_id": str(result.inserted_id),
                **student_data
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ===== 출석 관리 API =====

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """모든 출석 기록 조회"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        # 간단한 쿼리로 데이터 확인
        attendance_data = list(db.attendance.find().sort("student_id", 1))
        
        for record in attendance_data:
            record['_id'] = str(record['_id'])
        
        return jsonify({
            "success": True,
            "data": attendance_data,
            "count": len(attendance_data)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/attendance/check', methods=['POST'])
def check_attendance():
    """출석 체크"""
    try:
        data = request.json
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        # 필수 필드 검증
        if not data.get('student_id') or not data.get('week_id'):
            return jsonify({
                "success": False,
                "error": "학번과 주차는 필수 입력 항목입니다"
            }), 400
        
        attendance_record = {
            "student_id": data.get('student_id'),
            "week_id": data.get('week_id'),
            "status": data.get('status', '출석'),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now()
        }
        
        # 기존 기록 업데이트 또는 새로 추가
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
            "message": "출석이 체크되었습니다",
            "data": attendance_record
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ===== 통계 API =====

@app.route('/api/stats/overview', methods=['GET'])
def get_stats_overview():
    """전체 통계"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        total_students = db.students.count_documents({})
        total_attendance = db.attendance.count_documents({})
        
        # 상태별 분포
        status_distribution = {
            "출석": db.attendance.count_documents({"status": "출석"}),
            "결석": db.attendance.count_documents({"status": "결석"}),
            "지각": db.attendance.count_documents({"status": "지각"}),
            "조퇴": db.attendance.count_documents({"status": "조퇴"})
        }
        
        total_present = status_distribution["출석"]
        overall_rate = round((total_present / total_attendance) * 100, 2) if total_attendance > 0 else 0
        
        return jsonify({
            "success": True,
            "data": {
                "total_students": total_students,
                "total_attendance_records": total_attendance,
                "overall_attendance_rate": overall_rate,
                "status_distribution": status_distribution
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 건강 상태 체크 엔드포인트
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True)
