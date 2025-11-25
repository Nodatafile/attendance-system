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
            }
        ]
        
        # 샘플 주차 데이터
        sample_weeks = [
            {"week_id": 1, "week_name": "1주차"},
            {"week_id": 2, "week_name": "2주차"},
            {"week_id": 3, "week_name": "3주차"},
            {"week_id": 4, "week_name": "4주차"},
            {"week_id": 5, "week_name": "5주차"}
        ]
        
        # 풍부한 샘플 출석 데이터
        sample_attendance = [
            # 1주차
            {"student_id": "20240001", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 1, "status": "지각", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 1, "status": "결석", "date": "2024-03-01", "timestamp": datetime.now()},
            
            # 2주차
            {"student_id": "20240001", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 2, "status": "조퇴", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            
            # 3주차
            {"student_id": "20240001", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 3, "status": "결석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()}
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
            "/api/attendance-board", 
            "/api/init-db"
        ]
    })

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
            "students_added": 5,
            "weeks_added": 5,
            "attendance_added": 15
        })
    else:
        return jsonify({
            "success": False, 
            "error": "데이터베이스 초기화 실패"
        })

# ===== 프론트엔드 맞춤 API =====

@app.route('/api/attendance-board', methods=['GET'])
def get_attendance_board():
    """출석부 전체 데이터 """
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        # 쿼리 파라미터 처리
        week = request.args.get('week', 1, type=int)  # 기본값 1주차
        
        # 학생 데이터 조회
        students = list(db.students.find().sort("student_id", 1))
        
        # 해당 주차 출석 데이터 조회
        attendance_data = list(db.attendance.find({"week_id": week}))
        
        # 프론트엔드 맞춤형 데이터 변환
        result = []
        for index, student in enumerate(students, 1):
            # 해당 학생의 출석 기록 찾기
            attendance_record = next(
                (a for a in attendance_data if a["student_id"] == student["student_id"]),
                None
            )
            
            # 출석 상태 변환 (출석=true, 그외=false)
            is_attendance = attendance_record["status"] == "출석" if attendance_record else False
            
            # 프론트엔드 맞춤형 포맷
            student_data = {
                "number": index,  # 번호 (1부터 시작)
                "name": student["name"],
                "student_id": int(student["student_id"]),  # 숫자로 변환
                "department": student["major"],
                "is_attendance": is_attentionce
            }
            result.append(student_data)
        
        return jsonify({
            "success": True,
            "data": result,
            "week": week,
            "count": len(result)
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
        
        # 프론트엔드 맞춤형 데이터 변환
        result = []
        for index, student in enumerate(students, 1):
            student_data = {
                "number": index,
                "name": student["name"],
                "student_id": int(student["student_id"]),
                "department": student["major"],
                "is_attendance": False  # 기본값
            }
            result.append(student_data)
        
        return jsonify({
            "success": True, 
            "data": result,
            "count": len(result)
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
        
        # student_id를 문자열로 변환 (DB에는 문자열로 저장됨)
        student_id_str = str(data.get('student_id'))
        
        attendance_record = {
            "student_id": student_id_str,
            "week_id": data.get('week_id'),
            "status": "출석" if data.get('is_attendance', True) else "결석",
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
            "data": {
                "student_id": int(attendance_record["student_id"]),
                "week_id": attendance_record["week_id"],
                "is_attendance": attendance_record["status"] == "출석"
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/attendance/status', methods=['GET'])
def get_attendance_status():
    """특정 주차의 출석 상태 조회"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        # 쿼리 파라미터 처리
        week = request.args.get('week', 1, type=int)
        
        # 학생 데이터와 출석 데이터 조회
        students = list(db.students.find().sort("student_id", 1))
        attendance_data = list(db.attendance.find({"week_id": week}))
        
        # 프론트엔드 맞춤형 데이터 변환
        result = []
        for index, student in enumerate(students, 1):
            # 해당 학생의 출석 기록 찾기
            attendance_record = next(
                (a for a in attendance_data if a["student_id"] == student["student_id"]),
                None
            )
            
            # 출석 상태 변환
            is_attendance = attendance_record["status"] == "출석" if attendance_record else False
            
            student_data = {
                "number": index,
                "name": student["name"],
                "student_id": int(student["student_id"]),
                "department": student["major"],
                "is_attendance": is_attendance
            }
            result.append(student_data)
        
        # 통계 계산
        total_students = len(result)
        present_count = sum(1 for student in result if student["is_attendance"])
        attendance_rate = round((present_count / total_students) * 100, 2) if total_students > 0 else 0
        
        return jsonify({
            "success": True,
            "data": result,
            "week": week,
            "summary": {
                "total_students": total_students,
                "present_count": present_count,
                "absent_count": total_students - present_count,
                "attendance_rate": attendance_rate
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True)
