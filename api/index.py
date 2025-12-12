from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import re
import os
import urllib.parse

# Flask 앱 생성
app = Flask(__name__)
CORS(app)

# Vercel에서 인식할 수 있도록 application 변수 추가
application = app

# MongoDB 연결
def get_mongodb_uri():
    """MongoDB URI 생성"""
    password = os.environ.get("MONGODB_PASSWORD", "Ilovekwu123!")
    encoded_password = urllib.parse.quote_plus(password)
    
    if os.environ.get("MONGODB_URI"):
        return os.environ.get("MONGODB_URI")
    else:
        return f"mongodb+srv://attendance_user:{encoded_password}@attendance-cluster.n2vufnx.mongodb.net/attendance_db?retryWrites=true&w=majority&appName=attendance-cluster"

MONGODB_URI = get_mongodb_uri()

def get_db():
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        return client.attendance_db
    except Exception as e:
        print(f"MongoDB 연결 실패: {e}")
        return None

def validate_student_data(data, is_update=False):
    """학생 데이터 검증"""
    errors = []
    
    if not is_update:
        if not data.get('student_id'):
            errors.append("학번은 필수 항목입니다")
        else:
            try:
                student_id = int(data['student_id'])
            except ValueError:
                errors.append("학번은 숫자여야 합니다")
        if not data.get('name'):
            errors.append("이름은 필수 항목입니다")
        if not data.get('major'):
            errors.append("학과는 필수 항목입니다")
    
    if data.get('email') and not re.match(r'^[^@]+@[^@]+\.[^@]+$', data.get('email', '')):
        errors.append("유효한 이메일 형식이 아닙니다")
    
    return errors

def validate_attendance_data(data):
    """출석 데이터 검증"""
    errors = []
    valid_statuses = ["출석", "결석", "지각", "조퇴", "공결"]
    
    if not data.get('student_id'):
        errors.append("학번은 필수 항목입니다")
    else:
        try:
            int(data['student_id'])
        except (ValueError, TypeError):
            errors.append("학번은 숫자여야 합니다")
            
    if not data.get('week'):
        errors.append("주차는 필수 항목입니다")
    elif not str(data.get('week')).isdigit():
        errors.append("주차는 숫자여야 합니다")
        
    if not data.get('status'):
        errors.append("출석 상태는 필수 항목입니다")
    elif data.get('status') not in valid_statuses:
        errors.append(f"출석 상태는 {', '.join(valid_statuses)} 중 하나여야 합니다")

    if data.get('week') and not str(data.get('week')).isdigit():
        errors.append("주차는 숫자여야 합니다")
        
    return errors

