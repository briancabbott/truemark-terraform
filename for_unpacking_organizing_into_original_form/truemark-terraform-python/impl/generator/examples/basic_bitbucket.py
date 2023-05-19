from truemark_terraform import Terraform, Provider, Resource, BitBucketRepositoryResource

# truemark-bitbucket = {
#     source = "truemark.io/terraform/truemark-bitbucket"
p1 = Provider("truemark-bitbucket", source = "truemark.io/terraform/truemark-bitbucket", version = "1.0.0", username="", password="")

# A generic model  
r1 = Resource("truemark-bitbucket_project", "terraform-project-11", name = "terraform-project-11", key = "TFPROJ11",
  is_private = True, description = "an overview of the project.", owner = "babbott@truemark.io")


# Same model, specialized from the provider - not sure about this idea...
r2 = BitBucketRepositoryResource(name = "terraform-project-11", key = "TFPROJ11",
  is_private = True, description = "an overview of the project.", owner = "babbott@truemark.io")


Terraform.Generate().Apply()