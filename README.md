Distributed Denial of Service using the Slowloris attack
=======================================================

Initially written in perl, this program is a python rendition of the same code. It carries out a denial of service attack on the specified server. You can specify the following parameters:

1. The IP address of the target (default is 192,168.1.4)

2. The port number (default is 80)

3. The encoding format of the header (default is UTF-8)

I tested this program on a linux machine that runs Apache 2.2.22, and it works fine. This program should only be used in a control environment. I don't condone the use of this program to attack actual websites. I am not to be held responsible if someone uses this code for malicious purposes.
