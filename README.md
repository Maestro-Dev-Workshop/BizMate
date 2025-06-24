# BizMate - AI-Powered Business Management System

BizMate is a comprehensive business management system designed for Small to Medium Enterprises (SMEs) that leverages AI agents and Telegram bots to provide seamless business operations, customer service, and data analytics.

## 🚀 Features

### For Business Owners (BizMate Bot)
- **Business Registration & Management**: Register and manage business details
- **Inventory Management**: Track products, suppliers, and stock levels
- **Order Management**: View, fulfill, and track customer orders
- **Analytics & Reports**: Get insights on sales, profits, and business performance
- **Real-time Notifications**: Receive instant alerts for new orders
- **Personal Assistant Services**: AI-powered business assistance

### For Customers (Customer Service Bots)
- **Product Catalog**: Browse business products and services
- **Order Placement**: Place orders with negotiation capabilities
- **Order Tracking**: Track order status and history
- **Customer Support**: 24/7 AI-powered customer service
- **Purchase History**: View past orders and interactions

## 🏗️ Architecture

The system consists of several key components:

### Core Components
- **BotManager**: Orchestrates multiple Telegram bots
- **BizMate Agent**: AI agent for business owner interactions
- **Customer Service Agent**: AI agent for customer interactions
- **Database Manager**: Handles all database operations
- **Session Management**: Manages user sessions and state

### AI Agents
- **BizMate Agent**: Powered by Gemini 2.0 Flash model for business management
- **Customer Service Agent**: Handles customer inquiries and orders
- **Database Orchestrator**: Manages data operations
- **Analytics Agent**: Provides business insights and reports

## 📋 Prerequisites

- Python 3.8+
- MySQL Database
- Google AI SDK access (Gemini API)
- Telegram Bot API tokens
- Required Python packages (see requirements section)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bizmate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Telegram Bot Tokens
   BIZ_TOK=your_bizmate_bot_token
   
   # Database Configuration
   DB_HOST=localhost
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   
   # Google AI Configuration
   GOOGLE_API_KEY=your_google_ai_api_key
   
   # Other Settings
   RESET_QUOTA=24  # Session reset time in hours
   LOGS_FOLDER_PATH=./logs
   COMMS=your_communication_username
   ROUTER_SESSION=session_file for telegram
   ROUTER_ID=APP ID(You can get it from https://my.telegram.org/auth)
   ROUTER_HASH=APP_HASH

   ```

4. **Set up the database**
   - Create a MySQL database
   - Run the database schema setup (tables: business, customer, product, customer_order, visit, chat, log_history)

5. **Configure file paths**
   Update the log folder paths in `app.py`:
   ```python
   BZ_LOGS_FOLDER_PATH = Path("path/to/your/bizmate/logs")
   CS_LOGS_FOLDER_PATH = Path("path/to/your/customer_service/logs")
   ```

## 🚀 Usage

### Starting the System
```bash
python main/app.py
```

This will start:
- The main BizMate bot for business owners
- All registered customer service bots
- Automatic detection and addition of new customer service bots

### Bot Commands

#### BizMate Bot (Business Owners)
- `/start` or `/hello` - Initialize or restart the bot
- Natural language commands for:
  - "Show my inventory"
  - "Add new product"
  - "View pending orders"
  - "Generate sales report"
  - "Update supplier information"

#### Customer Service Bot (Customers)
- `/start` or `/hello` - Begin interaction
- Natural language commands for:
  - "Show me your products"
  - "I want to order [product]"
  - "Track my order"
  - "What's your business about?"

## 📊 Database Schema

### Key Tables
- **business**: Store business information and bot tokens
- **customer**: Customer details and contact information
- **product**: Product inventory and pricing
- **customer_order**: Order management and tracking  
- **visit**: Customer interaction logging
- **chat**: Chat session management
- **log_history**: Business owner login tracking

## 🔧 Configuration

### Adding New Customer Service Bots
1. Insert business record in database with Telegram bot token
2. The system automatically detects and starts new bots every 5 seconds

### Session Management
- Sessions reset after specified quota hours (default: 24 hours)
- Automatic welcome back messages with business updates
- State preservation across interactions

### Logging
- Conversation logs stored in specified directories
- Separate logs for each user and bot type
- Automatic log rotation and management

## 🛡️ Security Features

- Session-based user authentication
- Business owner verification through database
- Secure API key management through environment variables
- Input validation and sanitization
- Rate limiting through session quotas

## 🔄 System Flow

### Business Owner Interaction
1. User starts BizMate bot
2. System verifies business registration
3. If new user, delegates to database manager for registration
4. Provides business dashboard and management tools
5. Handles inventory, orders, and analytics requests

### Customer Interaction  
1. Customer starts business-specific customer service bot
2. System presents business information and product catalog
3. Handles product inquiries and order placement
4. Manages order tracking and customer support
5. Notifies business owner of new orders

### Order Management Flow
1. Customer places order through customer service bot
2. System validates inventory and customer details
3. Creates order record in database
4. Sends notification to business owner
5. Business owner can fulfill or decline order
6. Customer receives status updates

## 📈 Analytics & Reporting

The system provides comprehensive analytics including:
- Sales performance metrics
- Customer behavior analysis  
- Inventory turnover reports
- Profit and loss tracking
- Order fulfillment statistics

## 🧪 Testing

### Running Tests
```bash
# Test BizMate agent
python main/bizmate/agent.py

# Test individual components
python -m pytest tests/
```

### Manual Testing
- Use the conversation testing interface in agent files
- Monitor logs for debugging and performance analysis

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the logs in the designated log folders
- Review database records for data integrity
- Ensure all environment variables are properly set
- Verify Telegram bot tokens are active

## 🔮 Future Enhancements

- Mobile app integration
- Advanced analytics dashboard
- Multi-language support
- Payment gateway integration
- Inventory forecasting
- Supplier management automation

## 📞 Contact

For questions or support, please contact the development team or create an issue in the repository.

---

**Note**: Make sure to secure your API keys and database credentials. Never commit sensitive information to version control.
