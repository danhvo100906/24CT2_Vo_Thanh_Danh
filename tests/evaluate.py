import io
import json
import os
import sys
from collections import defaultdict

if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODEL_DIR = os.path.join(PROJECT_ROOT, 'framework', 'src', 'model')
PROCESSING_DIR = os.path.join(PROJECT_ROOT, 'framework', 'src', 'processing')

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)
if PROCESSING_DIR not in sys.path:
    sys.path.insert(0, PROCESSING_DIR)

from chatbot import get_response_details
from retrieval import search_materials


def evaluate_intents(test_file):
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    correct = 0

    y_true = []
    y_pred = []
    confusion = defaultdict(lambda: defaultdict(int))
    all_tags = set()

    for item in data:
        q = item['question']
        expected = item['expected_intent']
        res = get_response_details(q)
        pred = res['intent']

        y_true.append(expected)
        y_pred.append(pred)
        all_tags.add(expected)
        all_tags.add(pred)
        confusion[expected][pred] += 1

        if pred == expected:
            correct += 1

    accuracy = correct / total if total > 0 else 0.0

    # Tinh Precision, Recall, F1 theo tung class
    metrics_per_class = {}
    macro_prec = []
    macro_rec = []
    macro_f1 = []

    for tag in sorted(all_tags):
        tp = confusion[tag][tag]
        fp = sum(confusion[other][tag] for other in all_tags if other != tag)
        fn = sum(confusion[tag][other] for other in all_tags if other != tag)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        metrics_per_class[tag] = {
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "support": tp + fn
        }

        if tp + fn > 0:  # Chi tinh macro tren cac class co trong test set
            macro_prec.append(prec)
            macro_rec.append(rec)
            macro_f1.append(f1)

    avg_prec = sum(macro_prec) / len(macro_prec) if macro_prec else 0.0
    avg_rec = sum(macro_rec) / len(macro_rec) if macro_rec else 0.0
    avg_f1 = sum(macro_f1) / len(macro_f1) if macro_f1 else 0.0

    return {
        "total_samples": total,
        "correct_samples": correct,
        "accuracy": round(accuracy, 4),
        "macro_precision": round(avg_prec, 4),
        "macro_recall": round(avg_rec, 4),
        "macro_f1": round(avg_f1, 4),
        "class_metrics": metrics_per_class,
        "confusion_matrix": {k: dict(v) for k, v in confusion.items()}
    }


def evaluate_retrieval(test_file):
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    top1_correct = 0
    top3_correct = 0
    top5_correct = 0

    for item in data:
        q = item['question']
        expected_subject = item['expected_subject']
        results = search_materials(q)

        codes = [r.get('code') for r in results]

        if codes and codes[0] == expected_subject:
            top1_correct += 1
        if expected_subject in codes[:3]:
            top3_correct += 1
        if expected_subject in codes[:5]:
            top5_correct += 1

    return {
        "total_queries": total,
        "top1_accuracy": round(top1_correct / total, 4) if total > 0 else 0.0,
        "top3_accuracy": round(top3_correct / total, 4) if total > 0 else 0.0,
        "top5_accuracy": round(top5_correct / total, 4) if total > 0 else 0.0
    }


def evaluate_out_of_scope(test_file):
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    rejected_count = 0

    for item in data:
        q = item['question']
        res = get_response_details(q)
        # Out of scope duoc tinh la thanh cong khi nhan dien dung tag 'out_of_scope' hoac tra ve status 'fallback' / 'out_of_scope'
        if res['intent'] == 'out_of_scope' or res['status'] in ['out_of_scope', 'fallback']:
            rejected_count += 1

    return {
        "total_samples": total,
        "rejected_count": rejected_count,
        "rejection_rate": round(rejected_count / total, 4) if total > 0 else 0.0
    }


