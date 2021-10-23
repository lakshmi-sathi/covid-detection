
data = []
with open('corona_data_processed.csv') as fp:
    for line in fp:
        line = line[:-1]
        data.append(line.split(","))

print(data[0:2])
