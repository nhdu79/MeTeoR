# iterate from 10000 to 100000 with step 10000, run pipeline.py with argument --facts $i

# for i in $(seq 1 1 10)
for i in 7 8 9 10
do
  fact_nr=$((i * 10000))
  python3 pipeline.py --facts $fact_nr --glassbox 0
  # out_data_dir="output/$fact_nr.json"
  # java -jar proof_extractor.jar $out_data_dir
done
