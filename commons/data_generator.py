import json
import random
from faker import Faker

# สร้าง instance ของ Faker
fake = Faker()

# รายชื่อสาขา (branches) และช่องทาง (channels) ตัวอย่าง
branches = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
channels = ["Website", "Mobile App", "In-store", "Email", "Social Media"]

def generate_feedback(num_feedbacks):
    feedback_list = []
    
    for _ in range(num_feedbacks):
        feedback = {
            "customer_name": fake.name(),
            "customer_email": fake.email(),
            "feedback": fake.sentence(nb_words=random.randint(5, 20)),
            "rating": random.randint(1, 5),  # คะแนนจาก 1 ถึง 5
            "timestamp": fake.date_time_this_year().isoformat(),  # เวลาในปีนี้
            "branch": random.choice(branches),  # สุ่มเลือกสาขาจากรายชื่อ
            "channel": random.choice(channels),  # สุ่มเลือกช่องทางจากรายชื่อ
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat()  # สุ่มวันเกิดระหว่าง 18 ถึง 65 ปี
        }
        feedback_list.append(feedback)

    return feedback_list

def main():
    num_feedbacks = int(input("Enter the number of customer feedbacks to generate: "))
    feedback_data = generate_feedback(num_feedbacks)

    # บันทึกข้อมูลลงในไฟล์ JSON
    with open('customer_feedback.json', 'w') as json_file:
        json.dump(feedback_data, json_file, indent=4)

    print(f"Generated {num_feedbacks} feedback records and saved to 'customer_feedback.json'.")

if __name__ == "__main__":
    main()
