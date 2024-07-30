# Payroll Service Development

## Project Description

The Payroll Service Development project is designed to provide a comprehensive solution for managing employee data, leave requests, and payroll in a streamlined and efficient manner. The system includes user management, employee management, leave management, payroll management, and comprehensive review and documentation modules.

## Features

### 1. User Management & Employee Management
- **User Registration & Sign-In:** Allows users to register and log in to the system.
- **Role-Based Access Control:** Renders data based on user roles (e.g., admin, employee).
- **Employee Database:** Stores comprehensive information about each employee, including personal details, contact information, and employment history.
- **Employee Status Tracking:** Tracks and manages employee status such as active or inactive.

### 2. Leave Management
- **Leave Request System:** Allows employees to create, retrieve, and update their leave requests.
- **Approval Workflow:** Enables managers to review and approve/deny leave requests.
- **Email Notifications:** Sends automated notifications for leave approvals, system updates, and other relevant communications.

### 3. Payroll Management
- **Payment Scheduling:** Schedules payments for eligible employees and tracks the status.
- **Email Notifications:** Sends scheduled mails to employees regarding released payroll.

## Project Structure

- **/user_management:** Contains code related to user registration, sign-in, and role-based access control.
- **/employee_management:** Contains code for managing employee data and statuses.
- **/leave_management:** Contains code for handling leave requests and approval workflows.
- **/payroll_management:** Contains code for scheduling and tracking payroll payments.
- **/review_bug_fixes:** Contains code and documentation for system review, bug fixes, and final documentation.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript, jQuery
- **Backend:** Django, Python
- **Database:** PostgreSQL
- **Version Control:** Git
- **Deployment:** Heroku
- **Email Integration:** SMTP

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/payroll-service-development.git
   ```
2. Navigate to the project directory:
   ```sh
   cd payroll-service-development
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser for accessing the admin panel:
   ```sh
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

1. Access the application at `http://localhost:8000`.
2. Register and log in as a user.
3. Navigate through the various modules: User Management, Employee Management, Leave Management, Payroll Management.
4. Admin users can manage employee data and leave requests.
5. Employees can submit leave requests and view payroll details.

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```sh
   git push origin feature-name
   ```
6. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Thanks to all contributors and collaborators.
- Special thanks to Infosys Springboard for the internship opportunity and project guidance.
