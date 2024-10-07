# Food Traceability System

A comprehensive food traceability system leveraging blockchain, IoT, and modern web technologies to ensure food safety and transparency.

## System Architecture

### Frontend (React + TypeScript)
- **Framework**: React 18
- **State Management**: Redux Toolkit
- **UI Library**: Ant Design
- **HTTP Client**: Axios
- **Router**: React Router v6
- **Styling**: CSS Modules + SCSS

### Backend (FastAPI)
- **Framework**: FastAPI (Python)
- **Database**: SQLite + Redis
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **File Storage**: Local filesystem
- **API Documentation**: Swagger/OpenAPI

### Blockchain Network
- **Platform**: Hyperledger Fabric
- **Network Type**: Solo (Single Orderer)
- **Smart Contract**: Go (Chaincode)
- **Consensus**: Solo ordering service

### IoT System
- **Hardware**: Raspberry Pi
- **Communication**: MQTT Protocol
- **Sensors**: Temperature, Humidity, GPS
- **Data Collection**: Real-time environmental monitoring

## Project Structure


1️⃣
front-end
├── public/                     # Static resources directory
│   └── index.html             # Main HTML file
├── src/                       # Source code directory
│   ├── api/                   # API request related
│   │   ├── admin.ts          # Admin API endpoints
│   │   ├── auth.ts           # Authentication API endpoints
│   │   ├── axios.ts          # Axios configuration
│   │   └── products.ts       # Products API endpoints
│   ├── components/           # Common components
│   │   ├── common/           # Base components
│   │   │   ├── ErrorBoundary.tsx  # Error handling component
│   │   │   └── Loading.tsx   # Loading component
│   │   ├── Layout/           # Layout components
│   │   └── ProtectedRoute.tsx # Route protection component
│   ├── pages/                # Page components
│   │   ├── admin/           # Admin pages
│   │   ├── auth/            # Authentication pages
│   │   ├── consumer/        # Consumer pages
│   │   ├── distributor/     # Distributor pages
│   │   ├── producer/        # Producer pages
│   │   ├── retailer/        # Retailer pages
│   │   └── trace/           # Tracing pages
│   ├── routes/              # Route configuration
│   ├── services/            # Service layer
│   ├── store/               # Redux store
│   ├── styles/              # Style files
│   ├── types/               # TypeScript type definitions
│   └── utils/               # Utility functions




2️⃣
iot_tracking/
│
├── app.py                     # Main Flask application entry point
├── requirements.txt           # Project dependencies
│
├── hardware/                  # Hardware interface modules
│   ├── __init__.py
│   ├── sht35_sensor.py       # Temperature/humidity sensor interface
│   ├── gps_module.py         # GPS module interface
│   └── nfc_controller.py     # NFC shield controller
│
└── config/                   # Configuration files
    └── config.py            # Application configuration settings





3️⃣
blockchain/                             # Blockchain integration
│   │   ├── __init__.py    # Blockchain package initialization
│   │   ├── client.py      # Blockchain client implementation
│   │   ├── models.py      # Blockchain data models
│   │   ├── chaincode/     # Smart contract code
│   │   │   ├── Dockerfile # Smart contract container config
│   │   │   ├── foodtrace.go # Main smart contract code
│   │   │   ├── go.mod     # Go module dependencies
│   │   │   └── go.sum     # Go dependency version lock
│   │   └── network/       # Blockchain network configuration



