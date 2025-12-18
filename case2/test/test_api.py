import json

import requests

BASE_URL = "http://localhost:8000"


def test_health():
    print("TEST 1: Health Check")

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_prediction():
    print("TEST 2: Individual Prediction")

    student_data = {
        "hours_studied": 7.0,
        "previous_scores": 85.0,
        "extracurricular_activities": 1,
        "sleep_hours": 7.5,
        "sample_questions_practiced": 5,
    }

    response = requests.post(f"{BASE_URL}/api/v1/predictions/", json=student_data)

    print(f"Status: {response.status_code}")
    print(f"Request: {json.dumps(student_data, indent=2)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_create_student():
    print("TEST 3: Create Student")

    student = {
        "student_id": "TEST001",
        "name": "Juan Pérez",
        "input_data": {
            "hours_studied": 6.0,
            "previous_scores": 75.0,
            "extracurricular_activities": 1,
            "sleep_hours": 7.0,
            "sample_questions_practiced": 4,
        },
    }

    response = requests.post(f"{BASE_URL}/api/v1/students/", json=student)

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
    assert response.status_code == 201

    return student["student_id"]


def test_get_student(student_id):
    print("TEST 4: Get Student")

    response = requests.get(f"{BASE_URL}/api/v1/students/{student_id}")

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
    assert response.status_code == 200


def test_list_students():
    print("TEST 5: List Students")

    response = requests.get(f"{BASE_URL}/api/v1/students/")

    print(f"Status: {response.status_code}")
    print(f"Total students: {len(response.json())}")
    assert response.status_code == 200


def test_update_student(student_id):
    print("TEST 6: Update Student")

    update_data = {
        "input_data": {
            "hours_studied": 8.0,
            "previous_scores": 90.0,
            "extracurricular_activities": 1,
            "sleep_hours": 8.0,
            "sample_questions_practiced": 7,
        }
    }

    response = requests.put(
        f"{BASE_URL}/api/v1/students/{student_id}", json=update_data
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
    assert response.status_code == 200


def test_statistics():
    print("TEST 7: Statistics")

    response = requests.get(f"{BASE_URL}/api/v1/students/stats/summary")

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_delete_student(student_id):
    print("TEST 8: Delete Student")

    response = requests.delete(f"{BASE_URL}/api/v1/students/{student_id}")

    print(f"Status: {response.status_code}")
    assert response.status_code == 204


def test_batch_prediction():
    print("TEST 9: Batch Prediction")

    students = [
        {
            "hours_studied": 7.0,
            "previous_scores": 85.0,
            "extracurricular_activities": 1,
            "sleep_hours": 7.5,
            "sample_questions_practiced": 5,
        },
        {
            "hours_studied": 3.0,
            "previous_scores": 55.0,
            "extracurricular_activities": 0,
            "sleep_hours": 5.0,
            "sample_questions_practiced": 1,
        },
    ]

    response = requests.post(f"{BASE_URL}/api/v1/predictions/batch", json=students)

    print(f"Status: {response.status_code}")
    print(f"Students processed: {len(response.json())}")
    for i, pred in enumerate(response.json(), 1):
        print(f"\nStudent {i}:")
        print(f"Performance: {pred['performance_index_predicted']}")
        print(f"Risk: {pred['risk_level']}")

    assert response.status_code == 200


def run_all_tests():
    try:
        test_health()
        test_prediction()
        student_id = test_create_student()
        test_get_student(student_id)
        test_list_students()
        test_update_student(student_id)
        test_statistics()
        test_batch_prediction()
        test_delete_student(student_id)

        print("All tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\nConnection error. Is the API running at http://localhost:8000?")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    run_all_tests()
