# Xen Finance

Xen Finance is a comprehensive financial management application designed to help users manage their finances efficiently using modern web technologies. This is a personal project built using Django, a Python web development framework, and many other technologies like postgreSQL, celery, etc.

## Table of Contents
- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Admin Features](#admin-features)
- [Email Notifications](#email-notifications)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About

Xen Finance is a financial management application that provides users with tools to manage their finances, including account management, investments, withdrawals, and more. The application uses Celery for task scheduling and requires a message broker like RabbitMQ.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/buchii1/xen-finance.git
   ```
2. Navigate to the project directory:
   ```bash
   cd xen-finance
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up Celery and RabbitMQ (or another broker):
   - Install RabbitMQ: [RabbitMQ Installation Guide](https://www.rabbitmq.com/download.html)
   - Configure Celery in the project settings.

## Usage

To start the application, use the following commands:
```bash
python manage.py runserver
celery -A project_name worker --loglevel=info
celery -A project_name beat --loglevel=info
```

Open your browser and navigate to `http://localhost:8000` to access the application.

## Features

1. **Account Management**
   - Sign up and log in.
   - Activate Two-Factor Authentication (2FA).
   
2. **Dashboard**
   - Deposit money using crypto gateways.
   - Subscribe to investment plans and earn daily ROI.
   - Withdraw earnings.
   - Transfer money to other users using their username.
   - Manage crypto wallet addresses for withdrawals.
   - Update profile and complete KYC.
   - Generate and track referral links and earnings.
   - View detailed transaction history.
   - Deactivate or delete account.

## Admin Features

- Create and manage investment plans.
- Set charges on deposits and withdrawals.
- Terminate active investment plans.
- Approve/reject user deposit, transfer, and withdrawal requests.
- Activate/deactivate transfer feature for users.
- Activate 2FA globally.
- Edit user details and mark users inactive.

## Email Notifications

- Notifications for deposits, withdrawals, transfers, and investment purchases.
- Admin notifications for pending tasks.
- Status change notifications for user accounts.

## Future Enhancements

- Support for support tickets.
- Integration with additional payment gateways like BinancePay.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact:
- **Name**: Buchii
- **Email**: [okonkwogodspower@yahoo.com](mailto:okonkwogodspower@yahoo.com)
