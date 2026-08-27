def calculate_grade(scores):
    """Tính điểm trung bình và xếp loại sinh viên"""
    if not scores:
        return 0, "F"
    
    avg = sum(scores) / len(scores)
    
    if avg >= 8.5:
        rank = "Xuất sắc"
    elif avg >= 7.0:
        rank = "Khá"
    elif avg >= 5.0:
        rank = "Trung bình"
    else:
        rank = "Yếu"
        
    return round(avg, 2), rank