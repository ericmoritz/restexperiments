rm results/*

SAMPLE_SIZE=10000
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

# Test the Internal Data Caching methods
for i in control memcache libmc simple middleware; do
  URI=http://localhost:8000/$i
  echo "Priming the $i cache"
  curl $URI > results/$i.out.txt
  assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"
  ab -n $SAMPLE_SIZE -c1 $URI  > results/$i.ab.txt
done

# Do the varnish testing
for i in varnish_indirect esi; do
  URI=http://localhost:10001/$i
  echo "Priming the $i cache"
  curl $URI > results/$i.out.txt
  assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"
  ab -n $SAMPLE_SIZE -c1 $URI  > results/$i.ab.txt
done
