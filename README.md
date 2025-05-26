# Invoice Processor

A Flask-based web application that monitors a specified folder for Excel invoice files, extracts customer details (name, phone number, amount), and sends WhatsApp messages with UPI payment links using the Twilio API. Designed for businesses like pharmacies to automate invoice notifications and payment collection.

## Features
- **Folder Monitoring**: Automatically detects new Excel files (`.xlsx`, `.xls`) in a user-specified folder.
- **Customizable Columns**: Users can specify Excel column names for customer name, phone number, and amount via a web interface.
- **WhatsApp Notifications**: Sends payment requests with UPI links (e.g., Google Pay) via Twilio's WhatsApp API.
- **Processed File Tracking**: Marks processed files with a `.processed` flag to prevent reprocessing.
- **Retry Logic**: Retries failed message sends up to three times.
- **Responsive UI**: Professional, Tailwind CSS-styled web interface for configuring the folder and columns.

## Use Cases
1. **Pharmacy Billing**:
   - **Scenario**: A pharmacy generates daily Excel invoices with customer details and amounts owed for medications.
   - **Usage**: The app monitors the invoice folder, extracts customer name, phone number, and amount, and sends a WhatsApp message with a UPI payment link (e.g., `upi://pay?...`) for quick payment via Google Pay or similar apps.
   - **Benefit**: Automates payment reminders, reducing manual follow-ups and improving cash flow.

2. **Small Business Invoicing**:
   - **Scenario**: A retail shop or service provider creates Excel invoices for customers and wants to notify them for payments.
   - **Usage**: The app processes invoices, sends payment links to customers via WhatsApp, and tracks processed files to avoid duplicates.
   - **Benefit**: Streamlines payment collection for small businesses with limited staff.

3. **Subscription or Recurring Payments**:
   - **Scenario**: A business with recurring customer payments (e.g., monthly medical supplies) maintains an Excel sheet with payment details.
   - **Usage**: The app monitors for updated Excel files and sends payment reminders to customers.
   - **Benefit**: Ensures timely notifications for recurring payments, improving customer compliance.

4. **Bulk Payment Requests**:
   - **Scenario**: A business needs to send payment requests to multiple customers at once (e.g., after a bulk sale).
   - **Usage**: Drop an Excel file with customer details into the monitored folder, and the app sends WhatsApp messages to all listed customers.
   - **Benefit**: Saves time on manual messaging for bulk transactions.

## Installation

### Prerequisites
- Python 3.8+
- Git
- Twilio account with WhatsApp enabled (sandbox or purchased number)
- A UPI ID (e.g., for Google Pay)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/invoice-processor.git
   cd invoice-processor
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root:
   ```
   UPI_ID=your_upi_id@upi
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```
   - Replace `your_upi_id@upi` with your UPI ID (e.g., `yourname@okhdfcbank`).
   - Get `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` from the Twilio Console (https://console.twilio.com).
   - Use the Twilio WhatsApp sandbox number (`whatsapp:+14155238886`) for testing, or a purchased number.

5. **Ensure Folder Structure**:
   ```
   invoice-processor/
   ├── .env
   ├── .gitignore
   ├── app.py
   ├── requirements.txt
   ├── templates/
   │   └── index.html
   ├── .venv/
   └── .git/
   ```

## Usage
1. **Run the Application**:
   ```bash
   python app.py
   ```
   Open `http://localhost:5000` in a browser.

2. **Configure via Web Interface**:
   - **Folder Path**: Enter the absolute path to the folder containing Excel invoices (e.g., `/home/user/invoices` or `C:\invoices`).
   - **Column Names**: Specify Excel column names for customer name, phone number, and amount (defaults: `Customer_Name`, `Phone_Number`, `Amount`).
   - Click **Start Monitoring** to watch the folder and process existing unprocessed files.
   - Click **Stop Monitoring** to pause the process.

3. **Prepare Excel Files**:
   - Create Excel files (`.xlsx` or `.xls`) with columns matching the specified names.
   - Example:
     ```
     Customer_Name | Phone_Number | Amount
     John Doe      | +919876543210 | 500.00
     Jane Smith    | 9123456789    | 750.00
     ```
   - Place files in the monitored folder. Phone numbers without `+91` will have it added automatically.

4. **Twilio WhatsApp Setup**:
   - For the sandbox (`whatsapp:+14155238886`), recipients must send `join <sandbox-code>` to opt in (check Twilio Console for the code).
   - Messages include a UPI payment link (`upi://pay?...`) that opens a UPI app on mobile devices.

5. **Verify Operation**:
   - The app marks processed files with a `.processed` flag.
   - Check the console for logs (e.g., "Message sent to John Doe (+919876543210)").
   - Status/error messages appear in the UI.

## Project Structure
- `app.py`: Flask backend handling folder monitoring, Excel processing, and Twilio WhatsApp messaging.
- `templates/index.html`: Web interface styled with Tailwind CSS for configuring the folder and columns.
- `.env`: Stores sensitive configuration (UPI ID, Twilio credentials).
- `.gitignore`: Excludes `.env`, Excel files, `.processed` flags, and virtual environment.
- `requirements.txt`: Lists Python dependencies.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request on GitHub.

## License
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT OWNERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.