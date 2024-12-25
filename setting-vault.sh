#!/bin/bash

vault secrets enable transit
vault write -f transit/keys/signing-key type=rsa-2048
vault read transit/keys/signing-key

# policy.hcl
"""
path "transit/keys/signing-key" {
  capabilities = ["read"]
}
"""


vault policy write public-key-policy policy.hcl
vault token create -policy=public-key-policy


