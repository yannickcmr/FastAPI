""" File containing the FastAPI Description. """

DESCRIPTION = """ 
## FastAPI Example for Sales
A lightweight REST API for accessing and filtering business sales data, designed for easy integration and real-time analytics.

---
### 🚀 Quick Start
Access interactive API documentation at /docs after starting the server. All endpoints return consistent JSON responses with msg, code, and data fields.

---
### 🔍 Core Endpoints
| Endpoint | Method | Description | Parameters |
|:-------:|:-------:|:-------:|:-------:|
| / | GET | Welcome entry point | None |
| /ping |	GET |	Health check | log_lvl (optional) |
| /versions |	GET |	API version info |	log_lvl (optional) |
| /get_data |	GET |	Retrieve all sales data |	log_lvl (optional) |
| /filter_data |	POST |	Filter sales with custom queries |	JSON body with query |

---
### 📊 Data Operations
Dataset: Pre-loaded business_sales.csv with various business metrics

Filtering: Use /filter_data with MongoDB-style queries for precise data extraction

Response Format: All data endpoints return structured DataResponse with business records

---
### ⚙️ Features
CORS Enabled: Configured for cross-origin requests

Dynamic Logging: Adjust log level per request via log_lvl parameter

Async Support: Data-intensive endpoints use async processing

Thread Pooling: Optimized for concurrent requests
"""
