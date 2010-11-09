rm results/*

function assertequal {
    if [ "$1" != "$2" ]; then
	echo "Got \"$1\""
	echo "Expected \"$2\""
	echo "Fail."
	exit 1
    fi
}

for i in control direct indirect; do
  URI=http://localhost:8000/$i
  echo "Testing $i"
  curl $URI > results/$i.out.txt

  assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"

  ab -n 10000 -c1 $URI  > results/$i.ab.txt
done

# do ESI through varnish
i=esi
echo "Testing $i"
URI=http://localhost:10001/$i
curl $URI > results/$i.out.txt
assertequal "$(cat results/$i.out.txt)" "Gina Moritz;Aiden Moritz,Ethan Moritz"
ab -n 10000 -c1 $URI  > results/$i.ab.txt

