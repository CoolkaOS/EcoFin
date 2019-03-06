import wr
results = wr.read_results()
nicks = open('nicks.txt','w', encoding='utf-8')
for id in results:
    nicks.write(results[id][1]+'\n')
nicks.close()