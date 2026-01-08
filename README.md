Building REST API in Python Using Flask

Assumptions : 

1. Logs are sorted according to date and time (stored in logs/sample.log directory)
2. Time stamp format is in "Year-Day-Month" time - "Hr-Min-Sec"
3. Format - Timestamp\tLevel\tComponent\tMessage
4. Log format is consistent


Technologies : Python, Flask

API Endpoints : 

- GET /logs
- GET /logs/stats
- GET /logs/{log_id}

