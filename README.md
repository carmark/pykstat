DESCRIPTION:

This module provides a tied hash interface to the Solaris kstats library.
The kstats library allows you to get access to all the stats used by sar,
iostat, vmstat etc, plus a lot of others that aren't accessible through
the usual utilities.

Solaris categorises statistics using a 3-part key - module, instance and
name. For example, the root disk stats can be found under sd.0.sd0, and
the cpu statistics can be found under cpu_stat.0.cpu_stat0, as in the
above example. The method Solaris::Kstats-new()> creates a new 3-layer tree
of perl hashes with exactly the same structure - i.e. the stats for disk 0
can be accessed as $ks-{sd}{0}{sd0}>.

The bottom (4th) layer is a tied hash used to hold the individual statistics
values for a particular system resource.

Creating a Solaris::Kstat object doesn't actually read all the possible statistics in, as this would be horribly slow and inefficient. Instead it creates a 3-layer structure as described above, and only reads in the individual statistics as you reference them. For example, accessing $ks-{sd}{0}{sd0}{reads} will read in all the statistics for sd0, including writes, bytes read/written, service times etc. Once you have accessed a bottom level statitics value, calling $ks->update() will
automatically update all the individual values of any statistics that you have accessed.

Note that there are two values per bottom-level hash that can be read without causing the full set of statistics to be read from the kernel. These are "class" which is the kstat class of the statistics and "crtime" which is the time that the kstat was created. See kstat(3K) for full details of these fields.

Since it's practically impossible to test pykstat on every possible
permutation of kernel , python or distribution version, I need your
help and your feedback to fix the remaining problems.

If you have improvements or bugreports, please send them to:

METHODS:

new()

Create a new kstat statistics hierarchy and return a reference to the top-level hash. Use it like any normal hash to access the statistics.

refresh()

Update all the ststistics that have been accessed so far. Note that as the statistics are stored in a tied hash you can't use references to members of the hash, e.g. my $ref = \$ks-{sd}{0}{sd0}{reads}> followed by print("$$ref\n");, as the reference gets a copy of the value and won't be updated by refresh().

AUTHOR

Lei Xue carmark.dlut@gmail.com

SEE ALSO

kstat(3K), kstat_open(3K), kstat_close(3K), kstat_read(3K), kstat_chain_update(3K).
