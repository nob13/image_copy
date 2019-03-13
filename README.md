# image_copy

License: public domain 

Hacky photo copy script (python).

The script copies data from a source directory into a target photo library directory, extracts EXIF information and
stores them into the format "year/month", e.g. "2018/09".

It caches files it already copied, so that it's faster the next time. It also checks if a file is existant and skips it, if it is.

I use it on my linux machine to automate import, as all UI Tools faild to provide the same functionality.
