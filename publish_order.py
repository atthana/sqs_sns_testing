import boto3
import json
import uuid

# ใส่ ARN ของ SNS Topic ที่จดไว้
SNS_TOPIC_ARN = 'arn:aws:sns:ap-southeast-7:154230581564:TestOrderCreatedTopic'

def publish_order():
    sns = boto3.client('sns', region_name='ap-southeast-7') # เปลี่ยน region ตามของคุณ
    
    # จำลองข้อมูลออเดอร์
    order_data = {
        "order_id": str(uuid.uuid4()),
        "item": "Mechanical Keyboard",
        "quantity": 1,
        "customer_email": "q_electronics@hotmail.com"
    }

    # ส่งข้อความเข้า SNS
    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=json.dumps(order_data),
        Subject="New Order Created by GR"
    )

    print(f"✅ สร้างออเดอร์สำเร็จ! Message ID: {response['MessageId']}")
    print(f"ข้อมูล: {order_data}")

if __name__ == '__main__':
    publish_order()