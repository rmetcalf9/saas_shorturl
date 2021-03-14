# URL Shortner for my infrastructure

Twitter links my apps want to post are too long minaly due to embeded url's. I wanted to make a url shortner.

## Features

 - A singleton listens to a queue and reserves short url's based on requests.
 - url numbering system using allowed html chars to be as short as possible
 - Query service to find the short url (may be in singleton or another container)
 - State stored in object_store
 - Bad word removed - in case generated url's have bad words
