
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

    BASE="results/trans/$EXPERIMENT/n${SAMPLESIZE}c${CONCURRENCY}/$TESTNAME"

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

    mkdir -p "results/trans/${PHASE}/n${SAMPLESIZE}c${CONCURRENCY}/"
    rm "results/trans/${PHASE}/n${SAMPLESIZE}c${CONCURRENCY}/*"
    
    benchmark "${PHASE}"\
    	"control"\
        "http://localhost:8000/transclusion/${PHASE}/control"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        ""

    benchmark "${PHASE}"\
    	"spouse"\
        "http://localhost:8000/transclusion/${PHASE}/spouse"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Gina Moritz"
    
    benchmark "${PHASE}"\
    	"children"\
        "http://localhost:8000/transclusion/${PHASE}/children"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "Aiden Moritz,Ethan Moritz"

    benchmark "${PHASE}"\
    	"children"\
        "http://localhost:8000/transclusion/${PHASE}/template"\
        "$SAMPLESIZE"\
    	"$CONCURRENCY"\
        "{{ spouse }};{{ children }}"

    benchmark "${PHASE}"\
    	"children"\
        "http://localhost:8000/transclusion/${PHASE}/direct/family"\
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


