# Military Database API Development Plan
## FastAPI + SQLModel + PostgreSQL

### Overview
This document outlines the development plan for creating an async REST API for a military database management system. The API will manage orders, assignments, transfers, divisions, and related military organizational data.

### Database Analysis
Based on the PostgreSQL schema, the system manages:

#### Core Entities
- **Users**: System users with credentials and roles
- **Divisions**: Military organizational units (hierarchical structure)
- **Orders**: Military orders/commands with types and statuses
- **Assignments**: Tasks assigned to users based on orders
- **Transfers**: Movement/transfer of items between divisions
- **Audit Log**: Complete audit trail of all operations

#### Lookup Tables
- Order Types, Order Statuses, Priority Types, Target Types
- Assignment Types, Assignment Statuses
- Transfer Types, Transfer Statuses, Transfer Categories
- Item Types, Term Types

#### Key Features
- Hierarchical division structure with cycle detection
- Comprehensive audit logging for all operations
- Transfer tracking with active status management
- Order terms with completion tracking
- User authentication and authorization

### Technology Stack
- **Backend**: FastAPI (Python 3.11+)
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: PostgreSQL 16+
- **Authentication**: JWT tokens
- **Documentation**: Auto-generated OpenAPI/Swagger
- **Testing**: pytest + pytest-asyncio
- **Migration**: Alembic

