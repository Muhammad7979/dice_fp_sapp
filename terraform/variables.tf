

variable "ec2_instance_type" {
  default = "t3.micro"
  type    = string
}

variable "aws_root_storage_size" {
  default = 8
  type    = number
}

variable "ec2_ami_id" {
  default = "ami-0b6c6ebed2801a5cb"
  type    = string
}