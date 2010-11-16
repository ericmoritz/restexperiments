for PHASE in "phase1"; do
    for i in data/$PHASE/*/; do
        python bin/report.py $i
    done | python bin/report_to_csv.py tpr > docs/source/data/phase1/tpr.csv 
    
    
    for i in data/$PHASE/*/;
     do python bin/report.py $i; 
    done | python bin/report_to_csv.py rps > docs/source/data/phase1/rps.csv 
done