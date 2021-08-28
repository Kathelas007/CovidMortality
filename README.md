# Covid Mortality analysis

## Introduction
Without any doubt, the COVID-19 pandemic has impacted all of us. The question is, how do we measure the impact? 
There are plenty of statistics covering the number of new cases, test results and deaths. Unfortunately, 
methodologies vary across countries and therefore results may be either not as reliable as we might want 
or they require deeper understanding of said methodologies and other factors.

Mortality could be a simple indicator of the success or failure of individual countries concerning the pandemic. 
Mortality rate was partially decreased by lockdowns (for example, there were 15% less deaths from car 
 [accidents in the Czech republic](https://www.ibesip.cz/getattachment/Statistiky/Statistiky-nehodovosti-v-Ceske-republice/Dopravni-nehodovost-2020/20-12-NSBSP.pdf?lang=cs-CZ) in 2020. And hugely increased by Covid. Apart from deaths caused directly by this disease, it covers cases caused by 
 in the year 2020) and at the same time, hugely increased by COVID-19 
(apart from the COVID-19 cases, this also covers deaths caused indirectly because of the overwhelmed 
healthcare system and subsequent delayed or insufficient care.)

## Analysis
The map on the left shows difference in the number of average deaths in European countries between years 2016 — 2019 and 
the year 2020. 

The map on the right groups European countries by the percentage of mortality increase.  

![alt text](02_map.png)  

The second figure plots total mortality number for years 2016 — 2019 and the year 2020 in each country and sorts them 
by the percentage of the increase between those values.  

![alt text](01_barplot.png)

Average mortality for European countries between years 2016 — 2019 was 10.0 per 1000 inhabitants. It was 10% more (11.0) in the year 2020. 

As we can see, there are only three countries where the mortality decreased for the year 2020 instead — Norway, Iceland 
and France. This group is marked on the second map by black color.

Second group consists of countries from Denmark to Sweden, who were able to keep the number under 9.5. Suprisingly, 
Ukrajine belongs to them as well.

Next one covers rest of EU countries. The worst result from them has Poland, where the number of deaths has increased 
by 17% to 12.6. Czech Republic has slightly better result - 12.6, but still, it is probably not "Best in COVID".

Although, all of us have heard about strong waves in Spain or Italy, the highest mortality increase occurred in:
 Abania, Macedonia, Azerbajian and Armenia.

## Data source
Map: [leakyMirror](https://github.com/leakyMirror/map-of-europe)  
Mortality: [eurostat](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/countries)