4️⃣
backend/
├── app/
│   ├── api/                 # API routing layer
│   │   ├── __init__.py     # API package initialization
│   │   ├── admin.py        # Admin-related API endpoints
│   │   ├── auth.py         # Authentication endpoints (login, register)
│   │   ├── consumer.py     # Consumer-related endpoints
│   │   ├── product.py      # Product management endpoints (CRUD)
│   │   ├── iot.py         # IoT device data endpoints
│   │   ├── order.py       # Order management endpoints
│   │   ├── rfid.py        # RFID tag management endpoints
│   │   ├── sale.py        # Sales management endpoints
│   │   ├── shipment.py    # Logistics and delivery endpoints
│   │   ├── user.py        # User management endpoints
│   │   ├── warehouse.py   # Warehouse management endpoints
│   │   └── endpoints/
│   │       └── blockchain.py # Blockchain-related endpoints
│   │
│   ├── blockchain/         # Blockchain integration
│   │   ├── __init__.py    # Blockchain package initialization
│   │   ├── client.py      # Blockchain client implementation
│   │   ├── models.py      # Blockchain data models
│   │   ├── chaincode/     # Smart contract code
│   │   │   ├── Dockerfile # Smart contract container config
│   │   │   ├── foodtrace.go # Main smart contract code
│   │   │   ├── go.mod     # Go module dependencies
│   │   │   └── go.sum     # Go dependency version lock
│   │   └── network/       # Blockchain network configuration
│   │
│   ├── core/              # Core functionality
│   │   ├── __init__.py    # Core package initialization
│   │   ├── auth.py        # Authentication core functionality
│   │   ├── blockchain.py  # Blockchain core functionality
│   │   ├── config.py      # System configuration
│   │   ├── email.py       # Email functionality
│   │   ├── mqtt_handler.py # MQTT message handling
│   │   ├── mqtt.py        # MQTT client
│   │   └── security.py    # Security-related functionality
│   │
│   ├── db/                # Database related
│   │   ├── __init__.py    # Database package initialization
│   │   ├── base_class.py  # Base model class
│   │   ├── base.py        # Database base configuration
│   │   ├── init_db.py     # Database initialization script
│   │   ├── model_registry.py # Model registry
│   │   ├── redis.py       # Redis client configuration
│   │   ├── session.py     # Database session management
│   │   └── data/          # Database file storage
│   │
│   ├── middleware/        # Middleware
│   │   ├── __init__.py    # Middleware package initialization
│   │   └── auth.py        # Authentication middleware
│   │
│   ├── models/            # Data models
│   │   ├── __init__.py    # Models package initialization
│   │   ├── user.py        # User model
│   │   ├── product.py     # Product model
│   │   ├── order.py       # Order model
│   │   ├── sale.py        # Sales model
│   │   ├── shipment.py    # Logistics model
│   │   └── iot.py         # IoT device model
│   │
│   ├── schemas/           # Data validation schemas
│   │   ├── __init__.py    # Schema package initialization
│   │   ├── base.py        # Base schema
│   │   ├── auth.py        # Authentication schemas
│   │   ├── user.py        # User-related schemas
│   │   ├── product.py     # Product-related schemas
│   │   ├── order.py       # Order-related schemas
│   │   ├── sale.py        # Sales-related schemas
│   │   ├── shipment.py    # Logistics-related schemas
│   │   ├── iot.py         # IoT data schemas
│   │   └── blockchain.py  # Blockchain data schemas
│   │
│   ├── services/          # Business logic layer
│   │   ├── __init__.py    # Services package initialization
│   │   ├── admin.py       # Admin business logic
│   │   ├── auth.py        # Authentication business logic
│   │   ├── blockchain.py  # Blockchain business logic
│   │   ├── email.py       # Email service
│   │   ├── iot.py         # IoT device business logic
│   │   ├── product.py     # Product business logic
│   │   ├── sale.py        # Sales business logic
│   │   ├── shipment.py    # Logistics business logic
│   │   ├── trace.py       # Traceability business logic
│   │   └── user.py        # User business logic
│   │
│   ├── static/            # Static files
│   │   └── uploads/       # Uploaded file storage
│   │
│   ├── templates/         # Template files
│   │   └── email/         # Email templates
│   │       ├── alert.html # Alert email template
│   │       └── verify.html # Verification email template
│   │
│   ├── tests/             # Test files
│   │   ├── __init__.py    # Test package initialization
│   │   └── postman/       # Postman test collections
│   │
│   ├── utils/             # Utility functions
│   │   ├── __init__.py    # Utils package initialization
│   │   └── token.py       # Token handling utilities
│   │
│   ├── mock/              # Mock data
│   │   └── mqtt_simulator.py # MQTT simulator
│   │
│   ├── .env              # Environment variables
│   └── main.py           # Application entry point
│
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation



## Features

- **User Management**
  - Role-based access control
  - JWT authentication
  - Email verification

- **Product Management**
  - Product registration
  - Batch management
  - Price management
  - Inventory tracking

- **Supply Chain Tracking**
  - Real-time location tracking
  - Environmental monitoring
  - RFID/NFC integration
  - Blockchain verification

- **IoT Integration**
  - Temperature monitoring
  - Humidity monitoring
  - GPS tracking
  - Real-time alerts

## Getting Started

### Prerequisites
- Node.js >= 16
- Python >= 3.9
- Go >= 1.16
- Docker & Docker Compose
- Hyperledger Fabric 2.x
- Raspberry Pi (for IoT)

### Installation

1. **Frontend Setup**
bash
cd frontend
npm install
npm start

2. **Backend Setup**

bash
cd backend
source food/bin/activate # Windows: food\Scripts\activate
uvicorn app.main:app --reload --port 8002

3. **Blockchain Network**
cd blockchain
./network.sh up

4. **IoT System**
bash
cd iot_tracking
pip install -r requirements.txt
python app.py


## License
1. **MIT**
Copyright <2025>  <Oxford Brookes University><Theo shu>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


1. **Apache**
Copyright [2025] [Oxford Brookes University][Theo shu]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

