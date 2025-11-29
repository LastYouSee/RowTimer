# Rowing Event Timer

A Python GUI application for timing rowing events where participants complete two runs and are ranked by their consistency (smallest time difference between runs wins).

## Features

- **Participant Registration**: Register boats with participant names
- **Individual Boat Controls**: Each boat has dedicated START/STOP/RESET buttons for fast timing
- **Dual Run Timing**: Time two runs per participant with intuitive interface
- **Multiple Simultaneous Timers**: Time multiple boats at once without conflicts
- **Live Timer Display**: Real-time display of all active timers
- **Streamlined Operation**: No popup dialogs during timing - instant visual feedback
- **Reliable Button Styling**: tk.Button controls with guaranteed high-contrast colors for race day visibility
- **Anti-Blinking Interface**: Smooth, targeted updates eliminate distracting screen flashing during timing
- **Results Calculation**: Automatic ranking based on consistency (time difference)
- **Data Persistence**: Saves participant data between sessions
- **Results Export**: Export results to CSV format

## Requirements

- Python 3.6 or higher
- No additional dependencies required (uses Python standard library only)

## Installation

1. Clone or download this repository
2. No additional installation required - the application uses only Python standard library modules

## Usage

### Starting the Application

Run the application using either method:

```bash
python rowing_timer.py
```

or

```bash
python run_timer.py
```

### Application Tabs

#### 1. Registration Tab
- **Register participants**: Enter boat number and participant name
- **View registered boats**: See all participants and their current status
- **Manage participants**: Remove individual participants or clear all

#### 2. Timing Tab
- **Run selection**: Choose which run to time at the top (Run 1 or Run 2)
- **Individual boat controls**: Each boat has its own START/STOP/RESET buttons
- **Active timers**: View all currently running timers with real-time updates
- **Status display**: See each boat's current state with color coding (🔵 Ready → 🔴 Running → 🟢 Complete)
- **Instant feedback**: Completed times show immediately with ✓ checkmark - no popups to dismiss
- **Multiple simultaneous timing**: Time multiple boats at once without interference
- **Smooth updates**: Targeted interface updates eliminate blinking/flashing during timer operations

#### 3. Results Tab
- **Calculate results**: Process all completed participants and rank by consistency
- **View rankings**: See participants ranked from most to least consistent
- **Export results**: Save results to CSV file with timestamp

## How It Works

1. **Registration**: Register each boat with a unique boat number and participant name
2. **Run Selection**: Choose which run to time (Run 1 or Run 2) at the top
3. **Individual Timing**: Each boat has dedicated START/STOP buttons - no dropdown needed
4. **Multiple Boats**: Time multiple boats simultaneously during mass or staggered starts
5. **Results**: Calculate rankings based on consistency (smallest time difference wins)

## Data Storage

- Participant data is automatically saved to `rowing_data.json`
- Data persists between application sessions
- Results can be exported to timestamped CSV files

## Example Workflow

1. Start the application
2. Go to **Registration** tab and add all participants
3. Switch to **Timing** tab
4. Select "Run 1" at the top
5. For each boat:
   - Click that boat's START button when it begins
   - Click that boat's STOP button when it finishes
6. Select "Run 2" at the top and repeat for all boats
7. Go to **Results** tab
8. Click "Calculate Results" to see rankings
9. Click "Export Results" to save to CSV

## File Structure

```
RowTimer/
├── rowing_timer.py      # Main application
├── run_timer.py         # Launcher script
├── requirements.txt     # Dependencies info
├── README.md           # This file
├── rowing_data.json    # Generated data file
└── rowing_results_*.csv # Generated result exports
```

## Features in Detail

### Individual Boat Controls
- Each boat has dedicated START/STOP/RESET buttons using tk.Button for reliable colors
- No dropdown selection needed - just click the boat's button
- Status indicators show Ready/Running/Complete with color coding
- **Perfect for fast timing during close starts**
- **No popup dialogs** - instant visual feedback when timers complete
- **Guaranteed readable text**: Green START, Red STOP, Gray RESET buttons
- **Smooth operation**: Anti-blinking targeted updates maintain visual focus

### Timer Display
- **Real-time timer updates** (10ms precision)
- **Format**: MM:SS.sss (minutes:seconds.milliseconds)
- **Color-coded active timers** with boat identification
- **Multiple simultaneous timers** supported
- **Non-disruptive updates**: Interface updates don't interrupt timing flow

### Results Calculation
- Consistency score based on absolute time difference
- Ranking from most consistent (smallest difference) to least consistent
- Only participants with both runs completed are included in results

### Data Management
- Automatic save/load of participant data
- Confirmation dialogs for destructive operations
- Error handling for invalid inputs

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Ensure Python 3.6+ is installed
   - Check that tkinter is available (included with most Python installations)

2. **Timer not starting**
   - Check that the boat is registered in the Registration tab
   - Verify the correct run is selected at the top (Run 1 or Run 2)
   - Ensure the boat's timer isn't already running

3. **No results showing**
   - Ensure participants have completed both runs
   - Click "Calculate Results" to process the data

### Error Messages

- **"No boat specified"**: Click the START button for a specific registered boat
- **"Boat X is already registered"**: Use a different boat number
- **"No active timer"**: The boat/run combination doesn't have a running timer

### Visual Indicators

- **Green buttons (#4CAF50) with white text**: START buttons for clear visibility
- **Red buttons (#f44336) with white text**: STOP buttons for immediate recognition  
- **Gray buttons (#e0e0e0) with black text**: RESET buttons for neutral actions
- **Disabled buttons**: Light gray (#cccccc) with darker gray text (#666666)
- **Color-coded status**: Blue (Ready) → Red (Running) → Green (Complete with ✓)
- **Reliable colors**: Uses tk.Button instead of ttk for consistent appearance across systems

## Contributing

Feel free to submit issues or pull requests to improve the application.

## License

This project is open source and available under the MIT License.