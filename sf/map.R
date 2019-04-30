library(ggplot2)
library(ggmap)
library(ggrepel)

# setup SF coordinates, excludes Treasure Island
coord = as.numeric(c("-122.52494808","37.70308934","-122.34696604", "37.81657339"))
names(coord) <- c("left", "bottom", "right", "top") # https://rpubs.com/sowmya21jan/338762
# https://www.rdocumentation.org/packages/ggmap/versions/3.0.0/topics/get_stamenmap
basemap <- get_stamenmap(bbox = coord,zoom = 13,maptype = "terrain")
# ggmap 
bmMap <- ggmap(basemap) + mapTheme() + labs(title="San Francisco basemap")
bmMap

#basemap <- get_stamenmap(bbox = coord, zoom = 13, maptype = "toner-lite")

# http://zevross.com/blog/2014/07/16/mapping-in-r-using-the-ggplot2-package/
m <- read.csv("addr.csv", stringsAsFactors=FALSE)
head(m)
mm <- ggmap(basemap) + geom_point(data = m, aes(x=long, y=lat), color="red", size=0.25)
#mm <- mm + geom_label(data=m, aes(x=long, y=lat,label=addy),hjust=0, vjust=0)
mm <- mm + geom_label_repel(data=m, 
                            aes(x=long, y=lat,label=addy), 
                            size=2,
                            vjust=-2,
                            hjust=1)
# https://stackoverflow.com/questions/51527217/r-ggmap-add-annotation-superimposed-on-map
# https://stackoverflow.com/questions/15624656/label-points-in-geom-point

