# Trade

Trade is, in the designer's opinion, the most unique quality of the game. 

Trade manifests itself as the movement of resources between cities. Commerce facilitates this movement, as well as also being moved around in trade.

In the game, trade is very conservative, meaning that the default behaviour of cities is rather not to trade than to trade when it would be a risky situation. A combination of technological advancement and controls by the player can modify this behaviour to be ultimately more favourable.

## How trade works

Trade occurs in four phases:
- Selection Phase: each city determines the "favouribility" of each other city, being a measure of how much the city wants to trade with the other.
- Demand Phase: each city finds, for each resource, how much each other city would want to import ideally to make them have equal amounts.
- Offer Phase: each city places an offer for exports to each other city based on a combination of the favouribility and the demand from the previous phases.
- Import Phase: each city imports goods based on the offers it has been provided, but only as much as its available stock of commerce would allow for. 

#### Selection Phase

Each city determines how much it likes a particular destination to export to. The city does so by calculating a favouribility score, that:
 - increases with the available Commerce of the destination;
 - increases with the shared culture* between the two cities;
 - decreases with the "trade distance" between the cities;
 - decreases with unfavourable trade policies between the origin and destination civilisations (note that they can be the same civilisation). 

The total favouribility scores are then added up for the city, and the relative favourability score to a destination is calculated as the fraction of the total favourability score of that destination. 

#### Demand Phase

The demand, or gradient, of exports from an origin to the destination for a particular resource is calculated as the amount more of that resource per citizen the origin has than the destination. 

For example, if the origin city has 10 horses and the destination has 2, and the two cities have the same population, then there is a demand for the origin city to export horses to the destination. If, however, the origin city has 5 citizens and the destination city has 1 citizen, then both cities have 2 horses per citizen, meaning there is no demand for the export. 

The demand is calculated as the origin's resources per citizen minus the destination's resources per citizen. 

Demand cannot be below zero. If the destination would have more of the resource per citizen than the origin, the demand is simply set to zero. 

#### Offer Phase

Each city then decides on an offer to give as an export to each other city.

The offer is determined by:
 - the relative favourability of the destination for trading,
 - times the demand times the population of the destination (giving the amount of resource needed to transfer to equalise the resource per population of each city),
 - divided by the "trade distance" between the cities, or 2, whichever is greater. 

The offer is then also rounded down to the next integer; another case of trade being conservative.

In practice in a world of many competing cities each with their own desires, the offer is almost always smaller than the ideal amount needed to move around to make the share of the good equal among all cities. 

#### Import Phase

Once all offers have been set, each city wants to import as much of what is offered to them as possible. However, trade also has a cost.

It costs the importer 2 Commerce to import a single unit of a resource. Of that 2 Commerce, one goes to the exporter, and the other is lost, representing the cost of physically moving the good. 

The importing city counts up how many total resources they could import, given unlimited Commerce. Then, the city determines what fraction of those resources it can purchase (for 2 Commerce each), and buys that fraction (rounded down) of each offer it has been given. 

This is yet another way in which trade is conservative. 

## Trade Distance

Mentioned previously in this entry, "trade distance" is a term for the best route for a trade route to take. Trade distance is accounted for twice: in the selection phase, cities are preferable that have a smaller trade distance, and in the offer phase, the size of the offer is reduced by the trade distance.

Trade distance is, in brief, the length of the shortest path between two cities. This is affected by the state of the world:
 - Physical terrain: rougher and more hostile terrain is more difficult for traders to pass through. 
 - Infrastructre: roads, railroads, highways, etc. reduce the length of a path that uses them.
 - Harbour access: trade distance is almost always less over water - it is in effect a natural road - but only if there is direct access to a harbour for both the origin and the destination. 
 - Raiders and plunderers: pirates, bandits, or even armies of civilisations can blockade trade routes and prevent movement of goods through making possible pathways no longer safe to travel. 

Trade distance also changes with technology and access to resources. As energy capabilities evolve beyond muscle and wind, the difficulty of travelling far distances is reduced. 

### Details of Trade Distance

In general, trade distance is convex with distance. That is a fancy way of saying that as the length of the shortest path between two cities increases, the trade distance increases by even more. This has two major consequences:
 - If City A is twice as far away from City C as City B is, then the trade distance between City A and City C is strictly more than twice as much as the trade distance between City B and City C. 
 - If City A and City B are equidistant from City C, but further away from each other, the sum of the trade distances City A to City C and City C to City B is strictly less than the trade distance between City A and City B. 

In particular, this means that having more densely built cities will make for less overall trade distances (though not necessarily more efficient trade). Certain cities might act like trade hubs because of being close to a lot of individual cities that are not so close to each other. 

## Other effects of trade

Trade also has three more effects apart from its core mechanic:
- Spread of technology: when two civilisations trade, they share some science between each other depending on which technologies one has that the other does not. For more details, see technology*. 
- Spread of culture: when two cities trade, cultural influence is exchanged between them. Both the importer and exporter experience an amount of cultural influence based on the scale of the trade and the cultural strengths of their respective cities. 
- Spread of information: trade can also cause information about a civilisation's military to spread. 

## Other things affecting trade

### Technology

Different financial and logistic technologies can completely change how trade works. 

- Currency allows for Commerce to be stored and backed by tangible items, meaning that it can be stored, it can be taxed, and it can be transferred to cities. This allows players to "invest" in cities by giving them an influx of Commerce, or for cities to save up their Commerce to attract goods. 
- Banking allows for loans to be taken out, and cities can then go into debt. In practice, this means that the Import Phase consists only of the importing city buying all it is offered, and possibly ending up with a negative amount of Commerce that needs to regenerate. 
- New forms of energy beyond wind and muscle mean that trade distance becomes less and less strongly convex. In practice, this means that in-between cities are less and less relevant with technologies such as Steam Power, Internal Combustion, and Flight. 
- New forms of communication, starting from the Telegraph, through Radio, Television, The Internet, Social Media mean that ideas, if not tangible goods, can flow freely with minimal impact by distance. 

### Cultural Institutions

Shared cultural institutions, including language, writing systems, and others, influence how trade is selected and how much will actually happen. See more in Cultural Institutions*. 

### Diplomacy

Players may not be happy about trade moving freely through their countries, whether fearing cultural influence, losing a technological edge, or having all of their resources bought up by a more commercially powerful rival. 

Diplomatic actions can control whether or not trade networks are open, or tariffs, bringing in revenue while mainly disincentivising foreign trade. These actions can apply to all resources, or a handful of select ones.  
