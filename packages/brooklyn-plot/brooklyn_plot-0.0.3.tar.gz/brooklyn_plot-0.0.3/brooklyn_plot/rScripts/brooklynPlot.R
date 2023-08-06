#dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE, showWarnings = FALSE)  # create personal library
#.libPaths(Sys.getenv("R_LIBS_USER"))  # add to the path
#packages <- c("ggplot2")
#install.packages(setdiff(packages, rownames(installed.packages())))

library(ggplot2)

args <- commandArgs(TRUE)
gcsvdata <- read.csv(file = args[1], header=TRUE)
gdata <- subset(gcsvdata, select = c("chromosome_name", "percent_occurence"))
colnames(gdata)[colnames(gdata) == "chromosome_name"] ="chr"
gdata$row_n <- row.names(gdata)
gdata$row_n <- row.names(gdata)

gdata["chr"][gdata["chr"] == "X"] <- "23"
gdata["chr"][gdata["chr"] == "Y"] <- "24"
gdata["chr"][gdata["chr"] == "M" | gdata["chr"] == "MT"] <- "25"

gdata$group <- factor(as.numeric(gdata$chr))

pdf(file=args[2], width=8,height=8)

myCol <- rep(c("#FFC20A","#0C7BDC"), length.out = length(levels(gdata$group)))

chr_names <- c(
  `1` = "Chr1", `2` = "Chr2", `3` = "Chr3", `4` = "Chr4", `5` = "Chr5",
  `6` = "Chr6", `7` = "Chr7", `8` = "Chr8", `9` = "Chr9", `10` = "Chr10",
  `11` = "Chr11", `12` = "Chr12", `13` = "Chr13", `14` = "Chr14",`15` = "Chr15",
  `16` = "Chr16", `17` = "Chr17", `18` = "Chr18", `19` = "Chr19", `20` = "Chr20",
  `21` = "Chr21", `22` = "Chr22", `23` = "ChrX", `24` = "ChrY", `25` = "ChrMT"
)

ggplot(gdata, aes(x = row_n, y = percent_occurence, fill = group)) +
	ylim(0, 100) + 
      	geom_col() + 
      	facet_grid(. ~group,  scale="free_x", space="free", switch="x",labeller = as_labeller(chr_names)) +
      	labs(title = "Brooklyn plot across chromosomes", y = "Percent occurrence", x = "Chromosomes") +
      	theme(axis.text.x=element_blank(), axis.ticks.x=element_blank())+ scale_fill_manual(values=c(myCol)) + 
      	theme(legend.position = "none") +
      	theme(axis.line = element_line(linewidth = 0.5, color = "black")) + 
      	theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank())+ theme(strip.text.x = element_text(angle = 90))  + theme(panel.spacing.x=unit(0.1, "lines"))

garbage <- dev.off()
