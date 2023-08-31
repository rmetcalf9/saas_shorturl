# main.tf

module "saas_infra" {
  source = "git::https://github.com/rmetcalf9/tf_saas_service_infra.git?ref=0.0.12"

  ws_name = var.ws_name
  deployment_config = var.deployment_config

  # include_test_public = false
  # include_test_private = false
  # include_main_public = false
  # include_main_private = false

  # Private endpoints protected by roles
  secure_test_private = true
  secure_main_private = true

  private_allow_tenant_role_whitelist = [
    "saas_shorturl:hasaccount", "challengeapp:hasaccount", "challengeappstage:hasaccount", "social:hasaccount"
  ]

  # main url section
  mainurl_include = true
  mainurl = "rjm2.cc"
  mainurl_majorversion = "0"
  mainurl_destpath = "/public/api/r/"
  tenant_path_position_main_private = 6
  tenant_path_position_test_private = 6
}
