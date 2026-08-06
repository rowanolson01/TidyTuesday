# Tidy Tuesday Archive, Rowan Olson

## 2026 Week 31 - Basotho Wool Trade

![Basotho Wool Markets Keep Different Calendars](2026%20Week%2031%20Basotho%20Wool/basothowool.png)

This week's TidyTuesday explored international trade data from the UN Comtrade Database, focusing on **Basotho wool exports** recorded by importing countries between 2010 and 2024.

Rather than comparing the size of each trading partner, I focused on **when each market purchases wool throughout the year**. By converting every importer's monthly trade into a share of its own annual total, the visualization highlights the seasonal purchasing calendar unique to each destination.

Despite sourcing wool from the same country, the four largest importers exhibit strikingly different buying patterns. South Africa concentrates purchases late in the year, China peaks during April, India reaches its maximum in May, and Uruguay's imports are heavily concentrated at the beginning of the calendar year.

Together, these distributions illustrate that international trade relationships are distinguished not only by **how much** countries buy, but also by **when** they buy it.

**Links:**  
[View Code](2026%20Week%2031%20Basotho%20Wool/basothowool.py) |  
[Basotho Wool Dataset](2026%20Week%2031%20Basotho%20Wool/basotho_wool.csv) |  
[TidyTuesday Week 31](https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-08-04)

## 2026 Week 30 - Ecotourism

![Four Seasons. Four Wildlife Maps.](2026%20Week%2030%20Ecotourism/ecotourism.png)

This week's TidyTuesday explored the **ecotourism** package, containing georeferenced observations of four iconic Australian species recorded between 2014 and 2024.

Rather than mapping where each species can be found, I focused on **how Australia's wildlife landscape changes throughout the year**. By dividing the observations into the four Southern Hemisphere seasons, the visualization reveals how the same continent takes on a very different ecological character as species become more or less active over time.

The strongest seasonal shifts come from orchids, whose observations peak during winter and spring in southwestern Australia, while Gouldian finches remain concentrated across the tropical north. Manta rays and glowworms occupy much narrower geographic niches that remain comparatively stable throughout the year.

Together, these maps illustrate how seasonality shapes not only when species are observed, but the overall ecological landscape experienced across Australia.

**Links:**  
[View Code](2026%20Week%2030%20Ecotourism/ecotourism.py) |  
[Ecotourism Dataset](2026%20Week%2030%20Ecotourism/occurrences.csv) |  
[TidyTuesday Week 30](https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-07-28)

## 2026 Week 29 - Near-Death Experiences

