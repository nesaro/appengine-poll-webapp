webapp2 poll app
================

Author: Nestor Arocha Rodriguez

Comments
--------
 * Auth: I have used default authentication modules from appengine
 * The authentication parts can be implemented with decorators (like django's @auth_required )
 * Templates: I have experience with django and it uses the same template engine
 * Memcache: I have used memcache for voting page only; I assumed admin and results pages aren't requested very frequently, but if required /results/ would be a good candidate for caching
 * Database performance: The only critical part I could found is vote counting. I decided to do a query with a count for each result because I assumed performance for db query is better than a python for + __eq__ for each result. However, if the number of values per poll is too large, performance can be worse with count method
 

 


