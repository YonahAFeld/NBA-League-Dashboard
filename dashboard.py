import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define eras and policy changes
ERAS = {
    "Russell/Wilt Era": (1957, 1969),
    "Magic-Bird Era": (1979, 1989),
    "Jordan Era": (1989, 1998),
    "Post-Jordan / Iso-Heavy Era": (1999, 2004),
    "Analytics Era": (2014, 2019)
}

POLICY_CHANGES = {
    "Hand-checking banned": 2004,
    "3-point line introduced": 1979,
    "Shot clock introduced": 1954
}

# Define stat name mappings
STAT_NAMES = {
    # Basic Stats
    "PTS": "Points",
    "FGA": "Field Goal Attempts",
    "FGM": "Field Goals Made",
    "FG%": "Field Goal Percentage",
    "3PA": "Three-Point Attempts",
    "3PM": "Three-Pointers Made",
    "3P%": "Three-Point Percentage",
    "FTA": "Free Throw Attempts",
    "FTM": "Free Throws Made",
    "FT%": "Free Throw Percentage",
    "ORB": "Offensive Rebounds",
    "DRB": "Defensive Rebounds",
    "TRB": "Total Rebounds",
    "AST": "Assists",
    "STL": "Steals",
    "BLK": "Blocks",
    "TOV": "Turnovers",
    "PF": "Personal Fouls",
    "G": "Games Played",
    "MP": "Minutes Played",
    # Advanced Stats
    "Pace": "Pace Factor",
    "eFG%": "Effective Field Goal Percentage",
    "TOV%": "Turnover Percentage",
    "ORB%": "Offensive Rebound Percentage",
    "FT/FGA": "Free Throws Per Field Goal Attempt",
    "ORtg": "Offensive Rating",
    "TS%": "True Shooting Percentage"
}

# Define detailed stat explanations
STAT_EXPLANATIONS = {
    # Basic Stats
    "Points": "Average points scored per game",
    "Field Goal Attempts": "Average field goal attempts per game",
    "Field Goals Made": "Average field goals made per game",
    "Field Goal Percentage": "Percentage of field goals made",
    "Three-Point Attempts": "Average three-point attempts per game",
    "Three-Pointers Made": "Average three-pointers made per game",
    "Three-Point Percentage": "Percentage of three-pointers made",
    "Free Throw Attempts": "Average free throw attempts per game",
    "Free Throws Made": "Average free throws made per game",
    "Free Throw Percentage": "Percentage of free throws made",
    "Offensive Rebounds": "Average offensive rebounds per game",
    "Defensive Rebounds": "Average defensive rebounds per game",
    "Total Rebounds": "Average total rebounds per game",
    "Assists": "Average assists per game",
    "Steals": "Average steals per game",
    "Blocks": "Average blocks per game",
    "Turnovers": "Average turnovers per game",
    "Personal Fouls": "Average personal fouls per game",
    "Games Played": "Number of games played",
    "Minutes Played": "Average minutes played per game",
    # Advanced Stats
    "Pace Factor": "An estimate of possessions per 48 minutes",
    "Effective Field Goal Percentage": "Field goal percentage adjusted for the fact that 3-pointers are worth more than 2-pointers",
    "Turnover Percentage": "An estimate of turnovers committed per 100 plays",
    "Offensive Rebound Percentage": "An estimate of the percentage of available offensive rebounds a player grabbed while on the floor",
    "Free Throws Per Field Goal Attempt": "Ratio of free throw attempts to field goal attempts",
    "Offensive Rating": "An estimate of points produced per 100 possessions",
    "True Shooting Percentage": "A measure of shooting efficiency that accounts for 2-pointers, 3-pointers, and free throws"
}

# Helper function: convert season string (e.g., "2024-25") to an ending year integer
def season_to_year(season_str):
    season_str = season_str.strip()
    if '-' in season_str:
        first, second = season_str.split('-')
        return int(first[:2] + second)
    else:
        return int(season_str)

# Helper function to parse player years
def parse_player_years(years_str):
    try:
        # Remove quotes if present
        years_str = years_str.strip('"')
        
        # Handle special case for active players
        if 'Present' in years_str:
            start_year = int(years_str.split('–')[0])
            return start_year, 2024  # Use current year for active players
        
        # Handle multiple career spans (e.g., "1979–1991, 1996")
        spans = years_str.split(', ')
        all_years = []
        for span in spans:
            if '–' in span:
                # Handle year ranges with the specific dash character
                years = span.split('–')
                all_years.extend([int(years[0]), int(years[1])])
            else:
                # Handle single years
                all_years.append(int(span))
        return min(all_years), max(all_years)
    except Exception as e:
        st.sidebar.error(f"Error parsing year: {years_str}, Error: {str(e)}")
        return 0, 0

