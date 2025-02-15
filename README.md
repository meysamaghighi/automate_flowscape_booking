# Desk Booking Automation Script

## Authors
- **Meysam Aghighi** ([meysam.aghighi@gmail.com](mailto:meysam.aghighi@gmail.com)/[meysam.aghighi@ericsson.com](mailto:meysam.aghighi@ericsson.com))
- **Wei Li I** ([wei.i.li@ericsson.com](mailto:wei.i.li@ericsson.com))

---

## Description  
This script automates desk booking in Flowscape. It will book the selected desk in [flowscape-desk.yaml](flowscape-desk.yaml) for the next two weeks. It also uses your saved credentials for Edge to login.

---

## Usage  
### 1. Prerequisites  
- Install Python 3.x.  
- Install dependencies: `pip install selenium pycryptodome pywin32`

### 2. Update Configuration  
Modify these in [flowscape-desk.yaml](flowscape-desk.yaml) before running:  
- `building`
- `floor`
- `desk`

### 3. Run the Script  
`python Edge_automate_flowscape_booking.py`

### 4. Full Automation  
- Add the script to Windows Task Scheduler for automated daily runs. The best scheduled time is 12:01 since new desks open at noon.

---

## Contact  
For issues or suggestions, please contact the authors via email.
