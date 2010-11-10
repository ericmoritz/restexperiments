
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
    EXPECT=$5
    BASE="results/$EXPERIMENT/$TESTNAME"

    echo "Testing $TESTNAME"
    echo "Download $URI"
    curl "$URI" > "$BASE.out"

    if [ "$EXPECT"x != "x" ]; then
        assertequal "$(cat $BASE.out)" "$EXPECT"
    fi
    echo "Benchmarking $URI"
    ab -n "$SAMPLESIZE" -c1 "$URI" > "$BASE.ab.txt"

}

# The phase one benchmarking
function phase1 {
    SAMPLESIZE=$1

    mkdir results/phase1
    rm results/phase1/*

    benchmark "phase1" "control" \
        "http://localhost:8000/phase1/control" \
        "$SAMPLESIZE" \
        "Gina Moritz;Aiden Moritz,Ethan Moritz"

    benchmark "phase1" "traditional-direct" \
        "http://localhost:8000/phase1/conventional/direct/family" \
        "$SAMPLESIZE" \
        "Gina Moritz;Aiden Moritz,Ethan Moritz"

    benchmark "phase1" "restful-direct" \
        "http://localhost:8000/phase1/restful/direct/family" \
        "$SAMPLESIZE" \
        "Gina Moritz;Aiden Moritz,Ethan Moritz"
}

SAMPLESIZE=$1
phase1 $SAMPLESIZE
