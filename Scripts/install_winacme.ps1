wget https://github.com/win-acme/win-acme/releases/download/v2.1.18/win-acme.v2.1.18.1119.x64.pluggable.zip -OutFile letsencrypt-win-acme.zip
wget https://github.com/win-acme/win-acme/releases/download/v2.1.18/plugin.validation.dns.cloudflare.v2.1.18.1119.zip -OutFile cloudflare-dns-challenge.zip
tar -xvf letsencrypt-win-acme.zip
tar -xvf cloudflare-dns-challenge.zip