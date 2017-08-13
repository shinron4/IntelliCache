# IntelliCache

# Problem Defintion

Content centric network employs the concept of in-network management of content storage and distribution, where intermediate routers or base stations apply content storage and distribution policies based on the underlying content usage patterns. CCN uses content popularity as basic criteria for deciding content storage, and distribution policies. There is a direct correlation between content popularity and Social dynamics among users of that content.

IntelliCache is a cache implementation, which runs on a proxy server. Based upon the user access pattern it develops a directed graph G which represents the social dynamics between users. Now IntelliCache uses this graph G to infer the content popularity and then uses this content popularity measure to take caching decision.

