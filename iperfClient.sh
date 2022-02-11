while true
do
  iperf -c 10.0.0.1 -p 5566
  sleep $1
done
