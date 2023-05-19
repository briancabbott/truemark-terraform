from truemark_terraform import Terraform, Provider, Resource, Var, Data, BitBucketRepositoryResource



# s3_origin_id = "S3-${var.name}"
# fqdns = [for d in var.domain_names: format("%s%s%s", d.record_name, d.record_name == "" ? "" : ".", d.zone_name)]
# domain_names_create_records = [for d in var.domain_names: d if d.create_record]

var_certificate_domain = None
var_s3_bucket = None
d1 = Data("aws_acm_certificate", "spa", domain = var_certificate_domain, most_recent = True)
d2 = Data("aws_s3_bucket", "spa", bucket = var_s3_bucket)

#------------------------------------------------------------------------------
# Viewer Request Lambda
#------------------------------------------------------------------------------
r1 = Resource("aws_iam_role", "viewer_request", 
    name = "${var.name}-viewer-request", 
    assume_role_policy = file("${path.module}/lambda_policy.json"), 
    tags.Name = "${var.name}-lambda") 
# TODO: We need to figure out nested structures.... 
# tags.Name represents an Idea ... catch the property declarations and make it real by the time the objects finished instantiating... 

d3 = Data("template_file", "viewer_request", template = "${path.module}/viewer_request/index.tpl.js", domain = element(local.fqdns, 0))

# data.template_file should be able to become d3 because the internal reference is no longer needed, just direct property refs
r2 = Resource("local_file", "viewer_request", content = d3.rendered, filename = "${path.module}/viewer_request/index.js", depends_on = [d3])

d4 = Data("archive_file", "viewer_request", type = "zip", source_dir = "${path.module}/viewer_request", 
            output_path = "${path.module}/viewer_request.zip", depends_on = [r2])

r3 = Resource("aws_lambda_function", "viewer_request", filename = d4.output_path, source_code_hash = d4.output_base64sha256, 
             function_name = "${var.name}-viewer-request", role = r1.arn, handler = "index.handler", publish = True, runtime = "nodejs12.x", depends_on = [d4])

policy_json = "{ \
        \"Version\": \"2012-10-17\", \
        \"Statement\": [ \
            { \
            \"Action\": [ \
                \"logs:CreateLogGroup\", \
                \"logs:CreateLogStream\", \
                \"logs:PutLogEvents\" \
            ], \
            \"Resource\": \"arn:aws:logs:*:*:*\", \
            \"Effect\": \"Allow\" \
            } \
        ] \
        }"

r4 = Resource("aws_iam_policy", "viewer_request", name = "${var.name}-viewer-request", path = "/", description = "IAM policy for logging from a lambda", policy = policy_json)
r5 = Resource("aws_iam_role_policy_attachment", "viewer_request", policy_arn = r4.arn, role = r4.name)

#------------------------------------------------------------------------------
# Origin Request Lambda
#------------------------------------------------------------------------------
# TODO: We need to resolve issues like this: (tags.Name)
r6_0 = Resource("aws_iam_role", "origin_request", name = "${var.name}-origin-request", assume_role_policy = file("${path.module}/lambda_policy.json"), tags.Name = "${var.name}-lambda")
r6_1 = Resource("aws_iam_role", "origin_request", name = "${var.name}-origin-request", assume_role_policy = file("${path.module}/lambda_policy.json"), Resource("tags", "Name", "${var.name}-lambda"))

d5 = Data("template_file", "origin_request", template = File("${path.module}/origin_request/index.tpl.js"), domain = element(local.fqdns, 0))
r7 = Resource("local_file", "origin_request", content = d5.rendered, filename = "${path.module}/origin_request/index.js", depends_on = [d5])

d6 = Data("archive_file", "origin_request", type="zip", source_dir="${path.module}/origin_request", output_path="${path.module}/origin_request.zip", depends_on = [local_file.origin_request])

r8 = Resource("aws_lambda_function", "origin_request", filename = d6.output_path, source_code_hash = d6.output_base64sha256, function_name = "${var.name}-origin-request", 
    role = aws_iam_role.origin_request.arn, handler = "index.handler", publish = True, runtime = "nodejs12.x", depends_on = [d6])

mytffile.add(r1, r2)
Terraform.Apply()

# Hit List 
#    1. Looping:
#    2. API calls - to make decisions about what to create
#    3. Dependency Issues:
#    4. Chicken/Egg Resource Deployment
#    


# //resource "aws_cloudwatch_log_group" "origin_request" {
# //  name              = "/aws/lambda/${aws_lambda_function.origin_request.function_name}"
# //  retention_in_days = 2
# //  tags = {}
# //}

