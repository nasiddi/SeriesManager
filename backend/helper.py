
with open('data/tvdb_report.txt') as f:
    content = f.readlines()
shows = []
for line in content:
    if line.startswith('{') or line.startswith('2') or line.startswith(' '):
        continue
    if line not in shows:
        shows.append(line)
    else:
        print(line.strip('\n'))
