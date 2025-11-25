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
            "/api/attendance", 
            "/api/init-db",
            "/api/stats/overview"
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

# ===== 출석 관리 API =====

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """모든 출석 기록 조회 (쿼리 파라미터 지원)"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        # 쿼리 파라미터 처리
        week = request.args.get('week', type=int)
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        
        # 필터 조건 구성
        filter_condition = {}
        if week:
            filter_condition['week_id'] = week
        if student_id:
            filter_condition['student_id'] = student_id
        if status:
            filter_condition['status'] = status
        
        # 학생 정보와 함께 출석 데이터 조회
        pipeline = [
            {
                "$match": filter_condition
            },
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
            "count": len(attendance_data),
            "filters": {
                "week": week,
                "student_id": student_id,
                "status": status
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/attendance/student/<student_id>', methods=['GET'])
def get_student_attendance(student_id):
    """특정 학생의 출석 기록 조회"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        # 쿼리 파라미터 처리 (주차 필터)
        week = request.args.get('week', type=int)
        
        filter_condition = {"student_id": student_id}
        if week:
            filter_condition['week_id'] = week
        
        pipeline = [
            {
                "$match": filter_condition
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
                    "week_id": 1,
                    "week_name": "$week_info.week_name",
                    "status": 1,
                    "date": 1,
                    "timestamp": 1
                }
            },
            {
                "$sort": {"week_id": 1}
            }
        ]
        
        attendance_data = list(db.attendance.aggregate(pipeline))
        
        for record in attendance_data:
            record['_id'] = str(record['_id'])
        
        # 학생 정보 조회
        student = db.students.find_one({"student_id": student_id})
        if student:
            student['_id'] = str(student['_id'])
        
        # 통계 계산
        total_weeks = 5
        present_count = len([a for a in attendance_data if a["status"] == "출석"])
        attendance_rate = round((present_count / total_weeks) * 100, 2) if total_weeks > 0 else 0
        
        return jsonify({
            "success": True,
            "student": student,
            "data": attendance_data,
            "summary": {
                "total_weeks": total_weeks,
                "present_count": present_count,
                "absent_count": total_weeks - present_count,
                "attendance_rate": attendance_rate
            },
            "filters": {
                "week": week
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/attendance/week/<int:week_id>', methods=['GET'])
def get_week_attendance(week_id):
    """특정 주차의 출석 기록 조회"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "데이터베이스 연결 실패"}), 500
        
        pipeline = [
            {
                "$match": {"week_id": week_id}
            },
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
                "$sort": {"student_id": 1}
            }
        ]
        
        attendance_data = list(db.attendance.aggregate(pipeline))
        
        for record in attendance_data:
            record['_id'] = str(record['_id'])
        
        # 통계 계산
        total_students = db.students.count_documents({})
        present_count = len([a for a in attendance_data if a["status"] == "출석"])
        attendance_rate = round((present_count / total_students) * 100, 2) if total_students > 0 else 0
        
        return jsonify({
            "success": True,
            "week": {
                "week_id": week_id,
                "week_name": f"{week_id}주차"
            },
            "data": attendance_data,
            "summary": {
                "total_students": total_students,
                "present_count": present_count,
                "absent_count": total_students - present_count,
                "attendance_rate": attendance_rate
            }
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

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True)
