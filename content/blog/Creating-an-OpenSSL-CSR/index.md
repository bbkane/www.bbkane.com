+++
title = "Creating an OpenSSL CSR"
date = 2021-06-12
+++

If you want to make a TLS certicate, you need a Certificate Signing Request (CSR). Let's make one! I've verified that this produces a CSR suitable for pasting into DigiCert to get a certificate.

Making one isn't too bad if you use a config file. The following posts were super helpful when I was googling this:

- [Know about SAN Certificate and How to Create With OpenSSL ](https://geekflare.com/san-ssl-certificate/)
- [Steps to generate CSR for SAN certificate with openssl](https://www.golinuxcloud.com/openssl-subject-alternative-name/)

# Make the CSR config

First, make the config file ( I'm callling this `www.audiobubbly.com.cfg`). We'll use this config file to create a CSR and a Private Key.

```config
[ req ]
default_bits               = 2048
distinguished_name         = req_distinguished_name
req_extensions             = req_ext
prompt                     = no
[ req_distinguished_name ]
countryName                = US  # Country Name (2 letter code)
stateOrProvinceName        = California  # State or Province Name (full name)
localityName               = Sunnyvale  # Locality Name (eg, city)
organizationName           = bbkane.com  # Organization Name (eg, company)
commonName                 = www.audiobubbly.com  # Common Name (e.g. server FQDN or YOUR name)
[ req_ext ]
subjectAltName             = @alt_names
[alt_names]
DNS.1                      = audiobubbly.com
DNS.2                      = www.audiobubbly.com
IP.1                       = 10.0.0.1
```

A couple of things to notice here:

- `prompt = no` - if we don't add this, OpenSSL won't read our config file, even though we passed it. See [this issue](https://github.com/openssl/openssl/issues/3536).
- `[ req_distinguished_name ]` - if you work in an organization, and you want to make a cert "like the existing one", you can use openssl to check what's on it. I work for LinkedIn, so if I was making a LinkedIn cert, I would check the main website domain.

```bash
echo | openssl s_client -connect www.linkedin.com:443 -servername www.linkedin.com 2> /dev/null | openssl x509 -noout -subject
```

```
subject= /C=US/ST=California/L=Sunnyvale/O=LinkedIn Corporation/CN=www.linkedin.com
```

- The `Common Name` is repeated in the `subjectAltName`. Browsers don't check the `Common Name` field any more, just the `subjectAltName`. So we need to repeat it. These days, the `Common Name` is more of an identifier for humans to read than something that matters to computers.
- We're adding an IP to the `subjectAltName` section. That's just for demonstration. For production traffic, you probably prefer to use DNS instead of IPs directly.

# Create CSR and Private Key

```bash
openssl req \
    -out www.audiobubbly.com.csr \
    -newkey rsa:2048 \
    -nodes \
    -keyout www.audiobubbly.com.PRIVATE.key \
    -config ./www.audiobubbly.com.cfg
```

```
................+++
........................+++
writing new private key to 'www.audiobubbly.com.PRIVATE.key'
-----
```

Some notes here:

- `rsa:2048` is an older and slower algorithm. I'm using it because I'm used to it, but you should consider newer and better ones.
- `-nodes` means "no DES" - we won't be creating a password for our private key. See [this link](https://stackoverflow.com/a/5087138/2958070) for more info and alternative encryption algorithms.
- Examine the request you just created with the following command

```bash
openssl req -noout -text -in ./www.audiobubbly.com.csr
```

- Everyone knows this, but it's worth repeating anyway - don't share your private key with anyone you don't trust with control of your website.

# Request and deploy certificate

To test that this method and has all the information needed to create a DigiCert capable of serving live traffic, I:

- Used my DigiCert account to create a certificate valid for 2 days for www.audiobubbly.com
- Used GitHub to make an incredibly barebones [site repo](https://github.com/bbkane/www.audiobubbly.com)
- Created a corresponding www.audiobubbly.com site in Netlify
- Added the SSL certificates via the Domains Management menu. You need to paste in the Certificate, Private Key, and Intermediate Certs in the dialogue. The easiest way to get those is to click "More Options" on the DigiCert download portal and copy:
  -  the certificate text into the Certificate section of Netlify's dialogue,
  - both the Intermediate Certificate and the Root Certificate from the DigiCert popup to the Netlify dialogue,
  - and the Private Key we generated  (i.e., not in the DigiCert portal) into the Private key section of the Netlify dialogue
- Headed to [https://www.audiobubbly.com](https://www.audiobubbly.com) to load the site.

On a whim I **REVOKED** the certificate and headed to [SSL Labs](https://www.ssllabs.com/ssltest/) to see what happened. Yup. Things looked pretty secure, except my certificate got an "F" for being revoked. Interestingly, my browser still trusts the cert. I thought it might be a cache issue from before I revoked the cert, so I tried to load the site on my phone browser and it also worked just fine...

# Verify private key and certificate

If you're doing this a lot it's also useful to check that you've got the right set of certificates + the right private key:


Verify private key (source [here](https://www.ssl247.com/knowledge-base/detail/how-do-i-verify-that-a-private-key-matches-a-certificate-openssl-1527076112539/ka03l0000015hscaay/)):


```bash
openssl rsa -check -noout -in private-key.pem
```

Verify private key signs cert:

```bash
openssl rsa -modulus -noout -in private-key.pem | openssl md5
openssl x509 -modulus -noout -in leaf-cert.pem | openssl md5
```

Verify certificate chain (source [here](https://stackoverflow.com/a/26520714/2958070)):

```bash
openssl verify -CAfile ca-cert.pem -untrusted intermediate-cert.pem leaf-cert.pem
```

Verify dates (source [here](https://stackoverflow.com/questions/21297853/how-to-determine-ssl-cert-expiration-date-from-a-pem-encoded-certificate/21297927#21297927)):

```bash
openssl x509 -dates -noout -in leaf-cert.pem
```