# Load and process the CSV data
@st.cache_data
def load_data():
    # Load main stats data
    stats_file = "/Users/yonahfeld/NBA League Dashboard/Avg league stats per game.csv"
    df_stats = pd.read_csv(stats_file, header=1)
    df_stats['SortYear'] = df_stats['Season'].apply(season_to_year)
    df_stats.sort_values('SortYear', inplace=True)
    
    # Rename columns to be more user-friendly
    df_stats = df_stats.rename(columns=STAT_NAMES)
    
    # Load player career data
    try:
        players_file = "/Users/yonahfeld/NBA League Dashboard/NBA_Players_Career_Spans.csv"
        df_players = pd.read_csv(players_file)
        # Use the parse_player_years function to handle all cases
        career_years = df_players['Years Active'].apply(parse_player_years)
        df_players['Start_Year'] = [years[0] for years in career_years]
        df_players['End_Year'] = [years[1] for years in career_years]
    except Exception as e:
        st.sidebar.error(f"Error loading player data: {str(e)}")
        df_players = pd.DataFrame()
    
    return df_stats, df_players

df, df_players = load_data()

# Sidebar for user options
st.sidebar.header("Dashboard Options")

# Era selection
selected_era = st.sidebar.selectbox(
    "Select Era",
    ["All"] + list(ERAS.keys())
)

# Time range toggle
show_modern_era = st.sidebar.checkbox("Show Modern Era Only (Since 1970)", value=True)

# Policy changes toggles
st.sidebar.header("Policy Changes")
show_policy_changes = {}
for policy, year in POLICY_CHANGES.items():
    show_policy_changes[policy] = st.sidebar.checkbox(f"Show {policy} ({year})")

# Career spans
st.sidebar.header("Career Spans")
if not df_players.empty:
    show_careers = st.sidebar.checkbox("Show Player Career Spans")
    if show_careers:
        players = sorted(df_players['Player'].unique()) if 'Player' in df_players.columns else []
        if len(players) > 0:
            selected_players = st.sidebar.multiselect(
                "Select Players to Show Career Spans",
                players
            )
        else:
            st.sidebar.warning("No player data found in the career spans file.")
else:
    st.sidebar.warning("⚠️ Player career data file not found or empty.")
    show_careers = False

# Column selection
st.sidebar.header("Statistics Selection")
available_columns = [col for col in df.columns if col not in ['SortYear', 'Season', 'Player']]

# Add ratio calculation option
calculation_type = st.sidebar.radio(
    "Select Analysis Type",
    ["Single Statistics", "Calculate Ratio"]
)

if calculation_type == "Single Statistics":
    columns_for_graph = st.sidebar.multiselect(
        "Select statistics to graph",
        available_columns,
        default=["Points"]
    )
else:
    # Ratio calculation
    numerator = st.sidebar.selectbox("Select Numerator", available_columns, index=available_columns.index("Points") if "Points" in available_columns else 0)
    denominator = st.sidebar.selectbox("Select Denominator", available_columns, index=available_columns.index("Games Played") if "Games Played" in available_columns else 0)
    ratio_name = f"{numerator}/{denominator}"
    columns_for_graph = [ratio_name]

# Visualization Controls
st.sidebar.header("Visualization Controls")
# Year range slider
min_year = int(df['SortYear'].min())
max_year = int(df['SortYear'].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(1970 if show_modern_era else min_year, max_year)
)

# Y-axis scale
y_scale = st.sidebar.radio("Y-axis Scale", ["Linear", "Logarithmic"])

# Moving average smoothing
show_smoothed = st.sidebar.checkbox("Show Smoothed Trend")
if show_smoothed:
    window_size = st.sidebar.slider("Smoothing Window Size", 1, 10, 3)

# Main display area
st.title("NBA Historical Statistics Dashboard")

# Filter data based on all selections
df_filtered = df.copy()
if selected_era != "All":
    start_year, end_year = ERAS[selected_era]
    df_filtered = df_filtered[df_filtered['SortYear'].between(start_year, end_year)]
if show_modern_era:
    df_filtered = df_filtered[df_filtered['SortYear'] >= 1970]
df_filtered = df_filtered[df_filtered['SortYear'].between(year_range[0], year_range[1])]

