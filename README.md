# NBA League Dashboard

An interactive dashboard for visualizing NBA league statistics throughout history, built with Streamlit and Python. This dashboard allows users to explore NBA league averages per game from 1946-47 to present day, with features for analyzing trends, comparing eras, and viewing player career spans.

## Data Source

All statistics are sourced from [Basketball-Reference.com](https://www.basketball-reference.com/leagues/NBA_stats_per_game.html), specifically the NBA League Averages - Per Game section. The data includes both basic and advanced statistics from the 1946-47 season to the present.

## Features

### Statistical Analysis
- View league averages for various statistics per game
- Compare multiple statistics simultaneously
- Calculate custom ratios between different statistics
- Toggle between linear and logarithmic scales
- Apply moving average smoothing to identify trends

### Historical Context
- Filter data by different NBA eras:
  - Russell/Wilt Era (1957-1969)
  - Magic-Bird Era (1979-1989)
  - Jordan Era (1989-1998)
  - Post-Jordan / Iso-Heavy Era (1999-2004)
  - Analytics Era (2014-2019)
- View significant policy changes:
  - Hand-checking banned (2004)
  - 3-point line introduced (1979)
  - Shot clock introduced (1954)

### Player Career Spans
- Visualize player career spans on the graph
- Compare multiple players' careers simultaneously
- Color-coded career spans for easy identification

### Interactive Controls
- Customizable year range selection
- Option to focus on modern era (since 1970)
- Toggle visibility of policy changes and era backgrounds
- Adjustable smoothing window for trend analysis

## Statistics Available

### Basic Statistics
- Points
- Field Goal Attempts/Made/Percentage
- Three-Point Attempts/Made/Percentage
- Free Throw Attempts/Made/Percentage
- Rebounds (Offensive/Defensive/Total)
- Assists
- Steals
- Blocks
- Turnovers
- Personal Fouls
- Games Played
- Minutes Played

### Advanced Statistics
- Pace Factor (possessions per 48 minutes)
- Effective Field Goal Percentage
- Turnover Percentage
- Offensive Rebound Percentage
- Free Throws Per Field Goal Attempt
- Offensive Rating
- True Shooting Percentage

## Requirements

- Python 3.x
- Streamlit
- Pandas
- Matplotlib
- NumPy

## Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install streamlit pandas matplotlib numpy
```

## Usage

1. Run the dashboard:
```bash
streamlit run dashboard.py
```

2. Use the sidebar controls to:
   - Select statistics to display
   - Choose analysis type (single statistics or ratio calculation)
   - Filter by era or time range
   - Toggle various visualization options

## Data Files Required

- `Avg league stats per game.csv`: Contains NBA league averages per game statistics
- `NBA_Players_Career_Spans.csv`: Contains player career span information (optional)

## Acknowledgments

- Data provided by [Basketball-Reference.com](https://www.basketball-reference.com)
- Built with [Streamlit](https://streamlit.io) 