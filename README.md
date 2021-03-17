# URL Shortner for my infrastructure

Twitter links my apps want to post are too long minaly due to embeded url's. I wanted to make a url shortner.

## Features

 - private API to create short URL's.
 - secured via tenants and roles to fit into my saas structure
 - public API with the redirects.
 - url numbering system using allowed html chars to be as short as possible ( a-z, A-Z, 0-9, _.-~ = 26 + 26 + 10 + 4 = 66 chars)
 - Query service to find the short url (may be in singleton or another container)
 - State stored in object_store
 - Bad word removed - in case generated url's have bad words
 - not easiably guessable. You can not take one url and add one to get the next
 - constant length
 - short url's are expired after 365 days??
 - reads my jwt to get userid and allows only that user to delete/edit shorturls



## Parameter

pad = random number between 0..550731775.