### Project Structure
```
axiom_next/api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Settings and configuration
│   │   ├── database.py         # Database connection and session
│   │   ├── security.py         # Authentication and authorization
│   │   └── dependencies.py     # Common dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Base model classes
│   │   ├── user.py             # User models
│   │   ├── division.py         # Division models
│   │   ├── order.py            # Order models
│   │   ├── assignment.py       # Assignment models
│   │   ├── transfer.py         # Transfer models
│   │   ├── lookup.py           # Lookup table models
│   │   └── audit.py            # Audit log models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   ├── division.py         # Division schemas
│   │   ├── order.py            # Order schemas
│   │   ├── assignment.py       # Assignment schemas
│   │   ├── transfer.py         # Transfer schemas
│   │   ├── lookup.py           # Lookup schemas
│   │   └── common.py           # Common schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # API dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── users.py        # User CRUD endpoints
│   │       ├── divisions.py    # Division CRUD endpoints
│   │       ├── orders.py       # Order CRUD endpoints
│   │       ├── assignments.py  # Assignment CRUD endpoints
│   │       ├── transfers.py    # Transfer CRUD endpoints
│   │       ├── lookup.py       # Lookup table endpoints
│   │       └── audit.py        # Audit log endpoints
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py             # Base CRUD operations
│   │   ├── user.py             # User CRUD operations
│   │   ├── division.py         # Division CRUD operations
│   │   ├── order.py            # Order CRUD operations
│   │   ├── assignment.py       # Assignment CRUD operations
│   │   ├── transfer.py         # Transfer CRUD operations
│   │   └── lookup.py           # Lookup CRUD operations
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication service
│   │   ├── audit.py            # Audit logging service
│   │   ├── division.py         # Division business logic
│   │   ├── transfer.py         # Transfer business logic
│   │   └── notification.py     # Notification service
│   └── utils/
│       ├── __init__.py
│       ├── security.py         # Security utilities
│       ├── validators.py       # Custom validators
│       └── exceptions.py       # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Test configuration
│   ├── test_auth.py            # Authentication tests
│   ├── test_users.py           # User tests
│   ├── test_divisions.py       # Division tests
│   ├── test_orders.py          # Order tests
│   ├── test_assignments.py     # Assignment tests
│   ├── test_transfers.py       # Transfer tests
│   └── test_audit.py           # Audit tests
├── alembic/                    # Database migrations
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

### Development Phases

#### Phase 1: Project Setup & Core Infrastructure (Week 1)
1. **Environment Setup**
   - Set up virtual environment
   - Install dependencies (FastAPI, SQLModel, asyncpg, etc.)
   - Configure development environment

2. **Database Configuration**
   - Configure SQLModel engine for async PostgreSQL
   - Set up connection pooling
   - Configure Alembic for migrations

3. **Core Framework**
   - Create FastAPI application with CORS and middleware
   - Set up configuration management using Pydantic Settings
   - Implement basic error handling and logging

#### Phase 2: Authentication & User Management (Week 2)
1. **Authentication System**
   - JWT token implementation
   - Password hashing with bcrypt
   - Login/logout endpoints
   - Token refresh mechanism

2. **User Models & CRUD**
   - User SQLModel with relationships
   - User credentials handling
   - User CRUD operations
   - Role-based access control

3. **Security Middleware**
   - JWT authentication dependency
   - Permission checking
   - Rate limiting

#### Phase 3: Core Domain Models (Week 3)
1. **Lookup Tables**
   - Order types, statuses, priorities
   - Assignment types, statuses
   - Transfer types, statuses, categories
   - Item types, term types, target types

2. **Division Management**
   - Hierarchical division structure
   - Parent-child relationships
   - Cycle detection validation
   - Division location tracking

3. **Base CRUD Operations**
   - Generic CRUD base class
   - Soft delete implementation
   - Audit logging integration

#### Phase 4: Orders & Assignments (Week 4)
1. **Order Management**
   - Order CRUD with relationships
   - Order recipients handling
   - Order terms tracking
   - Status workflow management

2. **Assignment System**
   - Assignment CRUD operations
   - Executor assignment
   - Priority and target type handling
   - Report content management

3. **Business Logic Services**
   - Order validation rules
   - Assignment workflow
   - Status transition logic

#### Phase 5: Transfer System (Week 5)
1. **Transfer Management**
   - Transfer CRUD operations
   - Item transfer tracking
   - Active transfer management
   - Due date monitoring

2. **Transfer Items**
   - Item quantity tracking
   - Unit of measure handling
   - Item identifier uniqueness
   - Active status management

3. **Transfer Business Logic**
   - Single active transfer enforcement
   - Division location updates
   - Completion tracking
   - Validation rules

#### Phase 6: Audit & Reporting (Week 6)
1. **Audit System**
   - Comprehensive audit logging
   - Automatic trigger handling
   - Audit trail queries
   - Performance optimization

2. **Reporting Endpoints**
   - Division hierarchy reports
   - Transfer history tracking
   - Current item status
   - Assignment details

3. **Advanced Features**
   - Search and filtering
   - Pagination
   - Export functionality
   - Dashboard data endpoints

#### Phase 7: Testing & Documentation (Week 7)
1. **Comprehensive Testing**
   - Unit tests for all CRUD operations
   - Integration tests for workflows
   - Authentication and authorization tests
   - Database constraint tests

2. **API Documentation**
   - OpenAPI/Swagger documentation
   - Endpoint descriptions
   - Request/response examples
   - Authentication documentation

3. **Performance Optimization**
   - Query optimization
   - Caching strategies
   - Connection pooling tuning
   - Monitoring setup

#### Phase 8: Deployment & Production Setup (Week 8)
1. **Production Configuration**
   - Environment-specific settings
   - Security hardening
   - Database connection optimization
   - Logging configuration

2. **Deployment Setup**
   - Docker containerization
   - Production database setup
   - SSL/TLS configuration
   - Monitoring and health checks

### Key Implementation Details

#### Database Considerations
- Use async SQLAlchemy with asyncpg driver
- Implement proper connection pooling
- Handle PostgreSQL-specific features (triggers, functions)
- Maintain existing database constraints and triggers

#### Security Features
- JWT-based authentication
- Role-based access control (admin, user roles)
- Input validation and sanitization
- SQL injection prevention
- Rate limiting and DDoS protection

#### Performance Optimization
- Implement query optimization with proper joins
- Use database indexes effectively
- Implement caching for lookup tables
- Optimize pagination for large datasets

#### API Design Principles
- RESTful endpoints with clear naming
- Consistent response formats
- Proper HTTP status codes
- Comprehensive error handling
- API versioning support

### Dependencies
```txt
fastapi>=0.104.0
sqlmodel>=0.0.14
asyncpg>=0.29.0
alembic>=1.13.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
uvicorn[standard]>=0.24.0
pydantic-settings>=2.1.0
pytest>=7.4.0
pytest-asyncio>=0.23.0
httpx>=0.25.0
```

### Environment Variables
The `.env` file is already configured with:
- Database connection parameters
- Application settings
- CORS configuration
- Logging levels

### Success Criteria
- All database tables accessible via API
- Complete CRUD operations for all entities
- Proper authentication and authorization
- Comprehensive audit logging
- Performance meets requirements (sub-second response times)
- 100% test coverage for critical paths
- Production-ready deployment configuration

### Risk Mitigation
- Regular database backups during development
- Comprehensive testing strategy
- Incremental deployment approach
- Performance monitoring from day one
- Security review at each phase
- Documentation maintained throughout development

This plan provides a structured approach to building a robust, secure, and scalable military database API system.
