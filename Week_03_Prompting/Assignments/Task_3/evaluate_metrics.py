import csv
import hashlib
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path


TASK = Path(__file__).resolve().parent
DATA = TASK.parent / 'Task_2' / 'data'
sys.path.insert(0, str(DATA))
from evaluate_retrieval_predictions import load_database


def result_precision(expected, predicted):
    if not predicted:
        return 1.0 if not expected else 0.0
    expected_rows = Counter(tuple(row) for row in expected)
    predicted_rows = Counter(tuple(row) for row in predicted)
    matches = sum((expected_rows & predicted_rows).values())
    return matches / len(predicted)


def evaluate():
    csv.field_size_limit(1_000_000_000)
    with (DATA / 'restaurants_dataset.csv').open(encoding='utf-8-sig', newline='') as source:
        labels = list(csv.DictReader(source))
    expected_questions = [row['question'] for row in labels]
    connection = load_database()
    connection.execute('PRAGMA query_only = ON')
    results = {}
    try:
        for name in ('RISE', 'RACE', 'CAR'):
            filename = DATA / f'restaurants_dataset_predictions_{name}.csv'
            with filename.open(encoding='utf-8-sig', newline='') as source:
                predictions = list(csv.DictReader(source))
            if [row['question'] for row in predictions] != expected_questions:
                raise ValueError(f'{name}: missing, reordered or changed questions')
            details = []
            for label, prediction in zip(labels, predictions):
                expected = json.loads(label['result'])
                if not isinstance(expected, list):
                    raise ValueError('Expected result must be a list')
                sql = prediction['predicted_sql'].strip()
                error = None
                try:
                    if not sql.upper().startswith(('SELECT', 'WITH')):
                        raise sqlite3.OperationalError('Expected a SELECT query')
                    predicted = connection.execute(sql).fetchall()
                    correct = Counter(map(tuple, expected)) == Counter(map(tuple, predicted))
                    precision = result_precision(expected, predicted)
                except sqlite3.Error as exception:
                    predicted = []
                    correct = False
                    precision = 0.0
                    error = str(exception)
                details.append({
                    'question': label['question'],
                    'correct': correct,
                    'precision': precision,
                    'expected_rows': len(expected),
                    'predicted_rows': len(predicted),
                    'sql_error': error,
                })
            total = len(details)
            if total == 0:
                raise ValueError('No questions')
            correct = sum(row['correct'] for row in details)
            results[name] = {
                'prediction_file': f'../Task_2/data/{filename.name}',
                'prediction_sha256': hashlib.sha256(filename.read_bytes()).hexdigest(),
                'total': total,
                'correct': correct,
                'accuracy': correct / total,
                'mean_result_precision': sum(row['precision'] for row in details) / total,
                'partial_matches': sum(0 < row['precision'] < 1 for row in details),
                'sql_errors': sum(row['sql_error'] is not None for row in details),
                'questions': details,
            }
    finally:
        connection.close()
    return results


def main():
    results = evaluate()
    output = {
        'metric': 'Mean per-question result precision, using row multisets',
        'formula': 'Precision = matched rows / predicted rows',
        'empty_results': 'Both empty: 1; only one empty: 0; SQL error: 0',
        'runs': results,
    }
    (TASK / 'metrics.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    for name, result in results.items():
        print(f"{name}: accuracy={result['accuracy']:.2%}, mean precision={result['mean_result_precision']:.2%}")


if __name__ == '__main__':
    main()
