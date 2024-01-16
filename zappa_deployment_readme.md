
# Steps to Upload code on Zappa
1. buy domain on namecheap.com/use existing
2. register new site on cloudflare.com/use existing
3. cloudflare will give you (most probably) two nameservers
4. enter under https://ap.www.namecheap.com/domains/domaincontrolpanel/xkcd-excuse.com/domain DNS - choose "Custom DNS" nameservers given on cloudflare
5. go to AWS ACM and request a new certificate (certificate must be created in us-east-1 region)
6. enter if necessary multiple subdomains (foo.example.com & foo-dev.example.com)
7. make note of ACM ARN given from AWS management console
8. in zappa_settings.json enter under certificate_arn your ARN
9. in zappa_settings.json under route53_enabled put false - this is a must
10. in zappa_settings.json under domain enter domain for each stage ie. foo.example.com and foo-dev.example.com
11. run zappa certify <stage_name>
12. it should say: "Created a new domain name with supplied certificate. Please note that it can take up to 40 minutes for this domain to be created and propagated through AWS, but it requires no further work on your part. Certificate updated!"
go to CloudFlare DNS interface and enter
13. CNAME: foo - i3jtsjkdeu4wxo.cloudfront.net
14. CNAME: foo-dev - d2jtsjkdeu4wxo.cloudfront.net
15. wait for 40 minutes and check your domain(s), they should serve your Lambda function
