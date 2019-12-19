# Setting up security groups
resource "aws_security_group" "allow-ssh" {
    description = "Managed by Terraform"
    egress      = [
        {
            cidr_blocks      = [
                "0.0.0.0/0",
            ]
            description      = ""
            from_port        = 0
            ipv6_cidr_blocks = [
                "::/0",
            ]
            prefix_list_ids  = []
            protocol         = "-1"
            security_groups  = []
            self             = false
            to_port          = 0
        },
    ]
    
    ingress     = [
        {
            cidr_blocks      = [
                "0.0.0.0/0",
            ]
            description      = ""
            from_port        = 80
            ipv6_cidr_blocks = [
                "::/0",
            ]
            prefix_list_ids  = []
            protocol         = "tcp"
            security_groups  = []
            self             = false
            to_port          = 80
        },
        {
            cidr_blocks      = [
                "141.134.85.233/32",
            ]
            description      = "Jochen @ Home"
            from_port        = 22
            ipv6_cidr_blocks = []
            prefix_list_ids  = []
            protocol         = "tcp"
            security_groups  = []
            self             = false
            to_port          = 22
        },
        {
            cidr_blocks      = [
                "194.78.171.126/32",
            ]
            description      = ""
            from_port        = 56733
            ipv6_cidr_blocks = []
            prefix_list_ids  = []
            protocol         = "tcp"
            security_groups  = []
            self             = false
            to_port          = 56733
        },
        {
            cidr_blocks      = [
                "194.78.171.126/32",
            ]
            description      = "SSH for Ordina"
            from_port        = 22
            ipv6_cidr_blocks = []
            prefix_list_ids  = []
            protocol         = "tcp"
            security_groups  = []
            self             = false
            to_port          = 22
        },
        {
            cidr_blocks      = [
                "84.197.77.212/32",
            ]
            description      = "SSH for home"
            from_port        = 22
            ipv6_cidr_blocks = []
            prefix_list_ids  = []
            protocol         = "tcp"
            security_groups  = []
            self             = false
            to_port          = 22
        },
    ]
    name        = "allow-ssh"
    tags        = {}
    vpc_id      = "vpc-222d3b44"

    timeouts {}
}

resource "aws_instance" "ubuntu" {
    ami                          = "ami-02df9ea15c1778c9c"
    associate_public_ip_address  = true
    availability_zone            = "eu-west-1a"
    cpu_core_count               = 1
    cpu_threads_per_core         = 1
    disable_api_termination      = false
    ebs_optimized                = false
    get_password_data            = false
    iam_instance_profile         = "ecsInstanceRole"
    instance_type                = "t2.micro"
    ipv6_address_count           = 0
    ipv6_addresses               = []
    key_name                     = "amazon-linux-keypair"
    monitoring                   = false
    private_ip                   = "172.31.29.222"
    security_groups              = [
        "allow-ssh",
    ]
    source_dest_check            = true
    subnet_id                    = "subnet-19affc51"
    tags                         = {
        "Name" = "ubuntu"
    }
    tenancy                      = "default"
    volume_tags                  = {}
    vpc_security_group_ids       = [
        "sg-09ee9775e566411e9",
    ]

    credit_specification {
        cpu_credits = "standard"
    }

    root_block_device {
        delete_on_termination = true
        encrypted             = false
        iops                  = 100
        volume_size           = 8
        volume_type           = "gp2"
    }

    timeouts {}
}

