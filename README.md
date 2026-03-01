# Server Project Documentation

## 1. Project Overview

### Purpose
The server project is a Flask service that generates random alphanumeric data (length 1024), computes a SHA-256 checksum, stores the generated data, and exposes it to clients via HTTP.

### Technologies Used
- Python 3.11
- Flask
- Docker + Docker Compose
- Terraform (AWS EC2/VPC provisioning)
- GitHub Actions (CI/CD)
- Prometheus scrape config

### High-Level Architecture
1. User (or client app) requests `/data`.
2. Server generates random payload and checksum.
3. Server stores payload in `/serverdata/data.txt`.
4. Server returns JSON:
   - `data`
   - `checksum`
5. Client app can verify checksum on receipt.

---

## 2. Project Structure

```text
server-repo/
├── app/
│   └── server.py
├── terraform/
│   ├── main.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── setup_docker_server.sh
│   ├── setup_docker_client.sh
│   ├── terraform.tfstate
│   ├── terraform.tfstate.backup
│   ├── terra-key-ec2-server
│   ├── terra-key-ec2-server.pub
│   └── .terraform/...
├── .github/
│   └── workflows/
│       └── main.yml
├── Dockerfile
├── docker-compose.yml
├── prometheus.yaml
├── requirements.txt
├── terraform.tfstate
└── .gitignore
```

### Key Directories and Files
- `app/server.py`
  - Main Flask service.
  - Endpoints:
    - `GET /` -> HTML UI for manual generation.
    - `GET /data` -> generates payload/checksum and returns JSON.
- `Dockerfile`
  - Python slim image, installs Flask, exposes `5000`.
- `docker-compose.yml`
  - Runs server container with named volume `servervol:/serverdata`.
- `prometheus.yaml`
  - Targets `node_exporter` and `cadvisor` on localhost.
- `terraform/*.tf`
  - Provisions AWS VPC/subnet/IGW/route table/SG.
  - Creates two EC2 instances (`server`, `client`) and key pair.
  - Uses user-data scripts to install Docker and run containers.
- `terraform/setup_docker_server.sh`
  - Pulls and runs server Docker image on instance startup.
- `terraform/setup_docker_client.sh`
  - Pulls/runs client image with `SERVER_URL` referencing server private IP.
- `.github/workflows/main.yml`
  - CI/CD for server image build/push and EC2 deployment via SSH.
- `terraform.tfstate` and `terraform/terraform.tfstate*`
  - Terraform state artifacts (include deployed infra metadata and outputs).
- `terraform/terra-key-ec2-server` (private key)
  - Private SSH key file present in repo tree (high-risk secret exposure).

---

## 3. Installation & Setup

### Required Software
- Python `3.11+`
- pip
- Docker + Docker Compose
- Terraform (if provisioning infra)
- AWS credentials configured (for Terraform usage)

### Local Run (without Docker)
1. Setup environment:
   ```bash
   cd server-repo
   python3 -m venv .venv
   source .venv/bin/activate
   pip install flask
   ```
2. Start server:
   ```bash
   python app/server.py
   ```
3. Open:
   - UI: `http://localhost:5000`
   - API: `http://localhost:5000/data`

### Docker Run
```bash
cd server-repo
docker build -t dice-server .
docker run --rm -p 5000:5000 -v servervol:/serverdata dice-server
```

### Docker Compose Run
```bash
cd server-repo
docker compose up --build
```

---

## 4. Configuration

### Runtime Paths
- Data directory: `/serverdata`
- Saved payload file: `/serverdata/data.txt`

### Environment Variables
- No required runtime env var in current `server.py`.

### Terraform Variables (`terraform/variables.tf`)
- `ec2_instance_type` default `t3.micro`
- `aws_root_storage_size` default `8`
- `ec2_ami_id` default `ami-0b6c6ebed2801a5cb`

### Terraform Outputs (`terraform/outputs.tf`)
- `server_public_ip`
- `client_public_ip`

---

## 5. Usage

### Start the Project
- Local: `python app/server.py`
- Docker: `docker run ...`
- Compose: `docker compose up`

### Test Endpoints
- Health/manual UI check:
  ```bash
  curl -i http://localhost:5000/
  ```
- Data endpoint:
  ```bash
  curl http://localhost:5000/data
  ```

### API Endpoints
- `GET /`
  - Serves HTML page with **Generate Data** button.
- `GET /data`
  - Returns JSON:
  ```json
  {
    "data": "<1024-char random string>",
    "checksum": "<sha256 hex>"
  }
  ```

### UI Components
Inline HTML in `server.py` includes:
- Title and instructions
- `Generate Data` button
- Output panel displaying `data` and `checksum`

---

## 6. Docker / Deployment

### Dockerfile Notes
- Base: `python:3.11-slim`
- Installs Flask only
- Runs on port `5000`

### Compose Notes
- Container name: `dice_server`
- Volume: `servervol` -> `/serverdata`

### CI/CD Workflow
- Trigger: push to `main`
- Builds and pushes `dice_project_server_app:latest`
- SSH deploy to EC2, replacing running container

### Terraform Deployment Model
- AWS region in `provider.tf`: `us-east-1`
- Infra includes:
  - VPC + public subnet
  - Internet gateway + route table
  - SG allowing ports `22`, `80`, `5000` from `0.0.0.0/0`
  - EC2 instances for server and client
  - key pair from `terra-key-ec2-server.pub`
- Startup scripts install Docker and run published images.

---

## 7. Dependencies

### Python Libraries
- `flask`: HTTP routing, JSON responses, and HTML rendering

### Python Standard Library
- `hashlib`: checksum generation
- `random`, `string`: random data generation
- `os`: filesystem directory setup

### DevOps/Infra Dependencies
- Docker / Compose: container runtime
- Terraform AWS provider (`hashicorp/aws` `6.34.0` lock)
- GitHub Actions + Docker Hub + SSH deployment

---

## 8. Additional Notes

### Important Commands
- Start local server:
  ```bash
  python app/server.py
  ```
- Verify API quickly:
  ```bash
  curl http://localhost:5000/data | jq
  ```

### Common Pitfalls / Troubleshooting
- Port `5000` conflict if client and server run on same host without remapping one side.
- `requirements.txt` is empty; local Python install must be manual (`pip install flask`).
- Terraform user-data for client references server private IP interpolation; ensure networking/SG rules permit client-to-server access.

### Security/Operational Risks Found
- A private SSH key file exists in repo: `terraform/terra-key-ec2-server`.
- Terraform state files are committed and include environment metadata, public IP outputs, and resource details.
- Security groups allow broad inbound access (`0.0.0.0/0`); tighten before production.

Recommended immediate remediation:
1. Rotate exposed key material and remove private key from version control.
2. Move Terraform state to a secured remote backend.
3. Restrict security group ingress to required IP ranges.
