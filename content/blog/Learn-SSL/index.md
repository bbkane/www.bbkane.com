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

[nicanorflavier/ssl-certificate-chain-guide](https://github.com/nicanorflavier/ssl-certificate-chain-guide) describes a typical certificate chain setup for most users. "leaf" certs, intermediate certs, and root certs. Unfortunately, sometimes the "chain" is actually a graph... [Path Building vs Path Verifying: The Chain of Pain](https://medium.com/@sleevi_/path-building-vs-path-verifying-the-chain-of-pain-9fbab861d7d6) goes into details about how that works.

## More Specialized Knowledge

[The Illustrated TLS Connection](https://tls12.xargs.org/#client-hello) , [Ulfheim's Certificate Analysis](https://tls13.ulfheim.net/certificate.html), and [TLS, byte by byte](https://bytebybyte.dev/) describe TLS and certificates at a byte-level - what each byte of a connection or certificate means.

[SSL/TLS and PKI History](https://www.feistyduck.com/ssl-tls-and-pki-history/) is a timeline of TLS innovations and attacks. It really helps explain some of the quirks in the protocol. This is so enlightening I might put it in the "General Working Knowledge" section. I highly recommend.

[A Readable Specification of TLS 1.3](https://davidwong.fr/tls13/) is exactly what it says on the tin - explains all details of RFC 8446 in a more readable way. This could be useful to *write* a TLS implementation but is probably too much information for most of your needs.

### Security

[How CT Works : Certificate Transparency](https://certificate.transparency.dev/howctworks/) explains what Certificate Transparency is and why it's needed for publicly trusted Certificate Authorities. [Merkle Town](https://ct.cloudflare.com/) analyzes public CT logs to show which CAs, algorithms, and logs are most popular. [Certificate Transparency: The Gift That Keeps Giving](https://blog.rapid7.com/2018/01/04/certificate-transparency-the-gift-that-keeps-giving/) demonstrates how hackers can incorporate public CT logs into their attacks. [Certificate Search](https://crt.sh/) is a portal to search public Certificate Transparency logs.

[RedHat](https://www.redhat.com/sysadmin/pki-protection) explains some options to protect against SSL's vulnerability to rogue CAs.

[Caveats and pitfalls of cookie domains](https://xebia.com/blog/caveats-and-pitfalls-of-cookie-domains/) is not directly related to TLS, but covers how cookies (potentially login cookies) interact with domains. Check your how your site configures cookies before setting up domains and issuing TLS certificates for them.

[Google Online Security Blog: Sustaining Digital Certificate Security - Entrust Certificate Distrust](https://security.googleblog.com/2024/06/sustaining-digital-certificate-security.html) is a precedent-setting post - Google Chrome will not trust the Entrust Certificate Authority after October 2024. It's a fantastic post that really demonstrates the technical-social facets of TLS. Also see [HackerNews comments](https://news.ycombinator.com/item?id=40812833) and  [Entrust's response](https://www.entrust.com/blog/2024/07/thoughts-on-the-google-chrome-announcement-and-our-commitment-to-the-public-tls-certificate-business/).

## Tools to work with SSL

[Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/general/basic-concepts) - Azure's solution for storing TLS certificates. It's nice, but has some rough edges I should probably blog about in more detail.

[certigo](https://github.com/square/certigo) shows information about a certificate, from a file or by connecting to a server. Like my `easyssl.py` script below but not a total hack :)

[smallstep/cli](https://github.com/smallstep/cli) is a toolkit for working PKI - it actually works with several crytographical technologies, such as JWTS, OAuth, and SSH certificates. See [here](https://smallstep.com/blog/build-a-tiny-ca-with-raspberry-pi-yubikey/) to set up a CA on a Raspberry Pi and a YubiKey with smallstep's tools.

### Certificate Authorities

[LetsEncrypt](https://letsencrypt.org/) is a nonprofit and opensource Certificate Authority that provides FREE SSL certificates.

[CFSSL](https://github.com/cloudflare/cfssl) is [CloudFlare's tool](https://blog.cloudflare.com/introducing-cfssl/) for their internal PKI infrastructure - bundling certs and acting as a certificate authority.

[smallstep/certificates](https://github.com/smallstep/certificates) is a private certificate authority.

### Local Certificate Authorities

Useful for developing with HTTPS locally.

- [mkcert](https://github.com/FiloSottile/mkcert)
- [Minica](https://github.com/jsha/minica)
- [OpenSSL](https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/)

### OpenSSL

[The Most Common OpenSSL Commands](https://www.sslshopper.com/article-most-common-openssl-commands.html) also contains useful OpenSSL commands.

[Using the OpenSSL toolkit with Bash](https://www.linux-magazine.com/Online/Features/OpenSSL-with-Bash) contains useful OpensSSL commands.

LetsEncrypt also has an OpenSSL oneliner to create a self-signed cert that also includes SANs at [their docs](https://letsencrypt.org/docs/certificates-for-localhost/#making-and-trusting-your-own-certificates)

[easyssl.py](https://github.com/bbkane/dotfiles/blob/master/bin_common/bin_common/easyssl.py) is a small script I wrote to generate longer OpensSSL (actually LibreSSL cause I'm on MacOS) commands I need most. For example, getting the list of SANs. It prints out the generated command before running it for easy sharing.

[Creating an OpenSSL CSR](https://www.bbkane.com/blog/creating-an-openssl-csr/) is a blog post I just wrote explaining how to create a CSR to request a certicate from a Certificate Authority. This method has been tested with DigiCert.

### Miscellaneous

[Google Chrome's docs on Certificate Transparency](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/net/docs/certificate-transparency.md)

## Libraries to work with SSL

Citing note: I'm copying most of these descriptions from the preceding links :)

- Multi-language: [certifi](https://github.com/certifi) - A carefully curated collection of Root Certificates for validating the trustworthiness of SSL certificates while verifying the identity of TLS hosts. [google/tink](https://github.com/google/tink) appears to offer crypto primittives, but I haven't tried it.
- Python: [cryptography](https://cryptography.io/en/latest/) - `cryptography` includes both high level recipes and low level interfaces to common cryptographic algorithms such as symmetric ciphers, message digests, and key derivation functions.
- Go: [crypto/tls](https://golang.org/pkg/crypto/tls/) - Go's standard library actually has some really good functionality for TLS
- Java: [bouncycastle](https://www.bouncycastle.org/) - I haven't personally used this one, but a colleague found it and it seems to work for them.
- Rust: [ctz/rustls](https://github.com/ctz/rustls) - One of these days I'll learn Rust, and when I do, I'll use `rustls` for the TLS.
