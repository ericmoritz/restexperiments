
for PHASE in phase1 phase2 phase3; do
    mkdir -p docs/source/_static/data/${PHASE}/

    for i in data/${PHASE}/*/; do
        python bin/report.py $i
    done | python bin/report_to_csv.py tpr > docs/source/_static/data/${PHASE}/tpr.csv 
    
    
    for i in data/${PHASE}/*/;
     do python bin/report.py $i; 
    done | python bin/report_to_csv.py rps > docs/source/_static/data/${PHASE}/rps.csv 
done
