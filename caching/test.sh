rm results/*

SAMPLE_SIZE=$1
function assertequal {
    if [ "$1" != "$2" ]; then
	echo "Got \"$1\""
	echo "Expected \"$2\""
	echo "Fail."
	exit 1
    fi
}

# Precache the resources
assertequal "$(curl http://localhost:10001/spouse)" "Gina Moritz"
assertequal "$(curl http://localhost:10001/children)" "Aiden Moritz,Ethan Moritz"
assertequal "$(curl http://localhost:8000/spouse)" "Gina Moritz"
assertequal "$(curl http://localhost:8000/children)" "Aiden Moritz,Ethan Moritz"
assertequal "$(curl http://localhost:8000/mw_spouse)" "Gina Moritz"
assertequal "$(curl http://localhost:8000/mw_children)" "Aiden Moritz,Ethan Moritz"

# Test the Internal Data Caching methods
for i in control memcache libmc simple middleware varnish_indirect; do
  URI=http://localhost:8000/$i
  echo "Priming the $i cache"
  curl $URI > results/$i.out.txt
  assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"
  ab -n $SAMPLE_SIZE -c1 $URI  > results/$i.ab.txt
done

# Do the varnish testing
for i in memcache libmc simple middleware varnish_indirect esi; do
  URI=http://localhost:10001/$i
  echo "Priming the $i cache"
  curl $URI > results/varnish-$i.out.txt
  assertequal "$(cat results/varnish-$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"
  ab -n $SAMPLE_SIZE -c1 $URI  > results/varnish-$i.ab.txt
done
