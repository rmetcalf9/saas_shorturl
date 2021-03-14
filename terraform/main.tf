# main.tf

module "saas_infra" {
  source = "git::https://github.com/rmetcalf9/tf_saas_service_infra.git?ref=0.0.2"

  ws_name = var.ws_name
  deployment_config = var.deployment_config

  # include_test_public = false
  # include_test_private = false
  # include_main_public = false
  # include_main_private = false

  # No private endpoint. URL's can only be created via MQ event
  secure_test_private = false
  secure_main_private = false

  private_allow_tenant_role_whitelist = [
    "saas_shorturl:hasaccount"
  ]
}

