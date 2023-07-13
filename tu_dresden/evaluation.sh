# iterate from 10000 to 100000 with step 10000, run pipeline.py with argument --facts $i

for i in $(seq 1 1 10)
do
  fact_nr=$((i * 100))
  python3 pipeline.py --facts $fact_nr --glassbox 1
  out_data_dir="output/$fact_nr.json"
  java -jar proof_extractor.jar $out_data_dir
done