![The "Classic" Near-Death Experience Isn't Typical](2026%20Week%2029%20Near-Death%20Experiences/nderf.png)

This week's TidyTuesday explored the Near Death Experience Research Foundation (NDERF) dataset, containing hundreds of firsthand near-death experience reports alongside AI-detected themes extracted from each narrative.

Rather than examining individual stories, I focused on **how representative the commonly imagined near-death experience actually is**. By comparing the share of reports containing each detected phenomenon, the visualization separates the features that are widespread from those that are relatively uncommon.

The results suggest that the popular image of a near-death experience is built largely from memorable but infrequent events. Only **clinical death** and **out-of-body experiences** appear in a majority of reports, while phenomena such as unity, ESP, future visions, past lives, and alien encounters occur in a much smaller minority of cases.

Together, these distributions illustrate an important lesson in descriptive statistics: the most recognizable parts of a phenomenon are not always the parts that occur most often.

**Links:**  
[View Code](2026%20Week%2029%20Near-Death%20Experiences/nderf.py) |  
[NDERF Dataset](2026%20Week%2029%20Near-Death%20Experiences/nde_experiences.csv) |  
[TidyTuesday Week 29](https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-07-21)

## 2026 Week 28 - Penguins

![Most Penguin Genera Occupy Distinct Body Plans](2026%20Week%2028%20Penguins/penguins.png)

This week's TidyTuesday explored the AVONET penguin dataset, containing detailed morphological measurements for penguin species spanning six genera.

Rather than comparing individual measurements such as beak length or wing size, I used **principal component analysis (PCA)** to examine how overall body plans differ across penguin genera. By reducing ten standardized body measurements into two principal components, the visualization reveals the underlying morphological space occupied by each group.

Most genera form distinct clusters, suggesting that closely related species share characteristic body proportions. The most notable exception is the substantial overlap between *Eudyptes* and *Pygoscelis*, indicating that despite belonging to different genera, they occupy remarkably similar regions of morphospace. Meanwhile, the large-bodied *Aptenodytes* penguins stand apart from every other genus.

Together, these distributions illustrate how multivariate analysis can reveal broad patterns in morphology that would be difficult to recognize by comparing individual traits alone.

**Links:**  
[View Code](2026%20Week%2028%20Penguins/penguins.py) |  
[AVONET Penguin Dataset](2026%20Week%2028%20Penguins/many_penguins.csv) |  
[TidyTuesday Week 28](https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-07-14)

## 2026 Week 27 - UFC

![Every UFC Division Has a Different Way to Win](2026%20Week%2027%20UFC/ufc.png)

This week's TidyTuesday explored the Ultimate UFC Dataset, containing thousands of professional mixed martial arts fights across every UFC weight division.

Rather than comparing individual fighters or predicting winners, I focused on **how the composition of fight outcomes changes across weight classes**. By comparing the share of fights ending by knockout, submission, or decision, the visualization highlights the distinct finishing identities of each division.

The clearest trend is that knockouts become steadily less common as divisions get lighter, while submission rates remain remarkably consistent. Rather than replacing knockouts with more submissions, lighter divisions see a much larger share of fights reach the judges' scorecards.

Together, these distributions illustrate how each UFC division develops its own competitive style, with the biggest difference between divisions being not how often fighters submit their opponents, but how often they knock them out.

**Links:**  
[View Code](2026%20Week%2027%20UFC/ufc.py) |  
[Ultimate UFC Dataset](2026%20Week%2027%20UFC/ultimate_ufc_dataset.csv) |  
[TidyTuesday Week 27](https://github.com/rfordatascience/tidytuesday/tree/main/data/2026/2026-07-07)

## 2026 Week 26 - Wrecks

![The Age of Sail Gave Way to Steam](2026%20Week%2026%20Wrecks/wrecks.png)

This week's TidyTuesday explored the Wreck Inventory of Ireland Database, containing thousands of recorded shipwrecks spanning several centuries.

Rather than mapping where wrecks occurred, I focused on **how the composition of Ireland's shipwrecks changed over time**. By normalizing the frequency of each vessel type, the visualization highlights the gradual transition from traditional sailing vessels, such as sloops, brigs, schooners, and barques, to steam-powered ships during the late nineteenth and early twentieth centuries.

Because each vessel class is scaled independently, the chart emphasizes *when* each type was most commonly lost rather than *how many* were lost. Together, these distributions illustrate the technological evolution of maritime trade and transport as reflected through Ireland's recorded shipwrecks.

**Links:**  
[View Code](2026%20Week%2026%20Wrecks/wrecks.py) |
[Wreck Inventory Dataset](https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-06-30/wreck_inventory.csv) |
[TidyTuesday Week 26](https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-06-30/readme.md)

## 2026 Week 25 - Papal Encyclicals

![Why Have Papal Encyclicals Become So Rare?](2026%20Week%2025%20Papal%20Encyclicals/papalencyclicals.png)

This week's TidyTuesday explored papal encyclicals—formal letters issued by the pope on matters of doctrine, society, and the Church.

Rather than analyzing the text itself, I stepped back to examine a broader historical pattern. Plotting annual encyclical publication over nearly 150 years reveals a striking decline in frequency. While this visualization does **not** establish causation, it raises an interesting question: as new communication technologies such as radio, television, and eventually the internet emerged, did encyclicals become a less necessary medium for reaching a global audience?

The chart is intended as the beginning of that discussion rather than its conclusion.

**Links:**  
[View Code](2026%20Week%2025%20Papal%20Encyclicals/papalencyclicals.py) |
[Encyclicals Dataset](https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-06-23/encyclicals.csv) |
[Papal Metadata](https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-06-23/papal_encyclicals.csv) |
[Scripture References](https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-06-23/scripture_references.csv)