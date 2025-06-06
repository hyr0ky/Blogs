
- 多线程
```
cat ip.txt | xargs -P 10 -I {} sh -c 'sudo nmap -sT --min-rate 10000 -p- {} -oA nmapscan/{}_ports'

sudo nmap -sS -Pn -n --open --min-hostgroup 4 --min-parallelism 1024 --host-timeout 30 -T4 -v -oG result.txt -iL ip.txt

sudo nmap -sT -Pn -n --open --min-rate 10000 --host-timeout 30 -v -oG nmapscan/ports -iL ip.txt -oA nmapscan/ports
```