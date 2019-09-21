#!/usr/bin/env Rscript
# https://www.r-bloggers.com/passing-arguments-to-an-r-script-from-command-lines/
args = commandArgs(trailingOnly=TRUE)

# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("[usage] stamen.r <csv inputfile> <outputfile>", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "map.pdf"
}

print(paste("args[0]", args[0]))
print(paste("args[1]", args[1]))
print(paste("args[2]", args[2]))

## main
library(ggplot2)
library(ggmap)
library(ggrepel)

# setup SF coordinates, excludes Treasure Island
coord = as.numeric(c("-122.52494808","37.70308934","-122.34696604", "37.81657339"))
names(coord) <- c("left", "bottom", "right", "top") # https://rpubs.com/sowmya21jan/338762

# get Stamen map tiles to create a basemap
# https://www.rdocumentation.org/packages/ggmap/versions/3.0.0/topics/get_stamenmap
basemap <- get_stamenmap(bbox = coord,zoom = 13,maptype = "terrain")


# http://zevross.com/blog/2014/07/16/mapping-in-r-using-the-ggplot2-package/
m <- read.csv("addr.csv", stringsAsFactors=FALSE)
mm <- ggmap(basemap) + geom_point(data = m, aes(x=long, y=lat), color="red", size=0.25)
mm <- mm + geom_label_repel(data=m, 
                            aes(x=long, y=lat,label=addy), 
                            size=2,
                            vjust=-2,
                            hjust=1)


