from flask import Flask, request, render_template, jsonify
import os
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from twilio.rest import Client
import urllib.parse
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
UPI_ID = os.getenv("UPI_ID")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
MAX_RETRIES = 3


# Global variables for monitoring
observer = None
monitoring_thread = None
config = {
    "folder_path": None,
    "customer_name_col": "Customer_Name",
    "phone_number_col": "Phone_Number",
    "amount_col": "Amount"
}

class InvoiceHandler(FileSystemEventHandler):
    def __init__(self, customer_name_col, phone_number_col, amount_col):
        self.customer_name_col = customer_name_col
        self.phone_number_col = phone_number_col
        self.amount_col = amount_col

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.xlsx', '.xls')):
            print(f"New file detected: {event.src_path}")
            process_invoice(event.src_path, self.customer_name_col, self.phone_number_col, self.amount_col)

def process_invoice(file_path, customer_name_col, phone_number_col, amount_col, retry_count=0):
    processed_flag = f"{file_path}.processed"
    if os.path.exists(processed_flag):
        print(f"File {file_path} already processed, skipping.")
        return
    
    try:
        df = pd.read_excel(file_path)
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        all_messages_sent = True

        for index, row in df.iterrows():
            customer_name = row[customer_name_col]
            phone_number = str(row[phone_number_col])
            amount = float(row[amount_col])
            
            if not phone_number.startswith('+'):
                phone_number = f"+91{phone_number}"  # Adjust country code as needed
            
            payment_link = generate_payment_link(customer_name, amount)
            success = send_whatsapp_message(client, phone_number, customer_name, amount, payment_link)
            if not success:
                all_messages_sent = False
        
        if all_messages_sent:
            with open(processed_flag, 'w') as f:
                f.write("Processed")
            print(f"Marked {file_path} as processed.")
        else:
            if retry_count < MAX_RETRIES:
                print(f"Retrying {file_path} (Attempt {retry_count + 1}/{MAX_RETRIES})")
                time.sleep(5)
                process_invoice(file_path, customer_name_col, phone_number_col, amount_col, retry_count + 1)
            else:
                print(f"Max retries reached for {file_path}. Failed to send all messages.")
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        if retry_count < MAX_RETRIES:
            print(f"Retrying {file_path} (Attempt {retry_count + 1}/{MAX_RETRIES})")
            time.sleep(5)
            process_invoice(file_path, customer_name_col, phone_number_col, amount_col, retry_count + 1)
        else:
            print(f"Max retries reached for {file_path}. Error: {e}")

def generate_payment_link(customer_name, amount):
    params = {
        'pa': UPI_ID,
        'pn': customer_name,
        'am': amount,
        'cu': 'INR',
        'tn': f'Invoice Payment for {customer_name}'
    }
    query = urllib.parse.urlencode(params)
    return f"upi://pay?{query}"

def send_whatsapp_message(client, phone_number, customer_name, amount, payment_link):
    try:
        message_body = (
            f"Hello {customer_name},\n"
            f"Your invoice amount is ₹{amount:.2f}.\n"
            f"Please click the link to pay now: {payment_link}"
        )
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=f"whatsapp:{phone_number}"
        )
        print(f"Message sent to {customer_name} ({phone_number}), SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending WhatsApp message to {phone_number}: {e}")
        return False

def check_existing_files(folder_path, customer_name_col, phone_number_col, amount_col):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(('.xlsx', '.xls')) and not os.path.exists(f"{file_path}.processed"):
            print(f"Found unprocessed file: {file_path}")
            process_invoice(file_path, customer_name_col, phone_number_col, amount_col)

def start_monitoring(folder_path, customer_name_col, phone_number_col, amount_col):
    global observer
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    check_existing_files(folder_path, customer_name_col, phone_number_col, amount_col)
    event_handler = InvoiceHandler(customer_name_col, phone_number_col, amount_col)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    print(f"Monitoring folder: {folder_path}")

def stop_monitoring():
    global observer
    if observer:
        observer.stop()
        observer.join()
        print("Monitoring stopped")
        observer = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global monitoring_thread, config
    folder_path = request.form.get('folder_path')
    customer_name_col = request.form.get('customer_name_col') or "Customer_Name"
    phone_number_col = request.form.get('phone_number_col') or "Phone_Number"
    amount_col = request.form.get('amount_col') or "Amount"
    
    if not folder_path:
        return jsonify({"status": "error", "message": "Folder path is required"})
    
    config.update({
        "folder_path": folder_path,
        "customer_name_col": customer_name_col,
        "phone_number_col": phone_number_col,
        "amount_col": amount_col
    })
    
    stop_monitoring()
    monitoring_thread = threading.Thread(
        target=start_monitoring,
        args=(folder_path, customer_name_col, phone_number_col, amount_col)
    )
    monitoring_thread.daemon = True
    monitoring_thread.start()
    
    return jsonify({"status": "success", "message": f"Monitoring started for {folder_path}"})

@app.route('/stop', methods=['POST'])
def stop():
    stop_monitoring()
    return jsonify({"status": "success", "message": "Monitoring stopped"})

if __name__ == "__main__":
    app.run(debug=True)