
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

    echo "Testing $TESTNAME n$SAMPLESIZE c$CONCURRENCY"
    echo "Download $URI"

    curl "$URI" > "$BASE.out"

    if [ "$EXPECT"x != "x" ]; then
        assertequal "$(cat $BASE.out)" "$EXPECT"
    fi
    echo "Benchmarking $URI"
    ab "-n$SAMPLESIZE" "-c$CONCURRENCY" "$URI" > "$BASE.ab.txt"

}

# The phase one benchmarking
function base_app_test {
    PHASE=$1
    SAMPLESIZE=$2
    CONCURRENCY=$3

    mkdir -p "results/${PHASE}/n${SAMPLESIZE}c${CONCURRENCY}/"
    rm "results/${PHASE}/n${SAMPLESIZE}c${CONCURRENCY}/*"

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
	"ajax-template"\
        "http://localhost:8000/${PHASE}/restful/esi/family"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"

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


    benchmark "${PHASE}"\
        "control"\
        "http://localhost:8000/${PHASE}/control"\
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

function phase3 {
    PHASE="phase3"
    SAMPLESIZE=$1
    CONCURRENCY=$2

    mkdir -p "results/${PHASE}/n${SAMPLESIZE}c${CONCURRENCY}/"
    rm "results/${PHASE}/n${SAMPLESIZE}c${CONCURRENCY}/*"

    benchmark "${PHASE}"\
    	"convetional-memcached"\
        "http://localhost:8000/${PHASE}/conventional/memcache,direct/family"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"
    
    benchmark "${PHASE}"\
    	"spouse"\
        "http://localhost:10001/${PHASE}/restful/spouse"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Gina Moritz"
    
    benchmark "${PHASE}"\
    	"children"\
        "http://localhost:10001/${PHASE}/restful/children"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Aiden Moritz,Ethan Moritz"
    
    benchmark "${PHASE}"\
	"ajax-template"\
        "http://localhost:8000/${PHASE}/restful/ajax/family"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"

    benchmark "${PHASE}"\
        "restful-direct"\
        "http://localhost:10001/${PHASE}/restful/http,direct/family"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"

    benchmark "${PHASE}"\
	"restful-esi"\
        "http://localhost:10001/${PHASE}/restful/http,esi/family"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"


    benchmark "${PHASE}"\
        "control"\
        "http://localhost:8000/${PHASE}/control"\
    	"$SAMPLESIZE"\
    	"$CONCURRENCY"\
    	"Gina Moritz;Aiden Moritz,Ethan Moritz"

}

function http-test-suite {
    $1 10000 1
    $1 10000 250
    $1 10000 500
    $1 10000 750
    $1 10000 1000
}

http-test-suite phase1
http-test-suite phase2
http-test-suite phase3

