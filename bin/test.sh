
function assertequal {
    if [ "$1" != "$2" ]; then
	echo "Got \"$1\""
	echo "Expected \"$2\""
	echo "Fail."
	exit 1
    fi
}

function benchmark {
    EXPERIMENT=$1
    TESTNAME=$2
    URI=$3
    SAMPLESIZE=$4
    CONCURRENCY=$5
    EXPECT=$6

    BASE="results/$EXPERIMENT/n${SAMPLESIZE}c${CONCURRENCY}/$TESTNAME"

    echo "Testing $TESTNAME $SAMPLESIZE $CONCURRENCY"
    echo "Download $URI"

    curl "$URI" > "$BASE.out"

    if [ "$EXPECT"x != "x" ]; then
        assertequal "$(cat $BASE.out)" "$EXPECT"
    fi
    echo "Benchmarking $URI"
    ab -k -n "$SAMPLESIZE" "-c$CONCURRENCY" "$URI" > "$BASE.ab.txt"

}

# The phase one benchmarking
function base_app_test {
    PHASE=$1
    SAMPLESIZE=$2
    CONCURRENCY=$3

    mkdir -p "results/${PHASE}/n${SAMPLESIZE}c${CONCURRENCY}/"
    rm "results/${PHASE}/n${SAMPLESIZE}c${CONCURRENCY}/*"

    echo "sample: $SAMPLESIZE concurrency: $CONCURRENCY" > results/${PHASE}/config.txt

    benchmark "${PHASE}"\
        "control"\
        "http://localhost:8000/${PHASE}/control"\
    	"$SAMPLESIZE"\
    	"$CONCURRENCY"\
    	"Gina Moritz;Aiden Moritz,Ethan Moritz"
    
    benchmark "${PHASE}"\
    	"spouse"\
        "http://localhost:8000/${PHASE}/restful/spouse"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Gina Moritz"
    
    benchmark "${PHASE}"\
    	"children"\
        "http://localhost:8000/${PHASE}/restful/children"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Aiden Moritz,Ethan Moritz"
    
    benchmark "${PHASE}"\
    	"traditional-direct"\
        "http://localhost:8000/${PHASE}/conventional/direct/family"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"
    
    benchmark "${PHASE}"\
        "restful-direct"\
        "http://localhost:8000/${PHASE}/restful/direct/family"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"

    benchmark "${PHASE}"\
        "restful-indirect"\
        "http://localhost:8000/${PHASE}/restful/indirect/family"\
        "$SAMPLESIZE"\
        "$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"


    benchmark "${PHASE}"\
	"restful-esi"\
        "http://localhost:10001/${PHASE}/restful/esi/family"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"


}

function phase1 {
    base_app_test "phase1" $1 $2
}

function phase2 {
    base_app_test "phase2" $1 $2
}

phase1 10000 1
phase1 10000 250
phase1 10000 500
phase1 10000 750
phase1 10000 1000

phase2 10000 1
phase2 10000 250
phase2 10000 500
phase2 10000 750
phase2 10000 1000

