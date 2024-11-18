# Desk Booking Automation Script

### Author  
**Meysam Aghighi**  
Contact: [meysam.aghighi@gmail.com](mailto:meysam.aghighi@gmail.com) / [meysam.aghighi@ericsson.com](mailto:meysam.aghighi@ericsson.com)  

---

## Description  
This script automates desk booking in Flowscape. It searches for a desk, selects dates, and books it automatically, using saved credentials from your Chrome default profile.

---

## Usage  

### 1. Update Configuration  
Modify these variables in the script before running:  
- `desk`: Desk number to be booked.  
- `dates`: Days to book (ensure they match the month).

### 2. Prerequisites  
- Install Python 3.x.  
- Install dependencies:  
  ```bash
  pip install selenium pycryptodome pywin32
- Ensure Chrome is installed and the **default profile** has your saved credentials.

---

### 3. Run the Script  
1. Save Chrome tabs before running the script because the script closes Chrome.
2. Execute it in your Python environment.

---

### 4. Schedule Script Execution  
- Add the script to Windows Task Scheduler for automated daily runs.

---

### Assumptions  
- You are already logged into Flowscape using Chrome's saved credentials.  

---

### To-Do (WIP)  
1. **Fix "Next Month" Navigation:** Currently fails when booking dates in the next month.  


---

### Contact  
For issues or suggestions, please contact via email.
