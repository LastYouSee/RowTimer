# Rowing Timer - User Guide

## Quick Start

1. **Windows Users**: Double-click `start_timer.bat`
2. **All Users**: Run `python rowing_timer.py` or `python start_with_sample.py`

## Step-by-Step Tutorial

### Getting Started

When you first run the application, you'll see three tabs:
- **Registration**: Manage participants
- **Timing**: Start/stop timers for runs
- **Results**: View rankings and export data

### 1. Registering Participants

**Go to the Registration tab:**

1. Enter a unique **Boat Number** (e.g., "B001", "Team1", "Alice")
2. Enter the **Participant Name** (e.g., "Alice Johnson")
3. Click **Register**
4. Repeat for all participants

**Example Registration:**
```
Boat Number: B001    Participant Name: Alice Johnson    [Register]
Boat Number: B002    Participant Name: Bob Smith        [Register]
Boat Number: B003    Participant Name: Carol Davis      [Register]
```

**Tips:**
- Use consistent boat numbering (B001, B002, etc.)
- Participant names help identify results later
- You can remove participants by selecting them and clicking "Remove Selected"

### 2. Timing Runs

**Go to the Timing tab:**

For each participant, you need to time TWO runs:

#### Run Selection:
1. At the top, select which run you're timing: **"Run 1"** or **"Run 2"**
2. All boats will be timed for the selected run

#### Individual Boat Controls:
Each registered boat has its own row with:
- **Boat number and name** for easy identification
- **Status** showing current state (Ready/Running/Complete)
- **Current Time** displaying the recorded time or "-" if not timed
- **Three buttons**: START, STOP, RESET

#### Timing Process:
1. Select **"Run 1"** at the top
2. For each boat (e.g., B001):
   - When the boat starts rowing, click **B001's START button**
   - When the boat finishes, click **B001's STOP button**
   - Time is automatically saved
3. Repeat for all boats in Run 1
4. Switch to **"Run 2"** at the top
5. Repeat the timing process for all boats

#### Multiple Simultaneous Timing:
- You can time multiple boats at once
- Each boat has independent START/STOP buttons  
- Perfect for staggered starts or mass starts
- Active timers show at the top with live updates: **"Boat B001 Run 1: 01:23.456"**
- Completed times appear instantly with ✓ checkmark - no popup to dismiss
- Status colors: 🔵 Ready → 🔴 Running → 🟢 Complete

### 3. Viewing Results

**Go to the Results tab:**

1. Click **"Calculate Results"** to process all completed participants
2. Results are ranked by **consistency** (smallest time difference wins)
3. Only participants with BOTH runs completed appear in results

**Example Results Table:**
```
Rank | Boat | Name        | Run 1    | Run 2    | Difference | Consistency Score
1    | B003 | Carol Davis | 01:08.567| 01:08.234| 00:00.333  | 0.333s
2    | B001 | Alice J.    | 01:05.234| 01:05.890| 00:00.656  | 0.656s  
3    | B002 | Bob Smith   | 01:02.123| 01:03.456| 00:01.333  | 1.333s
```

**Winner**: Carol Davis (B003) - most consistent with only 0.333 seconds difference!

### 4. Exporting Results

1. After calculating results, click **"Export Results"**
2. Creates a CSV file: `rowing_results_20231201_143022.csv`
3. Open in Excel, Google Sheets, or any spreadsheet program

## Common Scenarios

### Scenario 1: Regular Race Day
1. Register all boats before the race starts
2. Time Run 1 for all boats
3. Take a break between runs
4. Time Run 2 for all boats
5. Calculate and announce results

### Scenario 2: Multiple Heats
1. Register boats for Heat 1
2. Complete both runs for Heat 1 boats
3. Calculate results for Heat 1
4. Register new boats for Heat 2
5. Repeat timing process

### Scenario 3: Mistakes and Corrections
- **Wrong button clicked**: Use RESET to clear timer
- **Timer started too early**: Click STOP, then RESET, then restart
- **Participant info wrong**: Remove and re-register
- **Want to re-time a run**: Select boat/run, click RESET, then re-time

## Understanding the Timing

### Time Format
- Display: **MM:SS.sss** (Minutes:Seconds.milliseconds)
- Example: **01:23.456** = 1 minute, 23.456 seconds

### Consistency Scoring
- **Lower difference = better ranking**
- **Example**: 
  - Boat A: Run1=60.0s, Run2=60.5s → Difference=0.5s
  - Boat B: Run1=58.0s, Run2=62.0s → Difference=4.0s
  - **Boat A wins** (more consistent despite slower times)

## Troubleshooting

### Problem: "No boats in dropdown"
**Solution**: Register participants in the Registration tab first

### Problem: "Can't start timer"
**Causes & Solutions**:
- Boat not registered → Go to Registration tab and register the boat first
- Timer already running for that boat/run → Look for "RUNNING" status, stop existing timer first
- Wrong run selected → Check the run selection at the top of the timing tab
- Button appears disabled → Check if boat already has a timer running for that run

### Problem: "No results showing"
**Causes & Solutions**:
- Haven't clicked "Calculate Results" → Click the button
- No boats have both runs complete → Complete timing for both runs
- All participants are incomplete → Check Registration tab for status

### Problem: Timer shows wrong time
**Solution**: 
1. Ensure correct run is selected at the top (Run 1 or Run 2)
2. Click the RESET button for that specific boat
3. Re-time the run using that boat's START/STOP buttons

## Tips for Race Day

### Before the Event
- [ ] Test the application with sample data
- [ ] Prepare a list of boat numbers and participant names
- [ ] Ensure laptop is charged and has backup power
- [ ] Have a backup timing method ready

### During the Event
- [ ] Register all participants before starting
- [ ] Announce which run is being timed and select it at the top
- [ ] Use clear boat identification (numbers, colors, etc.)
- [ ] Keep spectators informed of current timings
- [ ] Watch for boats with "RUNNING" status to avoid timing errors
- [ ] Save/export results immediately after calculation

### Best Practices
- **Consistent Boat Numbers**: Use B001, B002, B003... format
- **Clear Communication**: Announce "Boat B001 starting Run 1" before clicking that boat's START button
- **Visual Confirmation**: Check the boat name and status before clicking START
- **Watch Status Changes**: Completed timers show ✓ and time automatically - no popup to dismiss
- **Run Selection**: Always verify the correct run is selected at the top before timing
- **Monitor Colors**: Green status = complete, Red = running, Blue = ready
- **Regular Saves**: Application auto-saves, but you can restart if needed
- **Backup Results**: Export results to CSV as soon as calculated

## Advanced Features

### Multiple Simultaneous Timers
- You can time multiple boats at once - each has independent START/STOP buttons
- Each active timer shows separately in the Active Timers display
- Perfect for staggered starts or when boats finish at different times
- No limit on how many boats can be timed simultaneously

### Data Persistence
- All data automatically saves to `rowing_data.json`
- Restarting the application preserves all participant data and times
- Safe to close and reopen the application during an event

### Partial Results
- Participants with only one run completed show as "Partial" status
- They won't appear in final rankings until both runs are complete
- You can see their individual times in the Registration tab

## File Management

The application creates these files:
- `rowing_data.json` - Participant data (auto-created)
- `rowing_results_YYYYMMDD_HHMMSS.csv` - Exported results

Keep these files safe for record-keeping and potential disputes!