provider "aws" {
}


terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }

  }

  required_version = ">= 1.0"
}

resource "aws_iam_access_key" "akiaz44hqroiyapvbvo6" {
  status = "Active"
  user   = aws_iam_user.infrabro.name
}

resource "aws_iam_account_alias" "sumitkg" {
  account_alias = "sumitkg"
}

resource "aws_iam_policy" "arn_aws_iam__680499645329_policy_service_role_amazoncomprehendservicepolicy_detecttopicsfromtweets" {
  name   = "AmazonComprehendServicePolicy-DetectTopicsFromTweets"
  path   = "/service-role/"
  policy = "{\"Statement\":[{\"Action\":\"s3:GetObject\",\"Effect\":\"Allow\",\"Resource\":[\"arn:aws:s3:::tweets-of-arvidkahl/*\"]},{\"Action\":\"s3:ListBucket\",\"Effect\":\"Allow\",\"Resource\":[\"arn:aws:s3:::tweets-of-arvidkahl\"]},{\"Action\":\"s3:PutObject\",\"Effect\":\"Allow\",\"Resource\":\"arn:aws:s3:::tweets-of-arvidkahl/*\"}],\"Version\":\"2012-10-17\"}"
}

resource "aws_iam_policy" "arn_aws_iam__680499645329_policy_service_role_awslambdabasicexecutionrole_c0ad4b7c_c411_4888_987f_02bec9c7bb42" {
  name   = "AWSLambdaBasicExecutionRole-c0ad4b7c-c411-4888-987f-02bec9c7bb42"
  path   = "/service-role/"
  policy = "{\"Statement\":[{\"Action\":\"logs:CreateLogGroup\",\"Effect\":\"Allow\",\"Resource\":\"arn:aws:logs:ap-south-1:680499645329:*\"},{\"Action\":[\"logs:CreateLogStream\",\"logs:PutLogEvents\"],\"Effect\":\"Allow\",\"Resource\":[\"arn:aws:logs:ap-south-1:680499645329:log-group:/aws/lambda/bitespeed-identify:*\"]}],\"Version\":\"2012-10-17\"}"
}

resource "aws_iam_policy" "arn_aws_iam__680499645329_policy_service_role_awslambdavpcaccessexecutionrole_35f94556_99c0_4a28_913b_dc2f877bc20a" {
  name   = "AWSLambdaVPCAccessExecutionRole-35f94556-99c0-4a28-913b-dc2f877bc20a"
  path   = "/service-role/"
  policy = "{\"Statement\":[{\"Action\":[\"ec2:CreateNetworkInterface\",\"ec2:DeleteNetworkInterface\",\"ec2:DescribeNetworkInterfaces\"],\"Effect\":\"Allow\",\"Resource\":\"*\"}],\"Version\":\"2012-10-17\"}"
}

resource "aws_iam_role" "amazoncomprehendservicerole_detecttopicsfromtweets" {
  assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"comprehend.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
  description        = "Amazon Comprehend service role for creating custom models and analysis jobs."
  inline_policy {
  }

  managed_policy_arns  = [aws_iam_policy.arn_aws_iam__680499645329_policy_service_role_amazoncomprehendservicepolicy_detecttopicsfromtweets.arn]
  max_session_duration = 3600
  name                 = "AmazonComprehendServiceRole-DetectTopicsFromTweets"
  path                 = "/service-role/"
}

resource "aws_iam_role" "awsserviceroleforrds" {
  assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"rds.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
  description        = "Allows Amazon RDS to manage AWS resources on your behalf"
  inline_policy {
  }

  managed_policy_arns  = ["arn:aws:iam::aws:policy/aws-service-role/AmazonRDSServiceRolePolicy"]
  max_session_duration = 3600
  name                 = "AWSServiceRoleForRDS"
  path                 = "/aws-service-role/rds.amazonaws.com/"
}

