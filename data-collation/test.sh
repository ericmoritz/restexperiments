rm results/*

for i in control direct indirect; do
  URI=http://localhost:8000/$i
  echo "Testing $i"
  curl $URI > results/$i.out
  ab -n 1000 -c1 $URI  > results/$i.ab.txt
done

# do ESI through varnish
i=esi
echo "Testing $i"
URI=http://localhost:10001/$i
curl $URI > results/$i.out
ab -n 1000 -c1 $URI  > results/$i.ab.txt
