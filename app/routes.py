from framework.src.processing import calculate_grade

def process_student_data(student_name, scores):
    """Gọi logic tính toán từ framework và đóng gói dữ liệu trả về"""
    avg, rank = calculate_grade(scores)
    return {
        "name": student_name,
        "average": avg,
        "rank": rank
    }