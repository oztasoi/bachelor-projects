# CmpE 321 Spring 2020 Project 2
# Database Management System Implementation

## Environment Settings:
- `Python version: 3.7.7 64-bit`

## How to Run:
- To run this project, change directory into proper place and run.
```
python3 2016400198/src/storageManager.py <input_file_path> <output_file_path>
```

## Possible Errors:
- If any `ValueError` is raised, invalid input is given to the project.
- Several causes:
    - Non-alphanumeric type_name or feature_name
    - Limit exceeds for values (stated between 0 and 10000).
    - Logic errors (e.g. one deleted record cannot be deleted once more)