@title Heartbleed Report
@author lbroza
@date 04/13/2014
@tags Security


You may have heard about the Heartbleed bug discovered in OpenSSL by now. We just wanted to touch briefly on Heartbleed
and what you need to know to make sure you're protected with us.

Most sites use the TLS/SSL protocol to encrypt sensitive communication between you and their servers. Many sites use
OpenSSL to **enable** TLS/SSL to keep you safe as you use their services.

Heartbleed is a bug that was accidentally introduced into OpenSSL at the end of 2011. Exploitation of this bug makes it
theoretically possible to bypass OpenSSL's inherent security and obtain sensitive information. Any server using an
affected version of OpenSSL is susceptible to these exploits.

The Heartbleed bug did not directly affect our servers. However, if you use your Ografy password elsewhere on the
internet it may have been compromised.

To be safe, we'd recommend updating your Ografy password. Ideally you should choose a password that you don't use
anywhere else. Keeping track of many passwords can be annoying, but it's one of the best ways to keep your information
safe. There are a few great password managers out there that make this task substantially easier.

If you're interested in learning more about Heartbleed you can check out the official site at
<a href="http://heartbleed.com" target="_blank">http://heartbleed.com</a>.