# resource "aws_iam_policy" "origin_request" {
#   name        = "${var.name}-origin-request"
#   path        = "/"
#   description = "IAM policy for logging from a lambda"

#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": [
#         "logs:CreateLogGroup",
#         "logs:CreateLogStream",
#         "logs:PutLogEvents"
#       ],
#       "Resource": "arn:aws:logs:*:*:*",
#       "Effect": "Allow"
#     }
#   ]
# }
# EOF
# }

# resource "aws_iam_role_policy_attachment" "origin_request" {
#   policy_arn = aws_iam_policy.origin_request.arn
#   role = aws_iam_role.origin_request.name
# }

# #------------------------------------------------------------------------------
# # CloudFront Distribution
# #------------------------------------------------------------------------------
# resource "aws_cloudfront_origin_access_identity" "spa" {
#   comment = var.name
# }


# s1 = TFObject("statement")
# s1.actions = ["s3:GetObject"]
# s1.resources = ["${data.aws_s3_bucket.spa.arn}/*"]
# s2 = TFObject("statement")
# d7 = Data("aws_iam_policy_document", "spa", 


#     principals {
#       type        = "AWS"
#       identifiers = [aws_cloudfront_origin_access_identity.spa.iam_arn]
#     }
#   }

#   statement {
#     actions   = ["s3:ListBucket"]
#     resources = [data.aws_s3_bucket.spa.arn]

#     principals {
#       type        = "AWS"
#       identifiers = [aws_cloudfront_origin_access_identity.spa.iam_arn]
#     }
#   }
# }

# resource "aws_s3_bucket_policy" "spa" {
#   bucket = data.aws_s3_bucket.spa.id
#   policy = data.aws_iam_policy_document.spa.json
# }



rinner1_4 = 
rinner1_3 = Resource()
rinner1_2 = Resource()
rinner1_1 = 

r1 = R()

resource "aws_cloudfront_distribution" "spa" {

  origin {
    domain_name = data.aws_s3_bucket.spa.bucket_regional_domain_name
    origin_id   = local.s3_origin_id
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.spa.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = var.name
  default_root_object = "index.html"
  aliases             = local.fqdns

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    lambda_function_association {
      event_type = "viewer-request"
      lambda_arn = aws_lambda_function.viewer_request.qualified_arn
    }

    lambda_function_association {
      event_type = "origin-request"
      lambda_arn = aws_lambda_function.origin_request.qualified_arn
    }

    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  price_class = var.price_class

#   restrictions {
#     geo_restriction {
#       restriction_type = "none"
#     }
#   }

#   viewer_certificate {
#     minimum_protocol_version = var.minimum_protocol_version
#     ssl_support_method = "sni-only"
#     acm_certificate_arn = data.aws_acm_certificate.spa.arn
#   }

#   custom_error_response {
#     error_code = "403"
#     response_page_path = var.error_403_response_page_path
#     response_code = var.error_403_response_code
#     error_caching_min_ttl = var.error_403_caching_min_ttl
#   }

#   custom_error_response {
#     error_code = "404"
#     response_page_path = var.error_404_response_page_path
#     response_code = var.error_404_response_code
#     error_caching_min_ttl = var.error_404_caching_min_ttl
#   }
# }

# #------------------------------------------------------------------------------
# # Route53 Records
# #------------------------------------------------------------------------------
# data "aws_route53_zone" "spa" {
#   count = length(local.domain_names_create_records)
#   name = local.domain_names_create_records[count.index].zone_name
#   private_zone = false
# }

# resource "aws_route53_record" "spa" {
#   count = length(local.domain_names_create_records)
#   zone_id = data.aws_route53_zone.spa[count.index].id
#   name    = local.domain_names_create_records[count.index].record_name
#   type    = "A"
#   alias {
#     name = aws_cloudfront_distribution.spa.domain_name
#     zone_id = aws_cloudfront_distribution.spa.hosted_zone_id
#     evaluate_target_health = false
#   }
# }

# #------------------------------------------------------------------------------
# # Invalidation Policy
# #------------------------------------------------------------------------------
# resource "aws_iam_policy" "spa" {
#   name = var.name
#   path = var.path
#   description = "Allows invalidation requests"
#   policy = <<EOF
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "AllowInvalidate",
#             "Effect": "Allow",
#             "Action": "cloudfront:CreateInvalidation",
#             "Resource": "${aws_cloudfront_distribution.spa.arn}"
#         }
#     ]
# }
# EOF
# }
