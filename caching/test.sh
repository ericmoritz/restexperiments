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


# Test the Internal Data Caching methods
for i in control memcache libmc simple middleware varnish_indirect; do
  URI=http://localhost:8000/$i
  echo "Priming the $i cache"
  curl $URI > results/$i.out.txt
  assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"
  ab -n $SAMPLE_SIZE -c1 -e results/$i.csv -g results/$i.gplot $URI > results/$i.ab.txt
done

# Do the varnish testing
for i in esi; do
  URI=http://localhost:10001/$i
  echo "Priming the $i cache"
  curl $URI > results/$i.out.txt
  assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"
  ab -n $SAMPLE_SIZE -c1 -e results/$i.csv -g results/$i.gplot $URI  > results/$i.ab.txt
done

# Do the client side tests (aka AJAX)
for i in spouse children esi.tmpl; do
  URI=http://localhost:10001/$i
  echo "Priming the $i cache"
  curl $URI > results/ajax-$i.out.txt
  ab -n $SAMPLE_SIZE -c1 -e results/ajax-$i.csv -g results/ajax-$i.gplot $URI  > results/ajax-$i.ab.txt
done
