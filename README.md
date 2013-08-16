All the bloom filter implementations that I could find relied on C code that didn't have a compilation script (or binaries) for windows.

This is a simple, all-python implementation of a bloom filter.

Dependancies:
* scikit-learn, for an approprite hash function; murmurhash. Feel free to incorporate other hash function options (or add a try-except chain of imports with other hash functions for users that don't have scikit-learn)
* bitarray, for basic boolean handling
* matplotlib, not essential, just used for plotting hash function output in the module-tests (to demonstrate unifority)
	
Making a filter is simple:

    BloomFilter(iterable=(), max_entries=None, false_positive_rate=0.01)

If you just want to quickly make a bloom filter from an iterable, you can just make that iterable the only argument. Beware though that adding any more entries after will cause the error rate to go above its set value; to avoid this specify a the maximum number of entires that this bloom filter will have using max_entries.

To add to an existing filter just use myfilter.append(obj)

To add the contents of an iterable to an existing filter, use myfilter.update(iterable)

To test for membership use the native, python 'in' keyword:

    obj in myfilter