resource "aws_iam_role" "awsserviceroleforsupport" {
  assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"support.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
  description        = "Enables resource access for AWS to provide billing, administrative and support services"
  inline_policy {
  }

  managed_policy_arns  = ["arn:aws:iam::aws:policy/aws-service-role/AWSSupportServiceRolePolicy"]
  max_session_duration = 3600
  name                 = "AWSServiceRoleForSupport"
  path                 = "/aws-service-role/support.amazonaws.com/"
}

resource "aws_iam_role" "awsservicerolefortrustedadvisor" {
  assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"trustedadvisor.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
  description        = "Access for the AWS Trusted Advisor Service to help reduce cost, increase performance, and improve security of your AWS environment."
  inline_policy {
  }

  managed_policy_arns  = ["arn:aws:iam::aws:policy/aws-service-role/AWSTrustedAdvisorServiceRolePolicy"]
  max_session_duration = 3600
  name                 = "AWSServiceRoleForTrustedAdvisor"
  path                 = "/aws-service-role/trustedadvisor.amazonaws.com/"
}

resource "aws_iam_role" "bitespeed_identify_role_3m1zf9g5" {
  assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
  inline_policy {
  }

  managed_policy_arns  = [aws_iam_policy.arn_aws_iam__680499645329_policy_service_role_awslambdavpcaccessexecutionrole_35f94556_99c0_4a28_913b_dc2f877bc20a.arn, aws_iam_policy.arn_aws_iam__680499645329_policy_service_role_awslambdabasicexecutionrole_c0ad4b7c_c411_4888_987f_02bec9c7bb42.arn]
  max_session_duration = 3600
  name                 = "bitespeed-identify-role-3m1zf9g5"
  path                 = aws_iam_policy.arn_aws_iam__680499645329_policy_service_role_amazoncomprehendservicepolicy_detecttopicsfromtweets.path
}

resource "aws_iam_role" "rds_monitoring_role" {
  assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"monitoring.rds.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
  inline_policy {
  }

  managed_policy_arns  = ["arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"]
  max_session_duration = 3600
  name                 = "rds-monitoring-role"
  path                 = "/"
}

resource "aws_iam_role_policy_attachment" "amazoncomprehendservicerole_detecttopicsfromtweets_arn_aws_iam__680499645329_policy_service_role_amazoncomprehendservicepolicy_detecttopicsfromtweets" {
  policy_arn = aws_iam_policy.arn_aws_iam__680499645329_policy_service_role_amazoncomprehendservicepolicy_detecttopicsfromtweets.arn
  role       = aws_iam_role.amazoncomprehendservicerole_detecttopicsfromtweets.name
}

resource "aws_iam_role_policy_attachment" "awsserviceroleforrds_arn_aws_iam__aws_policy_aws_service_role_amazonrdsservicerolepolicy" {
  policy_arn = "arn:aws:iam::aws:policy/aws-service-role/AmazonRDSServiceRolePolicy"
  role       = aws_iam_role.awsserviceroleforrds.id
}

resource "aws_iam_role_policy_attachment" "awsserviceroleforsupport_arn_aws_iam__aws_policy_aws_service_role_awssupportservicerolepolicy" {
  policy_arn = "arn:aws:iam::aws:policy/aws-service-role/AWSSupportServiceRolePolicy"
  role       = aws_iam_role.awsserviceroleforsupport.id
}

resource "aws_iam_role_policy_attachment" "awsservicerolefortrustedadvisor_arn_aws_iam__aws_policy_aws_service_role_awstrustedadvisorservicerolepolicy" {
  policy_arn = "arn:aws:iam::aws:policy/aws-service-role/AWSTrustedAdvisorServiceRolePolicy"
  role       = aws_iam_role.awsservicerolefortrustedadvisor.id
}

resource "aws_iam_role_policy_attachment" "bitespeed_identify_role_3m1zf9g5_arn_aws_iam__680499645329_policy_service_role_awslambdabasicexecutionrole_c0ad4b7c_c411_4888_987f_02bec9c7bb42" {
  policy_arn = aws_iam_policy.arn_aws_iam__680499645329_policy_service_role_awslambdabasicexecutionrole_c0ad4b7c_c411_4888_987f_02bec9c7bb42.arn
  role       = aws_iam_role.bitespeed_identify_role_3m1zf9g5.id
}

