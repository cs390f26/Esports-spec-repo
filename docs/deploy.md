# Deploying to EC2

This guide launches an EC2 instance that runs `[scripts/userdata.sh](../scripts/userdata.sh)` on first boot, attaches an Elastic IP so the site keeps the same public address, and registers that address as a `moraviancs.click` subdomain through [Moravian CS DNS](https://awsdns.moraviancs.click/).

## Prerequisites

- An AWS account with permission to create EC2 instances, security groups, key pairs, and Elastic IPs.
- The latest `scripts/userdata.sh` and `deploy/requirements.txt` pushed to the `main` branch on GitHub. The instance clones from GitHub, not from your laptop.

## 1. Launch the instance

In the AWS console, go to **EC2 → Instances → Launch instances**.

1. **Name:** for example, `esports-reservation`.
2. **Application and OS image:** Amazon Linux 2023.
3. **Instance type:** `t2.micro` or `t3.micro` (free tier eligible).
4. **Key pair:** create or choose a key pair and keep the `.pem` file. You need it to SSH in.
5. **Network settings → Edit:**
  - **Auto-assign public IP:** Enable.
  - **Firewall (security groups):** Create a security group with these inbound rules:

    | Type | Port | Source    | Why                     |
    | ---- | ---- | --------- | ----------------------- |
    | SSH  | 22   | My IP     | Connect to the instance |
    | HTTP | 80   | 0.0.0.0/0 | Open the site           |

6. **Advanced details → User data:** paste the full contents of `scripts/userdata.sh`, starting with `#!/bin/bash`. Leave **User data has already been base64 encoded** unchecked.
7. Select **Launch instance**.

User data runs once, as root, on the instance's first boot. Setup usually takes 2–5 minutes after the instance reaches **Running**.

## 2. Allocate and associate an Elastic IP

The public IP an instance gets at launch changes whenever the instance is stopped and started. An Elastic IP stays the same.

1. Go to **EC2 → Network & Security → Elastic IPs → Allocate Elastic IP address**.
2. Keep **Amazon's pool of IPv4 addresses** and select **Allocate**.
3. Select the new address, then **Actions → Associate Elastic IP address**.
4. **Resource type:** Instance. Choose the instance from step 1.
5. Select **Associate**.

The instance's **Public IPv4 address** now shows the Elastic IP. The original auto-assigned address is released, so use the Elastic IP from now on.

## 3. Register a domain name

[Moravian CS DNS](https://awsdns.moraviancs.click/) points a subdomain of `moraviancs.click` at an IP address, so the site can be reached by name instead of by number.

1. Open [https://awsdns.moraviancs.click/](https://awsdns.moraviancs.click/).
2. Select **Sign in with Google** and use your `@moravian.edu` account.
3. Enter the Elastic IP from step 2 and save it. The site gives you a subdomain such as `yourname.moraviancs.click`.

Register the Elastic IP, not the auto-assigned address from launch. The Elastic IP stays the same, so the domain keeps working after the instance is stopped and started. A new DNS record can take a few minutes to start resolving.

## 4. Check the site

Open the domain in a browser over HTTP:

```text
http://<your-subdomain>.moraviancs.click/
```

The overview page should load. Use `http://`, not `https://`; the script does not set up a certificate.

## 5. (Optional) Connect over SSH

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<elastic-ip>
```

Once connected, these commands confirm each part of the setup:

```bash
# Output from the user data script
sudo tail -n 50 /var/log/cloud-init-output.log

# nginx is running
systemctl status nginx
```



## Troubleshooting


| Symptom                                           | Likely cause                                          | Fix                                                                                                     |
| ------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| The browser times out                             | Port 80 is not open, or you used `https://`           | Add an HTTP rule for port 80 to the security group; open the `http://` address                          |
| The domain does not load, but the Elastic IP does | The DNS record is new, or it points at a different IP | Wait a few minutes; check that [Moravian CS DNS](https://awsdns.moraviancs.click/) shows the Elastic IP |
| The nginx welcome page appears                    | The script is still running or failed partway through | Wait a few minutes, then check `/var/log/cloud-init-output.log`                                         |
| `git clone` fails in the log                      | The repository is private                             | Make the repository public                                                                              |
| `pip install` fails in the log                    | `deploy/requirements.txt` was not pushed to GitHub    | Push it, then rerun the script as shown below                                                           |
| SSH says permission denied                        | Wrong username, or the key file is too open           | Use `ubuntu` or `ec2-user`; run `chmod 400` on the key                                                  |




## Updating the deployment

User data does not run again on reboot. To pick up new commits, SSH in and rerun the script. It replaces the clone and the web folder each time, so it is safe to run again.

```bash
sudo bash /var/lib/cloud/instance/scripts/part-001
```

To start fresh instead, terminate the instance, launch a new one with the same user data, and associate the same Elastic IP with it.

## Cleaning up

An Elastic IP is billed while it is allocated, whether or not it is attached to a running instance. When you are done:

1. **Elastic IPs → Actions → Disassociate Elastic IP address**, then **Release Elastic IP addresses**.
2. **Instances → Instance state → Terminate instance**.

