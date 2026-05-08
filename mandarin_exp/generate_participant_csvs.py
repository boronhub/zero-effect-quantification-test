import pandas as pd
import numpy as np
import os
from pathlib import Path


def generate_participant_csvs(num_participants):
    master_file = "stimulus_table_all_exps_zh.csv"
    df = pd.read_csv(master_file)
    
    # Separate experiments
    esq_df = df[df['Experiment'] == 'ESQ'].copy()
    dist_df = df[df['Experiment'] == 'DIST'].copy()
    filler_df = df[df['Experiment'] == 'Filler'].copy()
    
    print(f"Master file loaded:")
    print(f"  ESQ entries: {len(esq_df)}")
    print(f"  DIST entries: {len(dist_df)}")
    print(f"  Filler entries: {len(filler_df)}")
    print()
    
    # Create output directory
    output_dir = "participant_csvs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate CSV for each participant
    for participant_id in range(1, num_participants + 1):
        # Process ESQ: select 1 entry per condition for each item
        esq_selected = []
        for item in sorted(esq_df['Item'].unique()):
            item_data = esq_df[esq_df['Item'] == item]
            # Group by condition (1, 2, 3, 4)
            for condition in sorted(item_data['Condition'].unique()):
                condition_data = item_data[item_data['Condition'] == condition]
                # Randomly select 1 entry from this condition
                selected_row = condition_data.sample(n=1, random_state=None)
                esq_selected.append(selected_row)
        
        esq_trials = pd.concat(esq_selected, ignore_index=True)
        
        # Process DIST: select 1 entry per condition for each item
        dist_selected = []
        for item in sorted(dist_df['Item'].unique()):
            item_data = dist_df[dist_df['Item'] == item]
            # Group by condition (1, 2, 3, 4)
            for condition in sorted(item_data['Condition'].unique()):
                condition_data = item_data[item_data['Condition'] == condition]
                # Randomly select 1 entry from this condition
                selected_row = condition_data.sample(n=1, random_state=None)
                dist_selected.append(selected_row)
        
        dist_trials = pd.concat(dist_selected, ignore_index=True)
        
        # Filler: keep all fillers as-is
        filler_trials = filler_df.copy()
        
        # Combine all trials
        participant_df = pd.concat([esq_trials, dist_trials, filler_trials], ignore_index=True)
        
        # Shuffle the entire participant file
        participant_df = participant_df.sample(frac=1, random_state=None).reset_index(drop=True)
        
        # Save to CSV
        output_file = os.path.join(output_dir, f"participant_{participant_id:02d}.csv")
        participant_df.to_csv(output_file, index=False)
        
        # Print summary
        esq_count = len(esq_trials)
        dist_count = len(dist_trials)
        filler_count = len(filler_trials)
        total_count = len(participant_df)
        
        print(f"Participant {participant_id:02d}: {output_file}")
        print(f"  ESQ trials: {esq_count}")
        print(f"  DIST trials: {dist_count}")
        print(f"  Filler trials: {filler_count}")
        print(f"  Total trials: {total_count}")
    
    print(f"\nGenerated {num_participants} participant CSV files in '{output_dir}/' directory")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python generate_participant_csvs.py <number_of_participants>")
        sys.exit(1)
    
    try:
        num_participants = int(sys.argv[1])
        if num_participants <= 0:
            print("Error: Number of participants must be positive")
            sys.exit(1)
    except ValueError:
        print("Error: Number of participants must be an integer")
        sys.exit(1)
    
    generate_participant_csvs(num_participants)