# Create visualization
if columns_for_graph:
    # Calculate ratio if needed
    if calculation_type == "Calculate Ratio":
        df_filtered[ratio_name] = df_filtered[numerator].astype(float) / df_filtered[denominator].astype(float)
    
    # Convert chosen columns to numeric values
    for col in columns_for_graph:
        if col in df_filtered.columns:
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')
    
    # Create plot
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot statistics
    for col in columns_for_graph:
        # Main line
        line = ax.plot(df_filtered['SortYear'], df_filtered[col], 
                marker='o', linewidth=2, markersize=6, label=col, alpha=0.6)
        
        # Add smoothed trend if requested
        if show_smoothed:
            smoothed = df_filtered[col].rolling(window=window_size, center=True).mean()
            ax.plot(df_filtered['SortYear'], smoothed, 
                   linewidth=3, label=f"{col} (Smoothed)", 
                   color=line[0].get_color(), alpha=1)
    
    # Set y-axis scale
    if y_scale == "Logarithmic":
        ax.set_yscale('log')
    
    # Dynamic x-axis ticks based on data range
    years = df_filtered['SortYear'].unique()
    year_range_span = years.max() - years.min()
    
    if year_range_span > 50:
        tick_spacing = 10
    elif year_range_span > 20:
        tick_spacing = 5
    else:
        tick_spacing = 2
    
    # Generate tick positions
    start_year = (years.min() // tick_spacing) * tick_spacing
    end_year = ((years.max() + tick_spacing) // tick_spacing) * tick_spacing
    tick_years = np.arange(start_year, end_year + 1, tick_spacing)
    
    # Set x-axis limits and ticks
    ax.set_xlim(years.min() - 1, years.max() + 1)
    ax.set_xticks(tick_years)
    ax.set_xticklabels(tick_years, rotation=45, ha='right')
    
    # Add minor ticks for better readability (limit the minor ticks)
    minor_locator = plt.MultipleLocator(1)
    minor_locator.MAXTICKS = 1000
    ax.xaxis.set_minor_locator(minor_locator)
    
    # Improve grid appearance
    ax.grid(True, which='major', linestyle='-', alpha=0.7)
    ax.grid(True, which='minor', linestyle=':', alpha=0.3)
    
    # Add policy change vertical lines
    for policy, year in POLICY_CHANGES.items():
        if show_policy_changes[policy]:
            if year >= years.min() and year <= years.max():
                ax.axvline(x=year, color='red', linestyle='--', alpha=0.5)
                # Position the text above the highest point in the graph
                y_max = max(df_filtered[columns_for_graph].max())
                ax.text(year, y_max * 1.02, policy, 
                       rotation=90, ha='right', va='bottom',
                       color='red', fontsize=10)

    # Add career spans if selected
    if show_careers and not df_players.empty:
        # Define a color palette for players
        colors = plt.cm.rainbow(np.linspace(0, 1, len(selected_players)))
        
        for player, color in zip(selected_players, colors):
            player_data = df_players[df_players['Player'] == player]
            if not player_data.empty:
                start_year = player_data['Start_Year'].iloc[0]
                end_year = player_data['End_Year'].iloc[0]
                ax.axvspan(start_year, end_year, 
                          alpha=0.3, 
                          color=color, 
                          label=f"{player} ({start_year}-{end_year})")

    # Customize plot appearance
    ax.set_xlabel("Season", fontsize=12, fontweight='bold')
    ax.set_ylabel("Value per Game", fontsize=12, fontweight='bold')
    title = f"NBA League Averages ({selected_era})" if selected_era != "All" else "NBA League Averages"
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add subtle background shading for different eras
    if selected_era == "All":
        for era, (start, end) in ERAS.items():
            if start >= years.min() and end <= years.max():
                ax.axvspan(start, end, alpha=0.1, color='gray')
                # Add era label
                ax.text((start + end) / 2, ax.get_ylim()[1], era,
                       ha='center', va='bottom', fontsize=8, alpha=0.7)
    
    # Improve legend appearance
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', 
             borderaxespad=0., frameon=True, fancybox=True, shadow=True)
    
    # Set margins to prevent cutoff
    plt.margins(x=0.02)
    
    # Adjust layout
    plt.tight_layout()
    
    # Display plot
    st.pyplot(fig)
    
    # Summary statistics
    st.markdown("---")
    st.write("### Summary Statistics")
    summary_df = df_filtered[columns_for_graph].describe()
    st.dataframe(summary_df.style.format(precision=2))
else:
    st.info("Please select at least one statistic to visualize.")

# Add glossary section at the bottom
st.markdown("---")
st.markdown("### Glossary")
st.markdown("#### Basic Statistics")
for stat, full_name in STAT_NAMES.items():
    if stat not in ["Pace", "eFG%", "TOV%", "ORB%", "FT/FGA", "ORtg", "TS%"]:
        st.markdown(f"- **{full_name}**: {STAT_EXPLANATIONS[full_name]}")

st.markdown("#### Advanced Statistics")
for stat, full_name in STAT_NAMES.items():
    if stat in ["Pace", "eFG%", "TOV%", "ORB%", "FT/FGA", "ORtg", "TS%"]:
        st.markdown(f"- **{full_name}**: {STAT_EXPLANATIONS[full_name]}")

st.markdown("#### Eras")
for era, (start, end) in ERAS.items():
    st.markdown(f"- **{era}**: {start}–{end}")

st.markdown("#### Policy Changes")
for policy, year in POLICY_CHANGES.items():
    st.markdown(f"- **{policy}**: {year}")
