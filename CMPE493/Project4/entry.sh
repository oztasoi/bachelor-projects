clear
[ -d output ] && rm -rf output
[ ! -d output ] && mkdir output
python3 preprocess.py .
python3 raw_model.py
python3 feature_selection_model.py
python3 randomization.py