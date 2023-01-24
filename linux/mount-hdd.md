Through the ubuntu desktop, you can see the mounted hdd but when you ssh then you cannot.

I followed the instruction from https://askubuntu.com/questions/164926/how-to-make-partitions-mount-at-startup which essentially says to go via `gnome-disks` and not using the defaults.

The other way is to edit `/etc/fstab` which seems to be a list of mounted drives which is also documented in the above link.