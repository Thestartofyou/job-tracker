import datetime
import requests

class Job:
    def __init__(self, job_id, customer_name, job_description, job_cost):
        self.job_id = job_id
        self.customer_name = customer_name
        self.job_description = job_description
        self.job_cost = job_cost
        self.date = datetime.datetime.now()

class JobTracker:
    def __init__(self):
        self.jobs = []
        self.next_job_id = 1

    def add_job(self, customer_name, job_description, job_cost):
        job = Job(self.next_job_id, customer_name, job_description, job_cost)
        self.jobs.append(job)
        self.next_job_id += 1
        return job

    def get_jobs(self):
        return self.jobs

    def send_payment_request(self, job, phone_number):
        message = f"Hi {job.customer_name}, the job you requested on {job.date} with a cost of {job.job_cost} is now due for payment. Please make payment to the following account number: XXXXXXXX. Thank you!"
        response = requests.post(
            'https://api.twilio.com/2010-04-01/Accounts/<YOUR_TWILIO_ACCOUNT_SID>/Messages.json',
            auth=('YOUR_TWILIO_ACCOUNT_SID', 'YOUR_TWILIO_AUTH_TOKEN'),
            data={
                'From': '<YOUR_TWILIO_PHONE_NUMBER>',
                'To': phone_number,
                'Body': message
            }
        )

        if response.status_code == 201:
            return True
        else:
            return False

# Create a JobTracker object
job_tracker = JobTracker()

# Add a new job
job = job_tracker.add_job("John Smith", "Fix leaking faucet", 50)

# Send payment request for the job to customer's phone number
job_sent = job_tracker.send_payment_request(job, "+1234567890")

if job_sent:
    print("Payment request sent successfully!")
else:
    print("Failed to send payment request.")
