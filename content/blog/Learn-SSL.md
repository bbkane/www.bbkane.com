+++
title = "Learn SSL"
date = 2021-06-08
+++

SSL is one of those weird niche subjects that no one learns until they run into a problem. It's confusing because there's a lot of moving parts, file formats, and terminology. For example, SSL (Secure Socket Layer) is also called TLS (Transport Layer Security). In this blog post the I'll probably switch between the acronyms unconsciously as I write. In addition, a lot of the tools used to work with SSL suck. I've been debugging basic SSL issues for a while at work now, and I've learned quite a bit about it (definitely not close to everything). 

So here's a link dump. I would recommend reading the "General Working Knowledge" links and skimming the others for something that looks interesting.

## General Working Knowledge

Note that some of these articles cover the same material.

Start with [Dissecting an SSL certificate](https://jvns.ca/blog/2017/01/31/whats-tls/) for a quick (like two page) summary about how how certificates work.

Next, dive in with [Everything you should know about certificates and PKI but are too afraid to ask](https://smallstep.com/blog/everything-pki/). 

[Transport Layer Security (TLS)](https://hpbn.co/transport-layer-security-tls/) is part of O'Reilly's [High Performance Browser Networking](https://hpbn.co/) free online book and contains a really great list of topics about SSL, including Server Name Indication (SNI) and Optimizing for TLS

[Automated Certificate Management Environment (ACME) Explained](https://sectigo.com/resource-library/what-is-acme-protocol) explains how to prove you own a domain to most (all?) public Certificate Authorities so they will issue you a certificate.

## More Specialized Knowledge

[The Illustrated TLS Connection](https://tls.ulfheim.net/) is a super interesting breakdown of the byte-level communications between a client and a server. I haven't needed to use WireShark for analyzing TLS connections, but if I do, I'm headed here first.

[Ulfheim's Certificate Analysis](https://tls13.ulfheim.net/certificate.html) is a companion site that breaks down a certificate at the byte level.

[SSL/TLS and PKI History](https://www.feistyduck.com/ssl-tls-and-pki-history/) is a timeline of TLS innovations and attacks. It really helps explain some of the quirks in the protocol. This is so enlightening I might put it in the "General Working Knowledge" section. I highly recommend.

[A Readable Specification of TLS 1.3](https://davidwong.fr/tls13/) is exactly what it says on the tin - explains all details of RFC 8446 in a more readable way. This could be useful to *write* a TLS implementation but is probably too much information for most of your needs.

### Security

[RedHat](https://www.redhat.com/sysadmin/pki-protection) explains some options to protect against SSL's vulnerability to rogue CAs.

[Certificate Search](https://crt.sh/) is a portal to search public Certificate Transparency logs.

[Certificate Transparency: The Gift That Keeps Giving](https://blog.rapid7.com/2018/01/04/certificate-transparency-the-gift-that-keeps-giving/) demonstrates how hackers can incorporate public Certificate Transparency logs into their attacks.

[Caveats and pitfalls of cookie domains](https://xebia.com/blog/caveats-and-pitfalls-of-cookie-domains/) is not directly related to TLS, but covers how cookies (potentially login cookies) interact with domains. Check your how your site configures cookies before setting up domains and issuing TLS certificates for them.

## Tools to work with SSL

[Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/general/basic-concepts) - Azure's solution for storing TLS certificates. It's nice, but has some rough edges I should probably blog about in more detail.

### Certificate Authorities

[LetsEncrypt](https://letsencrypt.org/) is a nonprofit and opensource Certificate Authority that provides FREE SSL certificates.

[CFSSL](https://github.com/cloudflare/cfssl) is [CloudFlare's tool](https://blog.cloudflare.com/introducing-cfssl/) for their internal PKI infrastructure - bundling certs and acting as a certificate authority.

[smallstep/certificates](https://github.com/smallstep/certificates) is a private certificate authority.

[smallstep/cli](https://github.com/smallstep/cli) is a toolkit for working PKI - it actually works with several crytographical technologies, such as JWTS, OAuth, and SSH certificates. See [here](https://smallstep.com/blog/build-a-tiny-ca-with-raspberry-pi-yubikey/) to set up a CA on a Raspberry Pi and a YubiKey with smallstep's tools.

### Local Certificate Authorities

Useful for developing with HTTPS locally.

- [mkcert](https://github.com/FiloSottile/mkcert)
- [Minica](https://github.com/jsha/minica)
- [OpenSSL](https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/)

### OpenSSL

[The Most Common OpenSSL Commands](https://www.sslshopper.com/article-most-common-openssl-commands.html) also contains useful OpenSSL commands.

[Using the OpenSSL toolkit with Bash](https://www.linux-magazine.com/Online/Features/OpenSSL-with-Bash) contains useful OpensSSL commands.

LetsEncrypt also has an OpenSSL oneliner to create a self-signed cert that also includes SANs at [their docs](https://letsencrypt.org/docs/certificates-for-localhost/#making-and-trusting-your-own-certificates)

[easyssl.py](https://github.com/bbkane/dotfiles/blob/master/bin_common/bin_common/easyssl.py) is a small script I wrote to generate longer OpensSSL (actually LibreSSL cause I'm on MacOS) commands I need most. For example, getting the list of SANs.

### Miscellaneous

[Google Chrome's docs on Certificate Transparency](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/net/docs/certificate-transparency.md)
