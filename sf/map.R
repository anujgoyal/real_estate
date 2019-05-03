#!/usr/bin/env Rscript
# https://www.r-bloggers.com/passing-arguments-to-an-r-script-from-command-lines/
library(ggplot2)
library(ggmap)
library(ggrepel)

args = commandArgs(trailingOnly=TRUE)

# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("[usage] ./map.R <csv inputfile> <outputfile>", call.=FALSE)
} else if (length(args)==1) {
  args[2] = "map" # default output file
  #print(paste("args[1]", args[1]))
  #print(paste("args[2]", args[2]))
}

# setup SF coordinates, excludes Treasure Island
coord = as.numeric(c("-122.52494808","37.70308934","-122.34696604", "37.81657339"))
# https://rpubs.com/sowmya21jan/338762
names(coord) <- c("left", "bottom", "right", "top") 
# Stamen: http://maps.stamen.com
# https://www.rdocumentation.org/packages/ggmap/versions/3.0.0/topics/get_stamenmap
basemap <- get_stamenmap(bbox = coord,zoom = 13,maptype = "terrain")

# something is wrong with mapTheme()
# bmMap <- ggmap(basemap) + mapTheme() + labs(title="San Francisco basemap") 
bmMap <- ggmap(basemap) + labs(title="San Francisco basemap") 

#basemap <- get_stamenmap(bbox = coord, zoom = 13, maptype = "toner-lite")

# http://zevross.com/blog/2014/07/16/mapping-in-r-using-the-ggplot2-package/
m <- read.csv("addr.csv", stringsAsFactors=FALSE)
#head(m)
mm <- ggmap(basemap) + geom_point(data = m, aes(x=long, y=lat), color="red", size=0.25)

# NB: this covered up the points
# mm <- mm + geom_label(data=m, aes(x=long, y=lat,label=addy),hjust=0, vjust=0)

# https://stackoverflow.com/questions/51527217/r-ggmap-add-annotation-superimposed-on-map
# https://stackoverflow.com/questions/15624656/label-points-in-geom-point
mm <- mm + geom_label_repel(data=m, 
                            aes(x=long, y=lat,label=addy), 
                            size=2,
                            vjust=-2,
                            hjust=1)
# save as pdf
pdf("map.pdf", height=10, width=10)
  plot(mm)
dev.off()

