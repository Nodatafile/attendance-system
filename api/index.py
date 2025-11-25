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

# ===== 시스템 관리 API =====

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

@app.route('/api/students', methods=['POST'])
def add_student():
    """새 학생 추가"""
    try:
        data = request.json
        db = get_db()
        
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

@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """특정 학생 조회"""
    try:
        db = get_db()
        student = db.students.find_one({"student_id": student_id})
        
        if not student:
            return jsonify({
                "success": False,
                "error": "학생을 찾을 수 없습니다"
            }), 404
        
        student['_id'] = str(student['_id'])
        return jsonify({
            "success": True,
            "data": student
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """학생 정보 수정"""
    try:
        data = request.json
        db = get_db()
        
        # 학생 존재 여부 확인
        existing_student = db.students.find_one({"student_id": student_id})
        if not existing_student:
            return jsonify({
                "success": False,
                "error": "학생을 찾을 수 없습니다"
            }), 404
        
        update_data = {
            "name": data.get('name', existing_student.get('name')),
            "major": data.get('major', existing_student.get('major')),
            "email": data.get('email', existing_student.get('email')),
            "phone": data.get('phone', existing_student.get('phone')),
            "updated_at": datetime.now()
        }
        
        # None 값 제거
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        result = db.students.update_one(
            {"student_id": student_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            updated_student = db.students.find_one({"student_id": student_id})
            updated_student['_id'] = str(updated_student['_id'])
            
            return jsonify({
                "success": True,
                "message": "학생 정보가 성공적으로 수정되었습니다",
                "data": updated_student
            })
        else:
            return jsonify({
                "success": False,
                "error": "학생 정보 수정에 실패했습니다"
            }), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """학생 삭제"""
    try:
        db = get_db()
        
        # 학생 존재 여부 확인
        student = db.students.find_one({"student_id": student_id})
        if not student:
            return jsonify({
                "success": False,
                "error": "학생을 찾을 수 없습니다"
            }), 404
        
        # 학생 삭제
        student_delete_result = db.students.delete_one({"student_id": student_id})
        
        # 해당 학생의 출석 기록도 삭제
        attendance_delete_result = db.attendance.delete_many({"student_id": student_id})
        
        return jsonify({
            "success": True,
            "message": "학생이 성공적으로 삭제되었습니다",
            "deleted_data": {
                "student": {
                    "student_id": student_id,
                    "name": student.get('name', '')
                },
                "attendance_records": attendance_delete_result.deleted_count
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

@app.route('/api/attendance/student/<student_id>', methods=['GET'])
def get_student_attendance(student_id):
    """특정 학생의 출석 기록 조회"""
    try:
        db = get_db()
        
        pipeline = [
            {
                "$match": {"student_id": student_id}
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
        total_weeks = 7
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
        
        # 필수 필드 검증
        if not data.get('student_id') or not data.get('week_id'):
            return jsonify({
                "success": False,
                "error": "학번과 주차는 필수 입력 항목입니다"
            }), 400
        
        # 학생 존재 여부 확인
        student = db.students.find_one({"student_id": data.get('student_id')})
        if not student:
            return jsonify({
                "success": False,
                "error": "학생을 찾을 수 없습니다"
            }), 404
        
        attendance_record = {
            "student_id": data.get('student_id'),
            "week_id": data.get('week_id'),
            "status": data.get('status', '출석'),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now()
        }
        
        # 기존 기록 확인
        existing_record = db.attendance.find_one({
            "student_id": attendance_record["student_id"],
            "week_id": attendance_record["week_id"]
        })
        
        # 기존 기록 업데이트 또는 새로 추가
        result = db.attendance.update_one(
            {
                "student_id": attendance_record["student_id"],
                "week_id": attendance_record["week_id"]
            },
            {"$set": attendance_record},
            upsert=True
        )
        
        action = "updated" if existing_record else "created"
        
        return jsonify({
            "success": True, 
            "message": f"출석이 성공적으로 {'수정' if existing_record else '체크'}되었습니다",
            "data": attendance_record,
            "action": action
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/attendance/<attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    """출석 기록 삭제"""
    try:
        db = get_db()
        
        # ObjectId로 변환 시도
        try:
            obj_id = ObjectId(attendance_id)
        except:
            return jsonify({
                "success": False,
                "error": "잘못된 출석 기록 ID입니다"
            }), 400
        
        # 출석 기록 존재 여부 확인
        attendance = db.attendance.find_one({"_id": obj_id})
        if not attendance:
            return jsonify({
                "success": False,
                "error": "출석 기록을 찾을 수 없습니다"
            }), 404
        
        # 출석 기록 삭제
        delete_result = db.attendance.delete_one({"_id": obj_id})
        
        return jsonify({
            "success": True,
            "message": "출석 기록이 성공적으로 삭제되었습니다",
            "deleted_record": {
                "attendance_id": attendance_id,
                "student_id": attendance.get('student_id', ''),
                "week_id": attendance.get('week_id', '')
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ===== 출석부 API =====

@app.route('/api/attendance-board', methods=['GET'])
def get_attendance_board():
    """출석부 전체 데이터"""
    try:
        db = get_db()
        
        students = list(db.students.find().sort("student_id", 1))
        weeks = list(db.weeks.find().sort("week_id", 1))
        attendance = list(db.attendance.find())
        
        result = {
            "weeks": weeks,
            "students": []
        }
        
        for student in students:
            student_data = {
                "student_id": student["student_id"],
                "name": student["name"],
                "student_number": student["student_id"],
                "major": student["major"],
                "attendance": {}
            }
            
            for week in weeks:
                week_attendance = next(
                    (a for a in attendance if a["student_id"] == student["student_id"] and a["week_id"] == week["week_id"]),
                    None
                )
                status = week_attendance["status"] if week_attendance else "결석"
                student_data["attendance"][week["week_id"]] = status
            
            student_data['_id'] = str(student['_id'])
            result["students"].append(student_data)
        
        return jsonify({"success": True, "data": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ===== 통계 API =====

@app.route('/api/stats/overview', methods=['GET'])
def get_stats_overview():
    """전체 통계"""
    try:
        db = get_db()
        
        total_students = db.students.count_documents({})
        total_attendance = db.attendance.count_documents({})
        
        # 주차별 통계
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
                "weekly_stats": weekly_stats,
                "status_distribution": status_distribution
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
