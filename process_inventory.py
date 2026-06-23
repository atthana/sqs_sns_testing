import boto3
import json
import time
import config

def process_queue():
    sqs = boto3.client(
        'sqs',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )
    
    print("⏳ รอรับงานจาก Inventory Queue...")
    
    while True:
        # ดึงข้อความจากคิว (Long Polling รอ 10 วินาทีเพื่อประหยัดทรัพยากร)
        response = sqs.receive_message(
            QueueUrl=config.SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10 
        )

        messages = response.get('Messages', [])
        
        if not messages:
            continue
            
        for message in messages:
            # SNS จะส่ง Message มาในรูปแบบ JSON ซ้อน JSON ต้อง Extract ออกมา
            sns_body = json.loads(message['Body'])
            order_data = json.loads(sns_body['Message'])
            
            print(f"\n📦 กำลังตัดสต็อกสำหรับ Order ID: {order_data['order_id']}")
            print(f"สินค้า: {order_data['item']} จำนวน: {order_data['quantity']}")
            
            # จำลองการใช้เวลาประมวลผล
            time.sleep(2)
            print("✅ ตัดสต็อกเสร็จสิ้น!")

            # ต้องลบข้อความออกจากคิวเมื่อทำงานเสร็จ ไม่งั้นข้อความจะเด้งกลับมาทำซ้ำ
            sqs.delete_message(
                QueueUrl=config.SQS_QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
            print("🗑️ ลบข้อความออกจากคิวแล้ว")

if __name__ == '__main__':
    process_queue()