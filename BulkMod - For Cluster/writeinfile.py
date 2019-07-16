

BOTTOMFILE = "bottomBMin"

for simnum in range(2,11):

    NEWFILENAME = "in.bulkCuNi" + str(simnum)


    reader = open(BOTTOMFILE,mode = "r")
    writer = open(NEWFILENAME,mode = "w")
    writer.write("# ---------------- Define Variables ---------------\n")
    writer.write("variable\tSIMNUM equal " + str(simnum) + "\n")
    for line in reader:
        writer.write(line)