def initialize_database():
    """데이터베이스 초기화"""
    try:
        db = get_db()
        if db is None:
            return False
            
        sample_students = [
            {
                "student_id": 2007720116,
                "name": "김조은", 
                "major": "소프트웨어학부",
                "email": "kimjoeun@school.ac.kr",
                "phone": "010-1111-1111",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "student_id": 2022322035,
                "name": "배혜윤",
                "major": "영어산업학과", 
                "email": "baehyeyoon@school.ac.kr",
                "phone": "010-2222-2222",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "student_id": 2023205106,
                "name": "송윤서",
                "major": "로봇학부",
                "email": "songyounseo@school.ac.kr",
                "phone": "010-3333-3333",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "student_id": 2023321012,
                "name": "김초련",
                "major": "정보융합학부",
                "email": "kimchorun@school.ac.kr",
                "phone": "010-4444-4444",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "student_id": 2024405040,
                "name": "송주미",
                "major": "로봇학부",
                "email": "songjumi@school.ac.kr",
                "phone": "010-5555-5555",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]
        
        sample_weeks = [
            {"week_id": 1, "week_name": "1주차", "start_date": "2024-03-01", "end_date": "2024-03-07"},
            {"week_id": 2, "week_name": "2주차", "start_date": "2024-03-08", "end_date": "2024-03-14"},
            {"week_id": 3, "week_name": "3주차", "start_date": "2024-03-15", "end_date": "2024-03-21"},
            {"week_id": 4, "week_name": "4주차", "start_date": "2024-03-22", "end_date": "2024-03-28"},
            {"week_id": 5, "week_name": "5주차", "start_date": "2024-03-29", "end_date": "2024-03-30"},
            {"week_id": 6, "week_name": "6주차", "start_date": "2024-04-05", "end_date": "2024-04-11"},
            {"week_id": 7, "week_name": "7주차", "start_date": "2024-04-12", "end_date": "2024-04-18"}
        ]
        
        now = datetime.now()
        
        sample_attendance = [
            # 1주차
            {
                "student_id": 2007720116, 
                "week_id": 1, 
                "status": "결석", 
                "date": "2024-03-01", 
                "timestamp": now,
                "expires_at": None,
                "is_auto_absent_processed": False,
                "original_status": "결석",
                "last_updated": now,
                "recheck_count": 0,
                "first_check_time": None,
                "recheck_time": None,
                "notes": "샘플 데이터 - 첫 인식"
            },
            {
                "student_id": 2022322035, 
                "week_id": 1, 
                "status": "결석", 
                "date": "2024-03-01", 
                "timestamp": now,
                "expires_at": None,
                "is_auto_absent_processed": False,
                "original_status": "결석",
                "last_updated": now,
                "recheck_count": 0,
                "first_check_time": None,
                "recheck_time": None,
                "notes": "샘플 데이터 - 첫 인식"
            },
            {
                "student_id": 2023205106, 
                "week_id": 1, 
                "status": "결석", 
                "date": "2024-03-01", 
                "timestamp": now,
                "expires_at": None,
                "is_auto_absent_processed": False,
                "original_status": "결석",
                "last_updated": now,
                "recheck_count": 0,
                "first_check_time": None,
                "recheck_time": None,
                "notes": "샘플 데이터 - 첫 인식"
            },
            {
                "student_id": 2023321012, 
                "week_id": 1, 
                "status": "결석", 
                "date": "2024-03-01", 
                "timestamp": now,
                "expires_at": None,
                "is_auto_absent_processed": False,
                "original_status": "결석",
                "last_updated": now,
                "recheck_count": 0,
                "first_check_time": None,
                "recheck_time": None,
                "notes": "샘플 데이터 - 첫 인식"
            },
            {
                "student_id": 2024405040, 
                "week_id": 1, 
                "status": "출석", 
                "date": "2024-03-01", 
                "timestamp": now,
                "expires_at": None,
                "is_auto_absent_processed": False,
                "original_status": "출석",
                "last_updated": now,
                "recheck_count": 0,
                "first_check_time": None,
                "recheck_time": None,
                "notes": "샘플 데이터 - 첫 인식"
            }
        ]
        
        # 기존 데이터 삭제
        db.students.delete_many({})
        db.weeks.delete_many({})
        db.attendance.delete_many({})
        
        # 새 데이터 삽입
        db.students.insert_many(sample_students)
        db.weeks.insert_many(sample_weeks) 
        db.attendance.insert_many(sample_attendance)

        # 인덱스 생성
        db.attendance.create_index([("student_id", 1), ("week_id", 1)], unique=True)
        db.attendance.create_index([("expires_at", 1)])
        db.attendance.create_index([("is_auto_absent_processed", 1)])

        print("✅ 데이터베이스 초기화 완료 ")
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
        "timestamp": datetime.now().isoformat(),
        "version": "1.1.5"
    })

