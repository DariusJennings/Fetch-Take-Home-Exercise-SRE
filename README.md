
# 🛠️ Endpoint Availability Checker
This is a lightweight Python script that monitors the availability of HTTP endpoints defined in a YAML file. It logs per-endpoint results every 15 seconds based on HTTP status and response time.

## ✅ Features
Supports GET and POST methods

Accepts custom headers and request bodies

Logs each endpoint’s availability every 15 seconds

Determines availability based on:

HTTP status code between 200–299

Response time ≤ 500ms

Graceful shutdown with Ctrl+C

---

## 📦 Requirements
Python 3.7+

requests

pyyaml

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DariusJennings/Fetch-Take-Home-Exercise-SRE.git
   cd Fetch-Take-Home-Exercise-SRE
   ```

2. Create and activate a virtual environment (this is optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

---

## Configuration

Create a YAML configuration file listing the endpoints you want to monitor. A sample configuration file (`endpoints.yaml`) is provided in the repository.

### Example `endpoints.yaml`:
```yaml
- body: '{"foo":"bar"}'
  headers:
    content-type: application/json
  method: POST
  name: sample body up    
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body  
  
- name: sample index up
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/

- body: "{}"
  headers:
    content-type: application/json
  method: POST
  name: sample body down    
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body

- name: sample error down
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/error 
```

---

## Usage

Run the program with the path to the YAML configuration file:

```bash
python3 availability-checker.py endpoints.yaml
```

### Example Output
   ```
2025-04-08 10:58:55,255 [sample body up] https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body - AVAILABLE | Status: 200 | Time: 89.97ms
2025-04-08 10:58:55,338 [sample index up] https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/ - AVAILABLE | Status: 200 | Time: 83.16ms
2025-04-08 10:58:55,429 [sample body down] https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body - UNAVAILABLE | Status: 422 | Time: 90.32ms
2025-04-08 10:58:55,993 [sample error down] https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/error - UNAVAILABLE | Error: HTTPSConnectionPool(host='dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com', port=443): Read timed out. (read timeout=0.5) | Time: 562.81ms
2025-04-08 10:58:55,993 [CUMULATIVE] dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com - Availability: 2/4 (50.00%)
   ```

---

## How It Works

1. The script reads a YAML file containing the list of HTTP endpoints.
2. Every 15 seconds, it:
   - Sends an HTTP request to each endpoint.
   - Evaluates the health of the endpoint based on:
     - HTTP status code (`200 - 299` is considered healthy).
     - Response latency (<500ms is considered healthy).
   - Tracks and logs cumulative availability percentages for each domain.
3. The script will run until manually stopped (e.g., via `CTRL+C`).

---

## Stopping the Program

To stop the monitoring, press `CTRL+C`. The script will exit gracefully.

---

## Identified Issues

| **Feature**                | **availability_checker.py**                                         | **main.py**                                                  |
| -------------------------- | ------------------------------------------------------------------  | ------------------------------------------------------------ |
| Logging Method             | Uses `logging` with timestamps                                        | Uses `print()` with basic output                               |
| Per-Endpoint Logging       | Logs individual endpoint results (status, latency, availability)    | Only logs cumulative domain availability                     |
| Cumulative Tracking        | Tracks per-domain stats (`available`, `total`)                          | Also tracks per-domain, but logs less detail                 |
| Latency Consideration      | Marks endpoint as unavailable if response > 500ms                   | Ignores latency; only status code determines availability    |  
| Response Time Logging      | Logs response time in ms                                            | No latency info logged                                       |
| Threading / Responsiveness | Uses background thread (`Thread`) to avoid blocking main thread       | Runs in a synchronous loop, blocks on sleep                  |
| YAML Config Validation     | Checks for proper list format before monitoring                     | Assumes YAML format is valid and structured correctly        |
| Error Details              | Logs error message and latency if request fails                     | Just marks as "DOWN" on exception, no details                |
| Body Handling in POST      | Uses `data=body` (more raw/flexible for generic formats)              | Uses `json=body` (more automatic for JSON)                     |

🧠 TL;DR
  * availability_checker.py is more detailed, and production-oriented compared to main.py:

    * Tracks availability more strictly (status and latency)

    * Gives full visibility into individual checks

    * Logs in a standardized, timestamped format

    * Resilient structure for future scaling or features
