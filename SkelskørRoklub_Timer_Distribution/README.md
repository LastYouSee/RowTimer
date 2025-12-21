# Skelskør Roklub - Ro Konkurrence Timer

En Python GUI applikation til tidtagning af rokonkurrencer hvor deltagere gennemfører to ture og rangeres efter deres konsistens (mindste tidsforskel mellem ture vinder).

*A Python GUI application for timing rowing events for Skelskør Roklub where participants complete two runs and are ranked by their consistency.*

## Funktioner / Features

- **🚣 Skelskør Roklub Branding**: Tilpasset til klubbens identitet og website
- **📝 Deltager Tilmelding**: Tilmeld både med deltager navne
- **⏱️ Individuelle Båd Kontroller**: Hver båd har dedikerede START/STOP/RESET knapper til hurtig tidtagning
- **🏁 Dobbelt Tur Tidtagning**: Tag tid på to ture per deltager med intuitivt interface
- **🚣‍♀️ Flere Samtidige Timere**: Tag tid på flere både samtidig uden konflikter
- **📊 Live Timer Display**: Real-time visning af alle aktive timere
- **🎯 Strømlinet Betjening**: Ingen popup dialoger under tidtagning - øjeblikkelig visuel feedback
- **🎨 Pålidelige Knap Farver**: tk.Button kontroller med garanteret høj kontrast til konkurrence dagen
- **✨ Anti-Blink Interface**: Glatte, målrettede opdateringer eliminerer distraherende skærm blinkning
- **🏆 Resultat Beregning**: Automatisk rangering baseret på konsistens (tidsforskel)
- **💾 Data Persistens**: Gemmer deltager data mellem sessioner
- **📄 Resultat Eksport**: Eksporter resultater til både CSV og PDF formater med professionel formatering

*Custom-branded for Skelskør Roklub with Danish interface and club information integrated throughout.*

## Krav / Requirements

### For Executable Version (Recommended)
- **Ingen krav** - Klar til brug direkte
- Windows 10 eller nyere
- Ca. 50 MB ledig plads

### For Python Source Version
- Python 3.6 eller højere / Python 3.6 or higher
- **ReportLab** (til PDF eksport): `pip install reportlab`
- Anden funktionalitet bruger kun Python standard bibliotek

## Installation / Download

### 📦 Executable Version (Lettest for Klubmedlemmer)
1. Download `SkelskørRoklub_Timer_Installer_YYYYMMDD.zip`
2. Udpak ZIP filen til en mappe
3. Dobbeltklik på `SkelskørRoklub_Timer.exe`
4. **FÆRDIG!** - Ingen yderligere installation påkrævet

### 👨‍💻 Developer Version (Python Source)
1. Klon eller download dette repository
2. Installer afhængigheder for fuld funktionalitet:
   ```bash
   python install_dependencies.py
   ```
   Eller installer manuelt: `pip install reportlab`
3. Grundlæggende funktionalitet virker uden yderligere afhængigheder

*The executable version is ready-to-use without Python installation. For developers, clone the repository as shown above.*

## Brug / Usage

### Start af Applikationen / Starting the Application

#### Executable Version (Anbefalet)
```
Dobbeltklik på: SkelskørRoklub_Timer.exe
```

#### Python Source Version
Kør applikationen med en af disse metoder:

```bash
python rowing_timer.py
```

eller / or

```bash
python start_with_sample.py  # Med eksempel data / With sample data
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
- **Export CSV**: Save results to comma-separated values file for spreadsheets
- **Export PDF**: Generate professional formatted report with tables and styling

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

1. Start applikationen / Start the application
2. Gå til **Tilmeldinger** fanen og tilføj alle deltagere / Go to **Registration** tab and add all participants
3. Skift til **Tidtagning** fanen / Switch to **Timing** tab
4. Vælg "Tur 1" i toppen / Select "Run 1" at the top
5. For hver båd / For each boat:
   - Klik på bådens START knap når den begynder
   - Klik på bådens STOP knap når den slutter
6. Vælg "Tur 2" i toppen og gentag for alle både / Select "Run 2" at the top and repeat for all boats
7. Gå til **Resultater** fanen / Go to **Results** tab
8. Klik "Beregn Resultater" for at se placeringer / Click "Calculate Results" to see rankings
9. Klik "Eksporter CSV" eller "Eksporter PDF" / Click "Export CSV" or "Export PDF" for reports

## File Structure

### Executable Distribution
```
SkelskørRoklub_Timer_Installer/
├── SkelskørRoklub_Timer.exe    # 🚀 Main application (ready to run)
├── INSTALLATION_GUIDE.txt      # Danish installation guide
├── LÆSMIG_FØRST.txt            # Quick start guide
├── README.md                   # This documentation
├── USER_GUIDE.md               # Detailed user guide
├── create_shortcut.bat         # Create desktop shortcut
└── uninstall.bat               # Uninstaller script
```

### Source Code Structure
```
RowTimer/
├── rowing_timer.py             # Main application
├── build_executable.py         # Build standalone executable
├── create_installer.py         # Create distribution package
├── BUILD_INSTRUCTIONS.md       # How to build executable
├── requirements.txt            # Dependencies info
├── install_dependencies.py     # Dependency installer
├── README.md                   # This file
├── rowing_data.json            # Generated data file
├── rowing_results_*.csv        # Generated CSV exports
└── rowing_results_*.pdf        # Generated PDF exports
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

### Results Calculation and Export
- **Consistency scoring**: Based on absolute time difference between runs
- **Ranking system**: Most consistent (smallest difference) to least consistent
- **CSV Export**: Comma-separated format for Excel, Google Sheets, etc.
- **PDF Export**: Professional formatted reports with tables and styling
- **File selection**: User-friendly save dialogs for choosing export location
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

### Export Formats

- **CSV Export**: Standard comma-separated values format
  - Compatible with Excel, Google Sheets, LibreOffice Calc
  - Includes rank, boat, name, times, and consistency scores
- **PDF Export**: Professional formatted reports (requires ReportLab)
  - Styled tables with headers and alternating row colors
  - Event information and summary statistics
  - Winner highlighting and consistency scoring explanation

## Om Skelskør Roklub / About Skelskør Roklub

**Skelskør Roklub** er en dansk roklub beliggende i Skælskør med fokus på motionsroning, coastal, kajak og inrigger. Klubben tilbyder træning i smukke omgivelser med et stærkt socialt fællesskab.

**Kontakt Information:**
- 📍 Gammelgade 25, 4230 Skælskør
- 📞 +45 40 73 16 60
- 📧 skelskoerroklub@gmail.com
- 🌐 www.skelskoerroklub.dk

*Skelskør Roklub is a Danish rowing club located in Skælskør focusing on fitness rowing, coastal, kayak, and sculling with training in beautiful surroundings.*

## 💻 Building Executable

For udviklere der vil bygge deres egen executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_executable.py

# Create installer package
python create_installer.py
```

Se `BUILD_INSTRUCTIONS.md` for detaljerede instruktioner.

*For developers wanting to build their own executable, see BUILD_INSTRUCTIONS.md for detailed instructions.*

## Bidrag / Contributing

Du er velkommen til at indsende issues eller pull requests for at forbedre applikationen.
Feel free to submit issues or pull requests to improve the application.

## Licens / License

Dette projekt er open source og tilgængeligt under MIT Licensen.
This project is open source and available under the MIT License.