@app.route('/api/test-db', methods=['GET'])
def test_db():
    """데이터베이스 연결 테스트"""
    try:
        db = get_db()
        if db is None:
            return jsonify({
                "success": False,
                "error": "DATABASE_ERROR",
                "message": "데이터베이스 연결 실패"
            }), 500
        
        # 간단한 쿼리 테스트
        students_count = db.students.count_documents({})
        attendance_count = db.attendance.count_documents({})
        
        return jsonify({
            "success": True,
            "message": "데이터베이스 연결 성공",
            "data": {
                "students_count": students_count,
                "attendance_count": attendance_count,
                "timestamp": datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "DATABASE_ERROR",
            "message": str(e)
        }), 500

@app.route('/api/init-db', methods=['POST'])
def init_db():
    """데이터베이스 초기화"""
    success = initialize_database()
    if success:
        return jsonify({
            "success": True,
            "message": "✅ 데이터베이스 초기화 완료!",
            "timestamp": datetime.now().isoformat()
        })
    else:
        return jsonify({
            "success": False, 
            "error": "DATABASE_ERROR",
            "message": "데이터베이스 초기화 실패"
        }), 500

# ===== 학생 관리 API =====
@app.route('/api/students', methods=['GET'])
def get_students():
    """모든 학생 조회"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        # 쿼리 파라미터 처리
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 50, type=int)
        sort_field = request.args.get('sort', 'student_id')
        order = request.args.get('order', 'asc')
        
        # 정렬 방향 설정
        sort_direction = 1 if order == 'asc' else -1
        
        # 페이지네이션
        skip = (page - 1) * limit
        
        # 학생 데이터 조회
        students = list(db.students.find()
                       .sort(sort_field, sort_direction)
                       .skip(skip)
                       .limit(limit))
        
        total_count = db.students.count_documents({})
        
        # 결과 변환
        result = []
        for student in students:
            student_data = {
                "id": str(student["_id"]),
                "student_id": student["student_id"],
                "name": student["name"],
                "major": student["major"],
                "email": student.get("email", ""),
                "phone": student.get("phone", ""),
                "created_at": student.get("created_at", "").isoformat() if student.get("created_at") else "",
                "updated_at": student.get("updated_at", "").isoformat() if student.get("updated_at") else ""
            }
            result.append(student_data)
        
        return jsonify({
            "success": True, 
            "data": result,
            "pagination": {
                "page": page,
                "limit": limit,
                "total_count": total_count,
                "total_pages": (total_count + limit - 1) // limit
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """특정 학생 조회"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500

        # student_id를 숫자로 변환
        try:
            student_id_int = int(student_id)
        except ValueError:
            return jsonify({
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": "학번은 숫자여야 합니다"
            }), 400
            
        student = db.students.find_one({"student_id": student_id})
        if not student:
            return jsonify({
                "success": False,
                "error": "STUDENT_NOT_FOUND",
                "message": "학생을 찾을 수 없습니다"
            }), 404
        
        student_data = {
            "id": str(student["_id"]),
            "student_id": student["student_id"],
            "name": student["name"],
            "major": student["major"],
            "email": student.get("email", ""),
            "phone": student.get("phone", ""),
            "created_at": student.get("created_at", "").isoformat() if student.get("created_at") else "",
            "updated_at": student.get("updated_at", "").isoformat() if student.get("updated_at") else ""
        }
        
        return jsonify({
            "success": True,
            "data": student_data
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

@app.route('/api/students', methods=['POST'])
def create_student():
    """학생 추가"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": "요청 데이터가 없습니다"
            }), 400
        
        # 데이터 검증
        errors = validate_student_data(data)
        if errors:
            return jsonify({
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": ", ".join(errors)
            }), 400
        
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        # 중복 학번 확인
        existing_student = db.students.find_one({"student_id": data['student_id']})
        if existing_student:
            return jsonify({
                "success": False,
                "error": "STUDENT_ALREADY_EXISTS",
                "message": "이미 존재하는 학번입니다"
            }), 400
        
        # 학생 데이터 생성
        student_data = {
            "student_id": data['student_id'],
            "name": data['name'],
            "major": data['major'],
            "email": data.get('email', ''),
            "phone": data.get('phone', ''),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        result = db.students.insert_one(student_data)
        
        return jsonify({
            "success": True,
            "message": "학생이 추가되었습니다",
            "data": {
                "id": str(result.inserted_id),
                "student_id": student_data['student_id']
            }
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """학생 정보 수정"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": "요청 데이터가 없습니다"
            }), 400
        
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        # 학생 존재 확인
        existing_student = db.students.find_one({"student_id": student_id})
        if not existing_student:
            return jsonify({
                "success": False,
                "error": "STUDENT_NOT_FOUND",
                "message": "학생을 찾을 수 없습니다"
            }), 404
        
        # 데이터 검증
        errors = validate_student_data(data, is_update=True)
        if errors:
            return jsonify({
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": ", ".join(errors)
            }), 400
        
        # 업데이트 데이터 준비
        update_data = {**data, "updated_at": datetime.now()}
        
        # 학생 정보 업데이트
        db.students.update_one(
            {"student_id": student_id},
            {"$set": update_data}
        )
        
        return jsonify({
            "success": True,
            "message": "학생 정보가 수정되었습니다"
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """학생 삭제"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        # 학생 존재 확인
        existing_student = db.students.find_one({"student_id": student_id})
        if not existing_student:
            return jsonify({
                "success": False,
                "error": "STUDENT_NOT_FOUND",
                "message": "학생을 찾을 수 없습니다"
            }), 404
        
        # 출석 기록 삭제 여부 확인
        delete_attendance = request.args.get('delete_attendance', 'true').lower() == 'true'
        
        # 학생 삭제
        db.students.delete_one({"student_id": student_id})
        
        # 출석 기록도 삭제
        if delete_attendance:
            db.attendance.delete_many({"student_id": student_id})
        
        return jsonify({
            "success": True,
            "message": "학생이 삭제되었습니다"
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

# ===== 출석 관리 API =====
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """출석 기록 조회 - 프론트엔드 맞춤형 형식"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
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
            
            # 요청하신 형식으로 변환
            student_data = {
                "number": index,  # 번호 (1부터 시작)
                "name": student["name"],
                "student_id": int(student["student_id"]),  # 숫자로 변환
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
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

@app.route('/api/attendance/check', methods=['POST'])
def check_attendance():
    """출석 체크 - 타임어택 로직 수정"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": "요청 데이터가 없습니다"
            }), 400
        
        errors = validate_attendance_data(data)
        if errors:
            return jsonify({
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": ", ".join(errors)
            }), 400
        
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        student = db.students.find_one({"student_id": data['student_id']})
        if not student:
            return jsonify({
                "success": False,
                "error": "STUDENT_NOT_FOUND",
                "message": f"학생을 찾을 수 없습니다 (학번: {data['student_id']})"
            }), 404

        now = datetime.now()
        week_id = int(data['week'])
        student_id = int(data['student_id'])
        
        # 기존 기록 확인
        existing_record = db.attendance.find_one({
            "student_id": student_id,
            "week_id": week_id
        })
        
        # ★★★ 재인식 횟수 계산 ★★★
        if existing_record:
            # 기존 기록이 있으면 재인식
            current_count = existing_record.get("recheck_count", 0)
            recheck_count = current_count + 1
            first_check_time = existing_record.get("first_check_time")
            if first_check_time is None:
                first_check_time = now
            
	        is_first_check = False
        else:
            # 첫 인식
            recheck_count = 1  # 첫 인식 완료 = 1
            first_check_time = now
            is_first_check = True
        
        # ★★★ 수정된 타임어택 로직 ★★★
        # recheck_count 기준:
        # 1: 첫 인식 완료 → 타임어택 ❌ 없음
        # 2: 재인식 1회 → 타임어택 ⏰ 있음 (짝수, 15분)
        # 3: 재인식 2회 → 타임어택 ❌ 없음 (홀수)
        # 4: 재인식 3회 → 타임어택 ⏰ 있음 (짝수, 15분)
        # 5: 재인식 4회 → 타임어택 ❌ 없음 (홀수)
        
        status = "출석"
        
        if recheck_count == 1:
            # 첫 인식 완료
            message = "출석이 체크되었습니다 (첫 인식)"
            expires_at = None
            has_time_limit = False
            should_set_expires_at = False
        elif recheck_count % 2 == 0:  # 수정: 짝수일 때 타임어택 있음 (2,4,6...)
            # 짝수번째 재인식 → 타임어택 있음
            message = f"재인식되었습니다 (재인식 #{recheck_count}회) - 🚨 15분 내 재인식 필요!"
            expires_at = now + timedelta(minutes=15)
            has_time_limit = True
            should_set_expires_at = True
        else:  # 홀수일 때 (3,5,7...)
            # 홀수번째 재인식 → 타임어택 없음
            message = f"재인식되었습니다 (재인식 #{recheck_count}회) - 타임어택 해제됨"
            expires_at = None
            has_time_limit = False
            should_set_expires_at = False
        
        # ★★★ 디버그 로그 ★★★
        print(f"\n{'='*60}")
        print(f"🎯 출석 체크 - 수정된 타임어택 로직")
        print(f"{'='*60}")
        print(f"학생: {student_id}, 주차: {week_id}")
        print(f"기존 기록: {'있음' if existing_record else '없음'}")
        if existing_record:
            print(f"이전 recheck_count: {existing_record.get('recheck_count')}")
        print(f"새 recheck_count: {recheck_count}")
        print(f"홀수/짝수: {'홀수' if recheck_count % 2 == 1 else '짝수'}")
        print(f"첫 인식 여부: {is_first_check}")
        print(f"타임어택 계산: has_time_limit={has_time_limit}")
        print(f"expires_at 설정: {expires_at}")
        print(f"should_set_expires_at: {should_set_expires_at}")
        print(f"메시지: {message}")
        print(f"{'='*60}\n")
        
        # ★★★ 업데이트 데이터 준비 ★★★
        update_data = {
            "student_id": student_id,
            "week_id": week_id,
            "status": status,
            "date": now.strftime("%Y-%m-%d"),
            "timestamp": now,
            "is_auto_absent_processed": False,
            "recheck_count": recheck_count,
            "first_check_time": first_check_time,
            "recheck_time": now if existing_record else None,
            "last_updated": now,
            "notes": f"재인식 {recheck_count}회 - 패턴: {'짝수-타임어택' if has_time_limit else '홀수-해제' if recheck_count > 1 else '첫인식'}"
        }
        
        # ★★★ 업데이트 연산 구성 ★★★
        update_operation = {"$set": update_data}
        
        if should_set_expires_at:
            # 타임어택 있음: expires_at 설정
            update_operation["$set"]["expires_at"] = expires_at
        else:
            # 타임어택 없음: expires_at 필드 제거
            update_operation["$unset"] = {"expires_at": ""}
            
            # 혹시 set에 있다면 제거
            if "expires_at" in update_operation["$set"]:
                del update_operation["$set"]["expires_at"]
        
        # ★★★ MongoDB 업데이트 ★★★
        result = db.attendance.update_one(
            {"student_id": student_id, "week_id": week_id},
            update_operation,
            upsert=True
        )
        
        # ★★★ 응답 데이터 ★★★
        response_data = {
            "success": True, 
            "message": message,
            "data": {
                "student_id": student_id,
                "week_id": week_id,
                "status": status,
                "student_name": student["name"],
                "expires_at": expires_at.isoformat() if expires_at else None,
                "recheck_count": recheck_count,
                "has_time_limit": has_time_limit,
                "is_in_timelock": has_time_limit,
                "first_check_time": first_check_time.isoformat() if first_check_time else now.isoformat(),
                "pattern_info": {
                    "count": recheck_count,
                    "is_even": recheck_count % 2 == 0,
                    "should_have_timelock": has_time_limit,
                    "description": f"{recheck_count}회 - {'짝수(타임어택)' if has_time_limit else '홀수/첫인식(해제)'}"
                }
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ ERROR in check_attendance: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": "SERVER_ERROR", "message": str(e)}), 500
        
@app.route('/api/attendance/process-auto-absent', methods=['POST', 'GET'])
def process_auto_absent():
    """짝수번째 재인식(2,4,6...) 후 15분 내 재인식 없으면 결석 처리"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        now = datetime.now()
        
        # 만료된 타임어택 찾기
        expired_records = list(db.attendance.find({
            "status": "출석",
            "expires_at": {"$exists": True, "$lt": now},
            "is_auto_absent_processed": False
        }))
        
        print(f"🔍 처리 대상 레코드: {len(expired_records)}건")
        for record in expired_records:
            print(f"   - 학생: {record.get('student_id')}, 주차: {record.get('week_id')}, recheck_count: {record.get('recheck_count')}")
        
        processed_count = 0
        failed_count = 0
        
        for record in expired_records:
            try:
                recheck_count = record.get("recheck_count", 0)
                
                # 짝수번째 재인식인지 확인 (2,4,6...)
                if recheck_count > 1 and recheck_count % 2 == 0:
                    expires_at = record.get("expires_at")
                    
                    result = db.attendance.update_one(
                        {"_id": record["_id"]},
                        {
                            "$set": {
                                "status": "결석",
                                "is_auto_absent_processed": True,
                                "auto_processed_at": now,
                                "notes": f"{record.get('notes', '')}\n[⏰ {recheck_count}회차 타임어택 만료 ({expires_at}) → 자동 결석]"
                            }
                        }
                    )
                    
                    if result.modified_count > 0:
                        processed_count += 1
                        print(f"✅ 자동 결석 처리됨: 학생 {record.get('student_id')}, 주차 {record.get('week_id')}")
                    else:
                        failed_count += 1
                else:
                    print(f"⚠️ 조건 불일치: recheck_count={recheck_count} (짝수 아님)")
                        
            except Exception as e:
                print(f"❌ 처리 실패: {e}")
                failed_count += 1
        
        # 처리된 레코드 다시 확인
        if processed_count > 0:
            processed_records = list(db.attendance.find({
                "auto_processed_at": {"$exists": True, "$gte": now - timedelta(seconds=10)}
            }))
            print(f"📊 실제 처리 확인: {len(processed_records)}건")
        
        return jsonify({
            "success": True,
            "message": f"자동 결석 처리 완료",
            "data": {
                "total_expired": len(expired_records),
                "processed_count": processed_count,
                "failed_count": failed_count,
                "timestamp": now.isoformat(),
                "condition": "짝수번째 재인식(2,4,6...) 후 15분 내 재인식 없음"
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/attendance/recheck-status/<int:student_id>/<int:week>', methods=['GET'])
def get_recheck_status(student_id, week):
    """학생의 재인식 상태 확인"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        record = db.attendance.find_one({
            "student_id": student_id,
            "week_id": week
        })
        
        if not record:
            return jsonify({
                "success": True,
                "has_record": False,
                "message": "출석 기록이 없습니다"
            })
        
        now = datetime.now()
        expires_at = record.get("expires_at")
        recheck_count = record.get("recheck_count", 0)
        
        # ★★★ 타임어택 상태 계산 ★★★
        has_expires_at_field = expires_at is not None
        
        # 현재 활성 타임어택 여부
        has_active_timelock = False
        is_expired = False
        
        if expires_at:
            time_left = (expires_at - now).total_seconds()
            is_expired = time_left <= 0
            has_active_timelock = not is_expired
        
        # ★★★ 수정된 타임어택 계산 ★★★
        if recheck_count == 1:
            expected_has_timelock = False  # 첫 인식: 없음
        elif recheck_count % 2 == 0:  # 수정: 짝수일 때 있음
            expected_has_timelock = True   # 짝수: 있음
        else:
            expected_has_timelock = False  # 홀수: 없음
        
        return jsonify({
            "success": True,
            "has_record": True,
            "data": {
                "student_id": student_id,
                "week_id": week,
                "status": record["status"],
                "recheck_count": recheck_count,
                "is_first_check": recheck_count == 1,
                "has_expires_at_field": has_expires_at_field,
                "has_active_timelock": has_active_timelock,
                "expected_has_timelock": expected_has_timelock,
                "expires_at": expires_at.isoformat() if expires_at else None,
                "minutes_remaining": round(time_left / 60, 1) if expires_at and not is_expired else None,
                "is_expired": is_expired,
                "first_check_time": record.get("first_check_time", "").isoformat() if record.get("first_check_time") else None,
                "last_recheck_time": record.get("recheck_time", "").isoformat() if record.get("recheck_time") else None,
                "is_auto_absent_processed": record.get("is_auto_absent_processed", False)
            },
            "pattern_info": {
                "description": f"{recheck_count}회 - {'첫인식' if recheck_count == 1 else '짝수-타임어택' if recheck_count % 2 == 0 else '홀수-해제'}",
                "match": has_active_timelock == expected_has_timelock
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/debug/timelock-test', methods=['POST'])
def debug_timelock_test():
    """타임어택 디버깅 테스트"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        data = request.get_json()
        student_id = data.get('student_id', 2007720116)
        week = data.get('week', 1)
        
        # 현재 기록 확인
        record = db.attendance.find_one({
            "student_id": student_id,
            "week_id": week
        })
        
        test_scenarios = []
        
        # 다양한 recheck_count 시나리오 테스트
        for recheck_count in [1, 2, 3, 4, 5]:
            is_even = recheck_count % 2 == 0  # 수정: 짝수 체크
            
            if recheck_count == 1:
                expected_timelock = False
                desc = "첫인식-없음"
            elif is_even:  # 수정: 짝수일 때 타임어택 있음
                expected_timelock = True
                desc = f"짝수({recheck_count})-있음"
            else:
                expected_timelock = False
                desc = f"홀수({recheck_count})-없음"
            
            test_scenarios.append({
                "recheck_count": recheck_count,
                "is_even": is_even,
                "expected_timelock": expected_timelock,
                "description": desc
            })
        
        return jsonify({
            "success": True,
            "current_record": {
                "exists": record is not None,
                "recheck_count": record.get("recheck_count") if record else None,
                "expires_at": record.get("expires_at") if record else None,
                "has_timelock_field": "expires_at" in record if record else False
            },
            "timelock_logic": {
                "rule": "recheck_count 기준: 1=첫인식(없음), 짝수=있음, 홀수=없음",
                "examples": test_scenarios
            },
            "note": "타임어택은 recheck_count가 짝수(2,4,6...)일 때만 설정됨"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/debug/auto-process-status', methods=['GET'])
def debug_auto_process_status():
    """자동 처리 상태 디버깅"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        now = datetime.now()
        
        # 현재 상태 확인
        all_records = list(db.attendance.find({}))
        
        status_summary = {
            "total": len(all_records),
            "by_status": {},
            "with_expires_at": 0,
            "expired_not_processed": 0,
            "auto_processed": 0
        }
        
        for record in all_records:
            status = record.get("status", "unknown")
            status_summary["by_status"][status] = status_summary["by_status"].get(status, 0) + 1
            
            if "expires_at" in record:
                status_summary["with_expires_at"] += 1
                
                if record["expires_at"] < now and not record.get("is_auto_absent_processed", False):
                    status_summary["expired_not_processed"] += 1
            
            if record.get("is_auto_absent_processed", False):
                status_summary["auto_processed"] += 1
        
        # 만료되었지만 처리되지 않은 레코드
        expired_not_processed = list(db.attendance.find({
            "expires_at": {"$exists": True, "$lt": now},
            "is_auto_absent_processed": False
        }))
        
        return jsonify({
            "success": True,
            "summary": status_summary,
            "expired_not_processed": len(expired_not_processed),
            "now": now.isoformat(),
            "debug_info": {
                "query_condition": "expires_at < now AND is_auto_absent_processed = False",
                "match_count": len(expired_not_processed)
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/attendance/student/<student_id>', methods=['GET'])
def get_student_attendance(student_id):
    """학생별 출석 기록"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        # 학생 존재 확인
        student = db.students.find_one({"student_id": student_id})
        if not student:
            return jsonify({
                "success": False,
                "error": "STUDENT_NOT_FOUND",
                "message": "학생을 찾을 수 없습니다"
            }), 404
        
        # 학생의 출석 기록 조회
        attendance_data = list(db.attendance.find({"student_id": student_id}).sort("week_id", 1))
        
        result = []
        for record in attendance_data:
            attendance_record = {
                "id": str(record["_id"]),
                "week_id": record["week_id"],
                "status": record["status"],
                "date": record.get("date", ""),
                "notes": record.get("notes", ""),
                "timestamp": record.get("timestamp", "").isoformat() if record.get("timestamp") else ""
            }
            result.append(attendance_record)
        
        # 통계 계산
        total_weeks = 7
        present_count = sum(1 for record in attendance_data if record["status"] == "출석")
        attendance_rate = round((present_count / total_weeks) * 100, 2) if total_weeks > 0 else 0
        
        return jsonify({
            "success": True,
            "data": result,
            "student_info": {
                "student_id": student["student_id"],
                "name": student["name"],
                "major": student["major"]
            },
            "stats": {
                "total_weeks": total_weeks,
                "present_count": present_count,
                "attendance_rate": attendance_rate,
                "records_count": len(attendance_data)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

@app.route('/api/attendance/week/<int:week>', methods=['GET'])
def get_week_attendance(week):
    """주차별 출석 기록"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        # 해당 주차 출석 데이터 조회
        attendance_data = list(db.attendance.find({"week_id": week}))
        
        # 학생 정보 조회
        students = list(db.students.find().sort("student_id", 1))
        student_map = {s["student_id"]: s for s in students}
        
        # 결과 변환
        result = []
        for record in attendance_data:
            student_info = student_map.get(record["student_id"], {})
            attendance_record = {
                "id": str(record["_id"]),
                "student_id": record["student_id"],
                "student_name": student_info.get("name", "Unknown"),
                "department": student_info.get("major", "Unknown"),
                "status": record["status"],
                "date": record.get("date", ""),
                "notes": record.get("notes", ""),
                "timestamp": record.get("timestamp", "").isoformat() if record.get("timestamp") else ""
            }
            result.append(attendance_record)
        
        # 통계 계산
        total_students = len(students)
        present_count = sum(1 for record in attendance_data if record["status"] == "출석")
        attendance_rate = round((present_count / total_students) * 100, 2) if total_students > 0 else 0
        
        status_count = {}
        for record in attendance_data:
            status = record["status"]
            status_count[status] = status_count.get(status, 0) + 1
        
        return jsonify({
            "success": True,
            "data": result,
            "week": week,
            "stats": {
                "total_students": total_students,
                "present_count": present_count,
                "attendance_rate": attendance_rate,
                "status_count": status_count
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

# ===== 통계 API =====
@app.route('/api/stats/overview', methods=['GET'])
def get_overview_stats():
    """전체 통계"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        # 기본 통계
        total_students = db.students.count_documents({})
        total_attendance = db.attendance.count_documents({})
        total_weeks = 7
        
        # 주차별 통계
        weekly_stats = []
        for week in range(1, total_weeks + 1):
            week_attendance = list(db.attendance.find({"week_id": week}))
            present_count = sum(1 for record in week_attendance if record["status"] == "출석")
            week_rate = round((present_count / total_students) * 100, 2) if total_students > 0 else 0
            
            weekly_stats.append({
                "week": week,
                "present_count": present_count,
                "attendance_rate": week_rate
            })
        
        # 상태별 통계
        status_stats = {}
        all_attendance = list(db.attendance.find())
        for record in all_attendance:
            status = record["status"]
            status_stats[status] = status_stats.get(status, 0) + 1
        
        return jsonify({
            "success": True,
            "data": {
                "total_students": total_students,
                "total_attendance_records": total_attendance,
                "total_weeks": total_weeks,
                "weekly_stats": weekly_stats,
                "status_stats": status_stats
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

@app.route('/api/stats/weekly', methods=['GET'])
def get_weekly_stats():
    """주차별 통계"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        total_students = db.students.count_documents({})
        total_weeks = 7
        
        weekly_stats = []
        for week in range(1, total_weeks + 1):
            week_attendance = list(db.attendance.find({"week_id": week}))
            
            status_count = {}
            for record in week_attendance:
                status = record["status"]
                status_count[status] = status_count.get(status, 0) + 1
            
            present_count = status_count.get("출석", 0)
            week_rate = round((present_count / total_students) * 100, 2) if total_students > 0 else 0
            
            weekly_stats.append({
                "week": week,
                "present_count": present_count,
                "attendance_rate": week_rate,
                "status_count": status_count
            })
        
        return jsonify({
            "success": True,
            "data": weekly_stats
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

@app.route('/api/stats/student/<student_id>', methods=['GET'])
def get_student_stats(student_id):
    """학생별 통계"""
    try:
        db = get_db()
        if db is None:
            return jsonify({"success": False, "error": "DATABASE_ERROR"}), 500
        
        # 학생 존재 확인
        student = db.students.find_one({"student_id": student_id})
        if not student:
            return jsonify({
                "success": False,
                "error": "STUDENT_NOT_FOUND",
                "message": "학생을 찾을 수 없습니다"
            }), 404
        
        # 학생의 출석 기록
        attendance_data = list(db.attendance.find({"student_id": student_id}))
        total_weeks = 7
        
        # 주차별 상태 매핑
        weekly_status = {}
        for record in attendance_data:
            weekly_status[record["week_id"]] = record["status"]
        
        # 전체 주차에 대한 상태 채우기
        all_weekly_stats = []
        for week in range(1, total_weeks + 1):
            status = weekly_status.get(week, "결석")
            all_weekly_stats.append({
                "week": week,
                "status": status
            })
        
        # 통계 계산
        present_count = sum(1 for week in all_weekly_stats if week["status"] == "출석")
        attendance_rate = round((present_count / total_weeks) * 100, 2)
        
        status_count = {}
        for week in all_weekly_stats:
            status = week["status"]
            status_count[status] = status_count.get(status, 0) + 1
        
        return jsonify({
            "success": True,
            "data": {
                "student_info": {
                    "student_id": student["student_id"],
                    "name": student["name"],
                    "major": student["major"]
                },
                "attendance_rate": attendance_rate,
                "present_count": present_count,
                "total_weeks": total_weeks,
                "weekly_stats": all_weekly_stats,
                "status_count": status_count
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": "DATABASE_ERROR", "message": str(e)}), 500

# ===== 기타 API =====
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "attendance-system",
        "timestamp": datetime.now().isoformat()
    })

# 404 에러 핸들러
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "message": "요청한 API 엔드포인트를 찾을 수 없습니다",
        "available_endpoints": [
            "GET /",
            "GET /api/test-db",
            "POST /api/init-db",
            "GET /api/students",
            "GET /api/students/{student_id}",
            "POST /api/students",
            "PUT /api/students/{student_id}",
            "DELETE /api/students/{student_id}",
            "GET /api/attendance",
            "POST /api/attendance/check",
            "GET /api/attendance/student/{student_id}",
            "GET /api/attendance/week/{week}",
            "GET /api/stats/overview",
            "GET /api/stats/weekly",
            "GET /api/stats/student/{student_id}",
            "GET /health"
        ]
    }), 404

# Vercel에서 필요
if __name__ == '__main__':
    app.run(debug=True)
