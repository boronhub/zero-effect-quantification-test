# Filler Images Resolution and Copy Summary

## Overview
Successfully resolved and copied all image files for Filler entries from the stimulus table to a centralized Filler directory.

## Source Information
- **CSV File**: `stimulus_table_all_exps_zh.csv` (25 Filler rows with 20 unique images)
- **Experiment Image Sources**:
  - Experiment 1 ESQ - pictures: 89 SVG files
  - Experiment 2 DIST - pictures: 80 SVG files
  - Experiment 3 UB - pictures: 40 SVG files

## Process
The `copy_filler_images.py` script:
1. Parsed the stimulus CSV file and extracted all Filler entries
2. Identified 20 unique image filenames referenced by Filler trials
3. Scanned all three experiment image directories to locate each image
4. Copied matched images to `/Filler/` directory

## Results

### ✓ Successfully Copied (20/20 images)
Images from ESQ folder (9):
- pic1_empty_scope.svg (1 reference)
- pic15_empty_scope.svg (1 reference)
- pic15_small_control.svg (1 reference)
- pic11_small_control.svg (1 reference)
- pic5_empty_restrictor.svg (1 reference)
- pic6_empty_scope.svg (1 reference)
- pic6_small_control.svg (1 reference)
- pic8_empty_scope.svg (1 reference)
- pic9_empty_restrictor.svg (1 reference)

Images from DIST folder (3):
- pic106_psp_violation_target_right.svg (1 reference)
- pic107_psp_violation_target_right.svg (1 reference)
- pic110_target_target_left.svg (1 reference)

Images from UB folder (8):
- pic301_einige_some_but_not_all.svg (1 reference)
- pic302_einige_all.svg (1 reference)
- pic302_einige_some_but_not_all.svg (1 reference)
- pic304_einige_all.svg (2 references)
- pic307_einige_some_but_not_all.svg (1 reference)
- pic308_einige_all.svg (1 reference)
- pic312_einige_some_but_not_all.svg (1 reference)
- pic317_einige_all.svg (1 reference)

## Data Corrections Made
Fixed CSV formatting issues before copying:
1. **Row 413 (Filler Item 1002)**: Corrected image filename from `pic301_einige_some_but_not_all.svgTrial` to `pic301_einige_some_but_not_all.svg`
2. **Rows 410-411 (Filler Item 405)**: Added missing `.svg` extensions to `pic6_empty_scope`

## Filler Directory Structure
```
/home/boron/work/ling/ling514paper/original-source-code/materials/Filler/
├── pic1_empty_scope.svg
├── pic5_empty_restrictor.svg
├── pic6_empty_scope.svg
├── pic6_small_control.svg
├── pic8_empty_scope.svg
├── pic9_empty_restrictor.svg
├── pic11_small_control.svg
├── pic15_empty_scope.svg
├── pic15_small_control.svg
├── pic106_psp_violation_target_right.svg
├── pic107_psp_violation_target_right.svg
├── pic110_target_target_left.svg
├── pic301_einige_some_but_not_all.svg
├── pic302_einige_all.svg
├── pic302_einige_some_but_not_all.svg
├── pic304_einige_all.svg
├── pic307_einige_some_but_not_all.svg
├── pic308_einige_all.svg
├── pic312_einige_some_but_not_all.svg
└── pic317_einige_all.svg
```

## Next Steps
- The web experiment interface (`experiment.html`) can now reference Filler images from this centralized directory
- Consider updating image path resolution in the experiment interface to support Filler folder
- Verify SVG rendering in browser before running pilot study

## Files Generated/Modified
- **Created**: `copy_filler_images.py` - Reusable script for image resolution and copying
- **Modified**: `stimulus_table_all_exps_zh.csv` - Fixed formatting issues (2 corrections)
- **Created**: `Filler/` directory - Contains all 20 Filler images
