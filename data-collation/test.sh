rm results/*

function assertequal {
    if [ "$1" != "$2" ]; then
	echo "Got \"$1\""
	echo "Expected \"$2\""
	echo "Fail."
	exit 1
    fi
}

SAMPLE_SIZE=$1

for i in control direct indirect; do
  URI=http://localhost:8000/$i
  echo "Testing $i"
  curl $URI > results/$i.out.txt

  assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"

  ab -n $SAMPLE_SIZE -c1 $URI  > results/$i.ab.txt
done

# do ESI through varnish
i=esi
echo "Testing $i"
URI=http://localhost:10001/$i
curl $URI > results/$i.out.txt
assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"
ab -n $SAMPLE_SIZE -c1 $URI  > results/$i.ab.txt

# Fetch the two resources and the esi resource to simulate the requests needed
# to do clientside collation
for i in spouse children esi; do
  URI=http://localhost:8000/$i
  echo "Testing ajax-$i"
  curl $URI > results/ajax-$i.out.txt
  ab -n $SAMPLE_SIZE -c1 $URI  > results/ajax-$i.ab.txt
done