resource "aws_iam_role_policy_attachment" "bitespeed_identify_role_3m1zf9g5_arn_aws_iam__680499645329_policy_service_role_awslambdavpcaccessexecutionrole_35f94556_99c0_4a28_913b_dc2f877bc20a" {
  policy_arn = aws_iam_policy.arn_aws_iam__680499645329_policy_service_role_awslambdavpcaccessexecutionrole_35f94556_99c0_4a28_913b_dc2f877bc20a.arn
  role       = aws_iam_role.bitespeed_identify_role_3m1zf9g5.id
}

resource "aws_iam_role_policy_attachment" "rds_monitoring_role_arn_aws_iam__aws_policy_service_role_amazonrdsenhancedmonitoringrole" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
  role       = aws_iam_role.rds_monitoring_role.id
}

resource "aws_iam_user" "infrabro" {
  name = "InfraBro"
  path = "/"
}

resource "aws_iam_user_policy_attachment" "infrabro_arn_aws_iam__aws_policy_readonlyaccess" {
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
  user       = aws_iam_user.infrabro.id
}

resource "aws_internet_gateway" "igw_0024b85f76201940d" {
  vpc_id = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_route_table" "rtb_089058b5765270c0c" {
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw_0024b85f76201940d.id
  }

  vpc_id = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_security_group" "sg_0c925a4cdc241164b" {
  description = "default VPC security group"
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
  }

  ingress {
    from_port = 0
    protocol  = "-1"
    self      = true
    to_port   = 0
  }

  name   = "default"
  vpc_id = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_subnet" "subnet_007200f6e190acb0f" {
  availability_zone_id                = "use1-az5"
  cidr_block                          = "172.31.64.0/20"
  map_public_ip_on_launch             = true
  private_dns_hostname_type_on_launch = "ip-name"
  vpc_id                              = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_subnet" "subnet_00ead86370aaad76c" {
  availability_zone_id                = "use1-az6"
  cidr_block                          = "172.31.32.0/20"
  map_public_ip_on_launch             = true
  private_dns_hostname_type_on_launch = "ip-name"
  vpc_id                              = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_subnet" "subnet_0149ebc6be7051e2f" {
  availability_zone_id                = "use1-az4"
  cidr_block                          = "172.31.16.0/20"
  map_public_ip_on_launch             = true
  private_dns_hostname_type_on_launch = "ip-name"
  vpc_id                              = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_subnet" "subnet_0599c1a77bdc18e33" {
  availability_zone_id                = "use1-az2"
  cidr_block                          = "172.31.80.0/20"
  map_public_ip_on_launch             = true
  private_dns_hostname_type_on_launch = "ip-name"
  vpc_id                              = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_subnet" "subnet_079fa47cbd3213cd3" {
  availability_zone_id                = "use1-az3"
  cidr_block                          = "172.31.48.0/20"
  map_public_ip_on_launch             = true
  private_dns_hostname_type_on_launch = "ip-name"
  vpc_id                              = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_subnet" "subnet_0ec713dc14be0251a" {
  availability_zone_id                = "use1-az1"
  cidr_block                          = "172.31.0.0/20"
  map_public_ip_on_launch             = true
  private_dns_hostname_type_on_launch = "ip-name"
  vpc_id                              = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_vpc" "vpc_0f26a8452ed32b8e6" {
  cidr_block           = "172.31.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  instance_tenancy     = "default"
}

resource "aws_route53_resolver_rule_association" "rslvr_autodefined_assoc_vpc_0f26a8452ed32b8e6_internet_resolver" {
  name             = "System Rule Association"
  resolver_rule_id = "rslvr-autodefined-rr-internet-resolver"
  vpc_id           = aws_vpc.vpc_0f26a8452ed32b8e6.id
}

resource "aws_s3_bucket" "tweets_of_arvidkahl" {
  arn            = "arn:aws:s3:::tweets-of-arvidkahl"
  bucket         = "tweets-of-arvidkahl"
  hosted_zone_id = "Z3AQBSTGFYJSTF"
}

