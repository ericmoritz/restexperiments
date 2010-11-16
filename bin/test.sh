
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
function phase1 {
    SAMPLESIZE=$1
    CONCURRENCY=$2

    mkdir -p "results/phase1/n${SAMPLESIZE}c${CONCURRENCY}/"
    rm "results/phase1/n${SAMPLESIZE}c${CONCURRENCY}/*"

    echo "sample: $SAMPLESIZE concurrency: $CONCURRENCY" > results/phase1/config.txt

    benchmark "phase1"\
        "control"\
        "http://localhost:8000/phase1/control"\
	"$SAMPLESIZE"\
	"$CONCURRENCY"\
	"Gina Moritz;Aiden Moritz,Ethan Moritz"

    benchmark "phase1"\
	"spouse"\
        "http://localhost:8000/phase1/restful/spouse"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Gina Moritz"

    benchmark "phase1"\
	"children"\
        "http://localhost:8000/phase1/restful/children"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Aiden Moritz,Ethan Moritz"

    benchmark "phase1"\
	"traditional-direct"\
        "http://localhost:8000/phase1/conventional/direct/family"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"

    benchmark "phase1"\
        "restful-direct"\
        "http://localhost:8000/phase1/restful/direct/family"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"

    #benchmark "phase1"\
    #    "restful-indirect"\
    #    "http://localhost:8000/phase1/restful/indirect/family"\
    #    "$SAMPLESIZE"\
    #    "$CONCURRENCY"\
    #    "Gina Moritz;Aiden Moritz,Ethan Moritz"


    benchmark "phase1"\
	"restful-esi"\
        "http://localhost:10001/phase1/restful/esi/family"\
        "$SAMPLESIZE"\
	"$CONCURRENCY"\
        "Gina Moritz;Aiden Moritz,Ethan Moritz"


}

phase1 100000 1
phase1 100000 10
phase1 100000 100
phase1 100000 1000

