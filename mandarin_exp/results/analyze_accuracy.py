#!/usr/bin/env python3
"""
Analyze accuracy of experiment results by experiment type, quantifier, and scenario.
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

def analyze_results(csv_file):
    """Analyze accuracy metrics from results CSV file."""
    
    # Store results by experiment type
    by_experiment = defaultdict(lambda: {'correct': 0, 'total': 0})
    by_quantifier = defaultdict(lambda: {'correct': 0, 'total': 0})
    by_scenario = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exp_type = row['experiment'].strip()
            quantifier = row['quantifier'].strip() if row['quantifier'].strip() else 'N/A'
            scenario = row['scenario'].strip() if row['scenario'].strip() else 'N/A'
            is_correct = int(row['correct'])
            
            by_experiment[exp_type]['total'] += 1
            by_experiment[exp_type]['correct'] += is_correct
            
            if exp_type in ['ESQ', 'DIST']:  # Only these have quantifiers
                by_quantifier[quantifier]['total'] += 1
                by_quantifier[quantifier]['correct'] += is_correct
                
                by_scenario[scenario]['total'] += 1
                by_scenario[scenario]['correct'] += is_correct
    
    return by_experiment, by_quantifier, by_scenario

def print_results(by_experiment, by_quantifier, by_scenario):
    """Print formatted accuracy results."""
    
    print("="*60)
    print("ACCURACY BY EXPERIMENT TYPE")
    print("="*60)
    for exp_type in sorted(by_experiment.keys()):
        stats = by_experiment[exp_type]
        pct = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{exp_type:15} | Correct: {stats['correct']:3}/{stats['total']:3} | {pct:6.2f}%")
    
    print("\n" + "="*60)
    print("ACCURACY BY QUANTIFIER (ESQ/DIST only)")
    print("="*60)
    for quantifier in sorted(by_quantifier.keys()):
        stats = by_quantifier[quantifier]
        pct = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{quantifier:15} | Correct: {stats['correct']:3}/{stats['total']:3} | {pct:6.2f}%")
    
    print("\n" + "="*60)
    print("ACCURACY BY SCENARIO (ESQ/DIST only)")
    print("="*60)
    for scenario in sorted(by_scenario.keys()):
        stats = by_scenario[scenario]
        pct = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{scenario:30} | Correct: {stats['correct']:3}/{stats['total']:3} | {pct:6.2f}%")

def main():
    """Main function."""
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        # Find the most recent results file
        results_dir = Path(__file__).parent
        csv_files = sorted(results_dir.glob("results_*.csv"), reverse=True)
        
        if not csv_files:
            print("No results CSV files found in current directory.")
            sys.exit(1)
        
        csv_file = csv_files[0]
        print(f"Analyzing: {csv_file.name}\n")
    
    by_experiment, by_quantifier, by_scenario = analyze_results(csv_file)
    print_results(by_experiment, by_quantifier, by_scenario)

if __name__ == '__main__':
    main()