def main():
    print("=" * 65)
    print("📊 BẮT ĐẦU ĐÁNH GIÁ CHỈ SỐ TOÀN DIỆN HỆ THỐNG STUDYBOT")
    print("=" * 65)

    intents_eval = evaluate_intents(os.path.join(BASE_DIR, 'test_intents.json'))
    retrieval_eval = evaluate_retrieval(os.path.join(BASE_DIR, 'test_retrieval.json'))
    oos_eval = evaluate_out_of_scope(os.path.join(BASE_DIR, 'test_out_of_scope.json'))

    print("\n1. KẾT QUẢ ĐÁNH GIÁ PHÂN LOẠI Ý ĐỊNH (INTENT CLASSIFICATION):")
    print(f"- Tổng số mẫu kiểm thử: {intents_eval['total_samples']}")
    print(f"- Số câu dự đoán chính xác: {intents_eval['correct_samples']}")
    print(f"- Độ chính xác (Accuracy): {intents_eval['accuracy'] * 100:.2f}%")
    print(f"- Macro Precision: {intents_eval['macro_precision'] * 100:.2f}%")
    print(f"- Macro Recall: {intents_eval['macro_recall'] * 100:.2f}%")
    print(f"- Macro F1-Score: {intents_eval['macro_f1'] * 100:.2f}%")

    print("\nChi tiết F1-Score theo từng Intent:")
    print(f"{'Intent Tag':<25} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'Số mẫu':<8}")
    print("-" * 75)
    for tag, m in intents_eval['class_metrics'].items():
        if m['support'] > 0:
            print(f"{tag:<25} | {m['precision']*100:>8.1f}% | {m['recall']*100:>8.1f}% | {m['f1_score']*100:>8.1f}% | {m['support']:>6}")

    print("\n2. KẾT QUẢ ĐÁNH GIÁ TRUY XUẤT TÀI LIỆU (DOCUMENT RETRIEVAL):")
    print(f"- Tổng số câu truy vấn tài liệu: {retrieval_eval['total_queries']}")
    print(f"- Retrieval Top-1 Accuracy: {retrieval_eval['top1_accuracy'] * 100:.2f}%")
    print(f"- Retrieval Top-3 Accuracy: {retrieval_eval['top3_accuracy'] * 100:.2f}%")
    print(f"- Retrieval Top-5 Accuracy: {retrieval_eval['top5_accuracy'] * 100:.2f}%")

    print("\n3. KẾT QUẢ ĐÁNH GIÁ CÂU HỎI NGOÀI PHẠM VI (OUT-OF-SCOPE REJECTION):")
    print(f"- Tổng số câu ngoài phạm vi: {oos_eval['total_samples']}")
    print(f"- Số câu nhận diện/từ chối đúng: {oos_eval['rejected_count']}")
    print(f"- Tỷ lệ từ chối an toàn (Rejection Rate): {oos_eval['rejection_rate'] * 100:.2f}%")

    # Bảng tổng hợp
    summary_table = {
        "intent_accuracy": intents_eval['accuracy'],
        "intent_precision": intents_eval['macro_precision'],
        "intent_recall": intents_eval['macro_recall'],
        "intent_f1": intents_eval['macro_f1'],
        "retrieval_top1": retrieval_eval['top1_accuracy'],
        "retrieval_top3": retrieval_eval['top3_accuracy'],
        "retrieval_top5": retrieval_eval['top5_accuracy'],
        "out_of_scope_accuracy": oos_eval['rejection_rate']
    }

    results_file = os.path.join(BASE_DIR, 'evaluation_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "summary": summary_table,
            "intents_detailed": intents_eval,
            "retrieval_detailed": retrieval_eval,
            "oos_detailed": oos_eval
        }, f, ensure_ascii=False, indent=4)

    print("\n" + "=" * 65)
    print(f"✅ Đã lưu báo cáo đánh giá chi tiết vào: {results_file}")
    print("=" * 65)


if __name__ == '__main__':
    main()
