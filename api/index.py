from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from bson import ObjectId

app = Flask(__name__)

# 상세 CORS 설정
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# MongoDB 연결
MONGODB_URI = "mongodb+srv://attendance_user:Ilovekwu123!@attendance-cluster.n2vufnx.mongodb.net/?appName=attendance-cluster"

def get_db():
    client = MongoClient(MONGODB_URI)
    return client.attendance_db

def initialize_database():
    """데이터베이스 초기화 - 테이블(컬렉션)과 샘플 데이터 생성"""
    try:
        db = get_db()
        
        # 샘플 학생 데이터
        sample_students = [
            {
                "student_id": "20240001",
                "name": "김철수", 
                "major": "컴퓨터공학과",
                "email": "kim@school.ac.kr",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240002",
                "name": "이영희",
                "major": "경영학과", 
                "email": "lee@school.ac.kr",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240003",
                "name": "박민수",
                "major": "전자공학과",
                "email": "park@school.ac.kr",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240004",
                "name": "정수진",
                "major": "디자인학과",
                "email": "jung@school.ac.kr",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240005",
                "name": "최윤호",
                "major": "영어영문학과",
                "email": "choi@school.ac.kr",
                "created_at": datetime.now()
            },
            {
                "student_id": "20240006", 
                "name": "한지민",
                "major": "법학과",
                "email": "han@school.ac.kr",
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
        
        # 풍부한 샘플 출석 데이터 (모든 학생 x 모든 주차)
        sample_attendance = [
            # 1주차 출석 데이터
            {"student_id": "20240001", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 1, "status": "지각", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 1, "status": "결석", "date": "2024-03-01", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 1, "status": "출석", "date": "2024-03-01", "timestamp": datetime.now()},
            
            # 2주차 출석 데이터
            {"student_id": "20240001", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 2, "status": "조퇴", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 2, "status": "출석", "date": "2024-03-08", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 2, "status": "지각", "date": "2024-03-08", "timestamp": datetime.now()},
            
            # 3주차 출석 데이터
            {"student_id": "20240001", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 3, "status": "결석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 3, "status": "출석", "date": "2024-03-15", "timestamp": datetime.now()},
            
            # 4주차 출석 데이터 (일부만)
            {"student_id": "20240001", "week_id": 4, "status": "출석", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240002", "week_id": 4, "status": "출석", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240004", "week_id": 4, "status": "지각", "date": "2024-03-22", "timestamp": datetime.now()},
            {"student_id": "20240006", "week_id": 4, "status": "출석", "date": "2024-03-22", "timestamp": datetime.now()},
            
            # 5주차 출석 데이터 (일부만)
            {"student_id": "20240001", "week_id": 5, "status": "조퇴", "date": "2024-03-29", "timestamp": datetime.now()},
            {"student_id": "20240003", "week_id": 5, "status": "출석", "date": "2024-03-29", "timestamp": datetime.now()},
            {"student_id": "20240005", "week_id": 5, "status": "출석", "date": "2024-03-29", "timestamp": datetime.now()}
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

# 서버 시작시 자동으로 테스트 데이터 생성
@app.before_first_request
def create_tables():
    try:
        db = get_db()
        # 컬렉션이 비어있을 때만 초기 데이터 생성
        if db.students.count_documents({}) == 0:
            initialize_database()
            print("✅ 테스트 데이터 자동 생성 완료!")
    except Exception as e:
        print(f"자동 데이터 생성 실패: {e}")

@app.route('/')
def home():
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
            "students_added": 6,
            "weeks_added": 7,
            "attendance_added": 23,
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

@app.route('/api/students', methods=['POST'])
def add_student():
    try:
        data = request.json
        db = get_db()
        
        student_data = {
            "student_id": data.get('student_id'),
            "name": data.get('name'),
            "major": data.get('major'),
            "email": data.get('email'),
            "created_at": datetime.now()
        }
        
        result = db.students.insert_one(student_data)
        
        return jsonify({
            "success": True,
            "message": "학생이 추가되었습니다",
            "id": str(result.inserted_id)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ===== 출석 관리 API =====

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    try:
        db = get_db()
        
        pipeline = [
            {
                "$lookup": {
                    "from": "students",
                    "localField": "student_id",
                    "foreignField": "student_id",
                    "as": "student_info"
                }
            },
            {
                "$unwind": "$student_info"
            },
            {
                "$lookup": {
                    "from": "weeks",
                    "localField": "week_id",
                    "foreignField": "week_id",
                    "as": "week_info"
                }
            },
            {
                "$unwind": "$week_info"
            },
            {
                "$project": {
                    "_id": 1,
                    "student_id": 1,
                    "student_name": "$student_info.name",
                    "student_major": "$student_info.major",
                    "week_id": 1,
                    "week_name": "$week_info.week_name",
                    "status": 1,
                    "date": 1,
                    "timestamp": 1
                }
            },
            {
                "$sort": {"student_id": 1, "week_id": 1}
            }
        ]
        
        attendance_data = list(db.attendance.aggregate(pipeline))
        
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
    try:
        data = request.json
        db = get_db()
        
        attendance_record = {
            "student_id": data.get('student_id'),
            "week_id": data.get('week_id', 1),
            "status": data.get('status', '출석'),
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
        
        return jsonify({"success": True, "message": "출석이 체크되었습니다"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ===== 통계 API =====

@app.route('/api/stats/overview', methods=['GET'])
def get_stats_overview():
    try:
        db = get_db()
        
        total_students = db.students.count_documents({})
        total_attendance = db.attendance.count_documents({})
        
        weekly_stats = []
        for week in range(1, 8):
            week_attendance = list(db.attendance.find({"week_id": week}))
            present_count = len([a for a in week_attendance if a["status"] == "출석"])
            
            weekly_stats.append({
                "week": week,
                "week_name": f"{week}주차",
                "total_students": total_students,
                "present_count": present_count,
                "absent_count": total_students - present_count,
                "attendance_rate": round((present_count / total_students) * 100, 2) if total_students > 0 else 0
            })
        
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
                "weekly_stats": weekly_stats,
                "status_distribution": status_distribution
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
